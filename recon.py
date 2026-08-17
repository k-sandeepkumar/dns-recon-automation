import argparse
import logging
import os
import re
from datetime import datetime
from pathlib import Path

import yaml

from tools.subfinder import run_subfinder
from tools.amass import run_amass
from tools.assetfinder import run_assetfinder
from tools.dnsx import run_dnsx
from tools.httpx import run_httpx

from utils.files import (
    create_directory,
    read_lines,
    write_lines
)

from utils.excel import create_workbook


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------
# Domain validation
# ---------------------------------------------------------

def validate_domain(domain):
    """
    Basic domain validation.
    """

    pattern = r"^(?=.{1,253}$)(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}$"

    return bool(
        re.match(pattern, domain)
    )


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(
                log_file,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ]
    )


# ---------------------------------------------------------
# Normalize subdomain
# ---------------------------------------------------------

def normalize_subdomain(value, root_domain):
    """
    Normalize tool output into a clean hostname.
    """

    value = value.strip().lower()

    if not value:
        return None

    # Remove protocol
    value = re.sub(
        r"^https?://",
        "",
        value
    )

    # Remove path
    value = value.split("/")[0]

    # Remove port
    value = value.split(":")[0]

    # Remove trailing dot
    value = value.rstrip(".")

    # Ignore obvious non-host lines
    if " " in value:
        return None

    if not value.endswith(root_domain):
        return None

    return value


# ---------------------------------------------------------
# Clean tool output
# ---------------------------------------------------------

def clean_tool_output(
    input_file,
    root_domain
):
    """
    Clean and normalize subdomains returned by tools.
    """

    raw_values = read_lines(input_file)

    cleaned = []

    for value in raw_values:

        hostname = normalize_subdomain(
            value,
            root_domain
        )

        if hostname:
            cleaned.append(hostname)

    return sorted(set(cleaned))


# ---------------------------------------------------------
# Build source mapping
# ---------------------------------------------------------

def build_source_mapping(
    tool_results
):
    """
    Map each subdomain to the tools that discovered it.
    """

    mapping = {}

    for tool_name, subdomains in tool_results.items():

        for subdomain in subdomains:

            if subdomain not in mapping:
                mapping[subdomain] = set()

            mapping[subdomain].add(
                tool_name
            )

    return mapping


# ---------------------------------------------------------
# Parse DNSx
# ---------------------------------------------------------

def parse_dnsx(
    dns_file,
    root_domain
):
    """
    Parse DNSx output.

    Keeps the complete DNSx result while extracting
    the hostname where possible.
    """

    results = []

    for line in read_lines(dns_file):

        parts = line.split()

        if not parts:
            continue

        host = parts[0]

        if host.endswith(root_domain):

            results.append(
                (
                    host,
                    line
                )
            )

    return results


# ---------------------------------------------------------
# Parse HTTPx
# ---------------------------------------------------------

def parse_httpx(
    http_file
):
    """
    Parse HTTPx output.

    HTTPx output is kept flexible because formatting can
    vary between versions.
    """

    results = []

    for line in read_lines(http_file):

        parts = line.split()

        if not parts:
            continue

        result = {
            "url": "",
            "status": "",
            "title": "",
            "technology": "",
            "webserver": "",
            "ip": ""
        }

        result["url"] = parts[0]

        for part in parts[1:]:

            status_match = re.search(
                r"\[(\d{3})\]",
                part
            )

            if status_match:
                result["status"] = status_match.group(1)

            if "title" in part.lower():
                result["title"] = part

            if "http" in part.lower():
                continue

        results.append(result)

    return results


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Automated DNS/Subdomain Reconnaissance "
            "and Excel Reporting"
        )
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Authorized target domain"
    )

    args = parser.parse_args()

    domain = args.domain.lower().strip()

    if not validate_domain(domain):

        print(
            "[!] Invalid domain format."
        )

        return

    config = load_config()

    base_output = config[
        "output"
    ][
        "base_directory"
    ]

    report_directory = config[
        "output"
    ][
        "report_directory"
    ]

    log_directory = config[
        "output"
    ][
        "log_directory"
    ]

    # -----------------------------------------------------
    # Create directories
    # -----------------------------------------------------

    target_directory = os.path.join(
        base_output,
        domain
    )

    create_directory(
        target_directory
    )

    create_directory(
        report_directory
    )

    create_directory(
        log_directory
    )

    # -----------------------------------------------------
    # Logging
    # -----------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    log_file = os.path.join(
        log_directory,
        f"{domain}_{timestamp}.log"
    )

    setup_logging(log_file)

    logging.info(
        "Starting reconnaissance for %s",
        domain
    )

    # -----------------------------------------------------
    # Tool paths
    # -----------------------------------------------------

    tools_config = config["tools"]

    subfinder_file = os.path.join(
        target_directory,
        "subfinder.txt"
    )

    amass_file = os.path.join(
        target_directory,
        "amass.txt"
    )

    assetfinder_file = os.path.join(
        target_directory,
        "assetfinder.txt"
    )

    combined_file = os.path.join(
        target_directory,
        "combined_subdomains.txt"
    )

    dnsx_file = os.path.join(
        target_directory,
        "dnsx.txt"
    )

    httpx_file = os.path.join(
        target_directory,
        "httpx.txt"
    )

    # -----------------------------------------------------
    # 1. SUBFINDER
    # -----------------------------------------------------

    logging.info(
        "Running Subfinder..."
    )

    run_subfinder(
        domain,
        subfinder_file,
        tools_config["subfinder"],
        config["settings"]["subfinder_all"]
    )

    # -----------------------------------------------------
    # 2. AMASS
    # -----------------------------------------------------

    logging.info(
        "Running Amass..."
    )

    run_amass(
        domain,
        amass_file,
        tools_config["amass"]
    )

    # -----------------------------------------------------
    # 3. ASSETFINDER
    # -----------------------------------------------------

    logging.info(
        "Running Assetfinder..."
    )

    run_assetfinder(
        domain,
        assetfinder_file,
        tools_config["assetfinder"]
    )

    # -----------------------------------------------------
    # Clean individual outputs
    # -----------------------------------------------------

    subfinder_results = clean_tool_output(
        subfinder_file,
        domain
    )

    amass_results = clean_tool_output(
        amass_file,
        domain
    )

    assetfinder_results = clean_tool_output(
        assetfinder_file,
        domain
    )

    # -----------------------------------------------------
    # Tool results dictionary
    # -----------------------------------------------------

    tool_results = {

        "Subfinder": subfinder_results,

        "Amass": amass_results,

        "Assetfinder": assetfinder_results
    }

    # -----------------------------------------------------
    # Combine all subdomains
    # -----------------------------------------------------

    source_mapping = build_source_mapping(
        tool_results
    )

    combined_subdomains = sorted(
        source_mapping.keys()
    )

    write_lines(
        combined_file,
        combined_subdomains
    )

    logging.info(
        "Total unique subdomains: %d",
        len(combined_subdomains)
    )

    # -----------------------------------------------------
    # 4. DNSx
    # -----------------------------------------------------

    logging.info(
        "Running DNSx..."
    )

    run_dnsx(
        combined_file,
        dnsx_file,
        tools_config["dnsx"]
    )

    # -----------------------------------------------------
    # 5. HTTPx
    # -----------------------------------------------------

    logging.info(
        "Running HTTPx..."
    )

    run_httpx(
        combined_file,
        httpx_file,
        tools_config["httpx"],
        config["settings"]["httpx_threads"]
    )

    # -----------------------------------------------------
    # Parse DNSx
    # -----------------------------------------------------

    dns_results = parse_dnsx(
        dnsx_file,
        domain
    )

    # -----------------------------------------------------
    # Parse HTTPx
    # -----------------------------------------------------

    http_results = parse_httpx(
        httpx_file
    )

    # -----------------------------------------------------
    # Create Excel report
    # -----------------------------------------------------

    report_file = os.path.join(
        report_directory,
        f"{domain}_recon.xlsx"
    )

    create_workbook(
        report_file,
        tool_results,
        source_mapping,
        dns_results,
        http_results
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    logging.info(
        "Reconnaissance completed."
    )

    logging.info(
        "Unique subdomains: %d",
        len(combined_subdomains)
    )

    logging.info(
        "DNS results: %d",
        len(dns_results)
    )

    logging.info(
        "HTTP results: %d",
        len(http_results)
    )

    logging.info(
        "Excel report: %s",
        report_file
    )

    print()
    print("=" * 60)
    print("RECONNAISSANCE COMPLETED")
    print("=" * 60)
    print(
        f"Target             : {domain}"
    )
    print(
        f"Unique subdomains  : {len(combined_subdomains)}"
    )
    print(
        f"DNS results        : {len(dns_results)}"
    )
    print(
        f"HTTP results       : {len(http_results)}"
    )
    print(
        f"Excel report       : {report_file}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()