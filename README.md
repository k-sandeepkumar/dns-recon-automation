# DNS Recon Automation

Automated DNS and subdomain reconnaissance tool for **authorized VAPT and security assessment engagements**.

DNS Recon Automation runs multiple reconnaissance tools independently, preserves their raw outputs, combines and deduplicates discovered subdomains, performs DNS resolution and HTTP/HTTPS probing, tracks the source of each discovered subdomain, and generates a consolidated Excel report.

> **⚠️ Authorized Use Only**
>
> Use this project only against domains, systems, and applications that you own or have **explicit written authorization** to assess.

---

## Features

* 🔎 Subdomain enumeration using:

  * Subfinder
  * Amass
  * Assetfinder
* 📁 Preserves individual raw output from every enumeration tool
* 🔗 Combines and deduplicates discovered subdomains
* 🌐 Performs DNS resolution using DNSx
* 🔥 Performs HTTP/HTTPS service discovery using HTTPx
* 🏷️ Tracks which enumeration tool discovered each subdomain
* 📊 Generates a consolidated Excel report
* 📝 Maintains timestamped reconnaissance logs
* 📂 Organizes output by target domain
* 🔄 Designed for repeatable VAPT reconnaissance workflows
* 🪟 Supports Windows PowerShell-based installation and execution

---

# Architecture

The automation follows this pipeline:

```text
                         Target Domain
                              │
                              ▼
                 ┌─────────────────────────┐
                 │   Subdomain Enumeration  │
                 └─────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ┌─────────┐     ┌─────────┐     ┌────────────┐
         │Subfinder│     │  Amass  │     │ Assetfinder│
         └────┬────┘     └────┬────┘     └─────┬──────┘
              │               │                 │
              ▼               ▼                 ▼
        Raw Output      Raw Output        Raw Output
              │               │                 │
              └───────────────┼─────────────────┘
                              ▼
                    ┌──────────────────┐
                    │ Deduplication    │
                    └────────┬─────────┘
                             ▼
                  Combined Subdomains
                             │
                             ▼
                       ┌──────────┐
                       │   DNSx   │
                       └────┬─────┘
                            ▼
                     Resolved Hosts
                            │
                            ▼
                       ┌──────────┐
                       │  HTTPx   │
                       └────┬─────┘
                            ▼
                    Live Web Services
                            │
                            ▼
                    ┌────────────────┐
                    │ Excel Report   │
                    └────────────────┘
```

---

# Project Structure

```text
dns-recon-automation/
│
├── README.md
├── requirements.txt
├── .gitignore
├── config.yaml
├── recon.py
├── install_tools.ps1
│
├── tools/
│   ├── __init__.py
│   ├── subfinder.py
│   ├── amass.py
│   ├── assetfinder.py
│   ├── dnsx.py
│   └── httpx.py
│
├── utils/
│   ├── __init__.py
│   ├── command.py
│   ├── files.py
│   └── excel.py
│
├── output/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
└── logs/
    └── .gitkeep
```

### Directory Description

| Path                | Purpose                                                |
| ------------------- | ------------------------------------------------------ |
| `recon.py`          | Main automation entry point                            |
| `config.yaml`       | Tool names and runtime configuration                   |
| `install_tools.ps1` | Windows installation and verification script           |
| `tools/`            | Wrappers for reconnaissance tools                      |
| `utils/`            | Command execution, file handling, and Excel generation |
| `output/`           | Raw and intermediate reconnaissance results            |
| `reports/`          | Final Excel reports                                    |
| `logs/`             | Timestamped execution logs                             |

---

# Requirements

The project requires:

### Operating System

* Windows 10/11
* PowerShell

### Programming Languages

* Python 3.x
* Go

### Reconnaissance Tools

* Subfinder
* Amass
* Assetfinder
* DNSx
* HTTPx

### Python Dependencies

```text
openpyxl
PyYAML
```

Install them with:

```powershell
pip install -r requirements.txt
```

---

# 1. Install Go

Go is required because the reconnaissance tools are installed using Go.

## Option 1 — Official Go Installer

Download Go from the official website:

[Go Downloads](https://go.dev/dl/?utm_source=chatgpt.com)

Download the Windows installer (`.msi`) appropriate for your system.

For most modern Windows systems:

```text
Windows x86-64
```

Run the installer and keep the default installation options:

```text
Next → Install → Finish
```

Close and reopen PowerShell.

Verify the installation:

```powershell
go version
```

Example:

```text
go version go1.xx.x windows/amd64
```

---

## Option 2 — Install Go Using Winget

If `winget` is available:

```powershell
winget install --id GoLang.Go
```

Close and reopen PowerShell.

Verify:

```powershell
go version
```

---

# 2. Configure Go Binary PATH

Go-installed binaries are normally placed in:

```text
C:\Users\<YourUsername>\go\bin
```

This directory should be available in your Windows `PATH`.

Check the current PATH:

```powershell
$env:PATH
```

To add the Go binary directory for the current user:

```powershell
$GoBin = "$env:USERPROFILE\go\bin"

[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "User") + ";$GoBin",
    "User"
)
```

Close and reopen PowerShell.

Verify:

```powershell
$env:PATH
```

You should see the Go binary directory in the PATH.

---

# 3. Install Reconnaissance Tools

The project uses the following tools:

| Tool        | Purpose                                          |
| ----------- | ------------------------------------------------ |
| Subfinder   | Passive subdomain enumeration                    |
| Amass       | Comprehensive attack-surface and DNS enumeration |
| Assetfinder | Domain and subdomain discovery                   |
| DNSx        | DNS resolution                                   |
| HTTPx       | HTTP/HTTPS service probing                       |

---

## Automatic Installation — Windows

The repository includes:

```text
install_tools.ps1
```

Open PowerShell.

If required, allow locally created PowerShell scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Run the installation script from the project root:

```powershell
.\install_tools.ps1
```

The script should:

1. Check whether Go is installed.
2. Install the required reconnaissance tools.
3. Verify that the binaries are available.
4. Display the installed tool versions.

---

# 4. Manual Tool Installation

If you prefer to install the tools manually, first verify Go:

```powershell
go version
```

Then install the required tools:

### Subfinder

```powershell
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### Amass

```powershell
go install github.com/owasp-amass/amass/v4/...@master
```

### Assetfinder

```powershell
go install github.com/tomnomnom/assetfinder@latest
```

### DNSx

```powershell
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
```

### HTTPx

```powershell
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

---

# 5. Verify Reconnaissance Tools

Verify each tool individually:

```powershell
subfinder -version
```

```powershell
amass -version
```

```powershell
assetfinder -h
```

```powershell
dnsx -version
```

```powershell
httpx -version
```

All commands should execute successfully before running the Python automation.

If a command is not recognized, verify that:

```text
C:\Users\<YourUsername>\go\bin
```

is included in your PATH.

---

# 6. Install Python Dependencies

From the project root:

```powershell
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
openpyxl
PyYAML
```

Verify Python:

```powershell
python --version
```

---

# 7. Configuration

The project uses:

```text
config.yaml
```

Example configuration:

```yaml
tools:
  subfinder: subfinder
  amass: amass
  assetfinder: assetfinder
  dnsx: dnsx
  httpx: httpx

settings:
  subfinder_all: true
  amass_timeout: 10
  httpx_threads: 50

output:
  base_directory: output
  report_directory: reports
  log_directory: logs
```

## Configuration Parameters

### Tools

The `tools` section defines the executable names or paths.

```yaml
tools:
  subfinder: subfinder
  amass: amass
  assetfinder: assetfinder
  dnsx: dnsx
  httpx: httpx
```

If a binary is installed at a custom location, its path can be configured accordingly.

### Settings

```yaml
settings:
  subfinder_all: true
  amass_timeout: 10
  httpx_threads: 50
```

| Setting         | Description                                       |
| --------------- | ------------------------------------------------- |
| `subfinder_all` | Enables the configured Subfinder enumeration mode |
| `amass_timeout` | Timeout configuration for Amass                   |
| `httpx_threads` | Number of HTTPx worker threads                    |

### Output

```yaml
output:
  base_directory: output
  report_directory: reports
  log_directory: logs
```

These directories control where reconnaissance results, reports, and logs are stored.

---

# 8. Run the Automation

From the project root:

```powershell
python recon.py -d example.com
```

Replace `example.com` with an authorized target domain.

Example:

```powershell
python recon.py -d authorized-target.example
```

> Only use domains for which you have explicit authorization.

---

# 9. Reconnaissance Workflow

The automation executes the following stages.

## Stage 1 — Subdomain Enumeration

The following tools run independently:

```text
Subfinder
Amass
Assetfinder
```

Each tool produces its own raw output.

Example:

```text
output/example.com/subfinder.txt
output/example.com/amass.txt
output/example.com/assetfinder.txt
```

---

## Stage 2 — Combine and Deduplicate

The individual results are combined into:

```text
combined_subdomains.txt
```

Duplicate subdomains are removed.

Example:

```text
api.example.com
dev.example.com
mail.example.com
staging.example.com
```

Each unique subdomain is retained only once in the combined list.

---

## Stage 3 — DNS Resolution

The combined subdomain list is passed to DNSx.

DNSx identifies hosts that successfully resolve through DNS.

Output:

```text
dnsx.txt
```

This stage helps distinguish discovered names from hosts that currently resolve.

---

## Stage 4 — HTTP/HTTPS Probing

Resolved hosts are passed to HTTPx.

HTTPx identifies reachable HTTP/HTTPS services and collects configured service information.

Output:

```text
httpx.txt
```

Depending on the configuration, HTTPx results can contain information such as:

* URL
* HTTP status
* Title
* Technology information
* Web server information
* Content length
* Response metadata

---

# 10. Output Structure

After execution, a target-specific directory is created:

```text
output/
└── example.com/
    ├── subfinder.txt
    ├── amass.txt
    ├── assetfinder.txt
    ├── combined_subdomains.txt
    ├── dnsx.txt
    └── httpx.txt
```

This design preserves the original output of every reconnaissance stage.

---

# 11. Excel Report

The final report is generated under:

```text
reports/
└── example.com_recon.xlsx
```

The workbook contains separate sheets for the major reconnaissance stages.

### Workbook Sheets

```text
Subfinder
Amass
Assetfinder
Combined
DNSx
HTTPx
```

---

## Combined Sheet

The `Combined` sheet tracks which enumeration tools discovered each subdomain.

Example:

| Subdomain             | Source                        |
| --------------------- | ----------------------------- |
| `api.example.com`     | Amass, Subfinder              |
| `dev.example.com`     | Assetfinder, Subfinder        |
| `mail.example.com`    | Amass                         |
| `staging.example.com` | Amass, Assetfinder, Subfinder |

This provides useful visibility into the overlap and coverage of the individual enumeration tools.

---

# 12. Logs

Each execution generates a timestamped log file.

Example:

```text
logs/
└── example.com_2026-08-17_18-30-00.log
```

The log records information such as:

* Target domain
* Start time
* End time
* Tool execution
* Tool errors
* Number of discovered subdomains
* Number of unique subdomains
* DNS resolution results
* HTTP/HTTPS results
* Excel report location

Example:

```text
[INFO] Target: example.com
[INFO] Starting Subfinder
[INFO] Starting Amass
[INFO] Starting Assetfinder
[INFO] Combining subdomains
[INFO] Starting DNSx
[INFO] Starting HTTPx
[INFO] Generating Excel report
[INFO] Reconnaissance completed
```

---

# 13. Expected Terminal Output

A successful execution should display a summary similar to:

```text
============================================================
              RECONNAISSANCE COMPLETED
============================================================

Target              : example.com
Unique subdomains   : 127
DNS results         : 113
HTTP results        : 48

Excel report        : reports/example.com_recon.xlsx
Output directory    : output/example.com/
Log file            : logs/example.com_2026-08-17_18-30-00.log

============================================================
```

> The numbers above are examples only. Actual results depend on the authorized target and the data returned by the reconnaissance tools.

---

# 14. Complete Setup Example

A typical workflow on a new Windows machine:

## Step 1 — Verify Go

```powershell
go version
```

---

## Step 2 — Configure PowerShell

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Step 3 — Install Reconnaissance Tools

```powershell
.\install_tools.ps1
```

---

## Step 4 — Verify Tools

```powershell
subfinder -version
amass -version
assetfinder -h
dnsx -version
httpx -version
```

---

## Step 5 — Install Python Dependencies

```powershell
pip install -r requirements.txt
```

---

## Step 6 — Configure the Project

Review:

```text
config.yaml
```

Make sure the configured tool names and output directories are correct.

---

## Step 7 — Run Reconnaissance

```powershell
python recon.py -d authorized-target.example
```

---

## Step 8 — Review Raw Results

```text
output/authorized-target.example/
```

---

## Step 9 — Review Excel Report

```text
reports/authorized-target.example_recon.xlsx
```

---

## Step 10 — Review Logs

```text
logs/
```

---

# 15. Data Flow

The complete data flow is:

```text
                    Authorized Target
                           │
                           ▼
                ┌─────────────────────┐
                │ Subdomain Discovery │
                └──────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
      Subfinder          Amass         Assetfinder
          │                │                │
          ▼                ▼                ▼
      Raw Data          Raw Data          Raw Data
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  Combine + Deduplicate
                           │
                           ▼
               combined_subdomains.txt
                           │
                           ▼
                         DNSx
                           │
                           ▼
                      Resolved Hosts
                           │
                           ▼
                        HTTPx
                           │
                           ▼
                    Live Web Services
                           │
                           ▼
                   Excel Report (.xlsx)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
        VAPT Analysis               Evidence
```

---

# 16. Why Individual Tool Outputs Are Preserved

The project intentionally does **not** discard the original output from individual tools.

For example:

```text
subfinder.txt
amass.txt
assetfinder.txt
```

are preserved even after creating:

```text
combined_subdomains.txt
```

This provides several advantages:

* Tool-level traceability
* Easier troubleshooting
* Comparison of enumeration coverage
* Reproducibility
* Better VAPT documentation
* Easier validation of discovered assets
* Evidence preservation for assessment reports

---

# 17. Reconnaissance Evidence

For each target, the following evidence can be retained:

```text
Target
  │
  ├── Subfinder results
  ├── Amass results
  ├── Assetfinder results
  │
  ├── Combined subdomains
  │
  ├── DNS resolution results
  │
  ├── HTTP/HTTPS results
  │
  ├── Excel report
  │
  └── Execution log
```

This makes the automation suitable for structured VAPT reconnaissance workflows.

---

# 18. Error Handling

The automation should continue safely when an individual reconnaissance tool fails.

For example:

```text
Subfinder       → SUCCESS
Amass           → SUCCESS
Assetfinder     → FAILED
DNSx            → SUCCESS
HTTPx           → SUCCESS
Excel Report    → SUCCESS
```

The failure should be recorded in the log while allowing the remaining workflow to continue where possible.

Tool failures should never be silently ignored.

---

# 19. Security Considerations

This project is intended for **authorized security assessment and reconnaissance**.

Before running the automation:

* Confirm ownership or written authorization.
* Confirm the exact target scope.
* Avoid unauthorized third-party domains.
* Follow the engagement's rate limits.
* Respect exclusions defined in the assessment scope.
* Store reconnaissance results securely.
* Do not commit sensitive reconnaissance data to public repositories.

Recommended `.gitignore` entries:

```text
__pycache__/
*.pyc
.env

output/*
!output/.gitkeep

reports/*
!reports/.gitkeep

logs/*
!logs/.gitkeep
```

---

# 20. Troubleshooting

## `go` is not recognized

Check:

```powershell
go version
```

If PowerShell cannot find Go, restart PowerShell and verify that Go is installed.

---

## Reconnaissance tool is not recognized

Example:

```text
subfinder : The term 'subfinder' is not recognized...
```

Check whether the Go binary directory exists:

```powershell
Test-Path "$env:USERPROFILE\go\bin"
```

Check the PATH:

```powershell
$env:PATH
```

The following directory should be present:

```text
C:\Users\<YourUsername>\go\bin
```

---

## Python dependency error

Run:

```powershell
python -m pip install --upgrade pip
```

Then:

```powershell
pip install -r requirements.txt
```

---

## PowerShell execution-policy error

Run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then execute:

```powershell
.\install_tools.ps1
```

---

## Excel report is not generated

Check:

```text
logs/
```

for the execution error.

Also verify that:

```powershell
pip install openpyxl
```

has completed successfully.

---

# 21. Recommended VAPT Workflow

A typical authorized assessment workflow can be organized as:

```text
Scope Confirmation
       │
       ▼
Target Domain
       │
       ▼
DNS & Subdomain Recon
       │
       ▼
Asset Consolidation
       │
       ▼
DNS Resolution
       │
       ▼
HTTP/HTTPS Discovery
       │
       ▼
Asset Inventory
       │
       ▼
Manual Validation
       │
       ▼
Vulnerability Assessment
       │
       ▼
Evidence Collection
       │
       ▼
VAPT Reporting
```

DNS Recon Automation focuses on the **reconnaissance and asset-inventory stages** of this workflow.

---

# 22. Future Enhancements

Potential future improvements include:

* [ ] Multi-target input file support
* [ ] Scheduled reconnaissance
* [ ] Historical result comparison
* [ ] New subdomain detection
* [ ] Removed subdomain detection
* [ ] DNS record collection
* [ ] IP address mapping
* [ ] ASN and CIDR enrichment
* [ ] HTTP status tracking
* [ ] Technology fingerprinting
* [ ] Screenshot collection
* [ ] JSON output
* [ ] CSV output
* [ ] SQLite/PostgreSQL result storage
* [ ] Web-based dashboard
* [ ] Email/notification integration
* [ ] Configurable tool execution profiles
* [ ] Retry and timeout management
* [ ] Assessment-specific scope/exclusion handling

---

# 23. Project Goal

The goal of this project is to provide a **repeatable, traceable, and organized DNS/subdomain reconnaissance workflow** for authorized VAPT engagements.

Instead of manually executing multiple tools and merging their results, the automation provides:

```text
Multiple Recon Tools
        ↓
Independent Evidence
        ↓
Deduplication
        ↓
DNS Validation
        ↓
HTTP/HTTPS Discovery
        ↓
Source Tracking
        ↓
Excel Report
        ↓
VAPT Asset Inventory
```

---

# 24. License and Authorized Use

This project is intended for security professionals, penetration testers, VAPT teams, and security researchers performing **authorized assessments**.

The user is responsible for ensuring that all targets are within the authorized assessment scope.

**Do not use this project to perform reconnaissance against systems without permission.**

---

## Quick Start

For experienced users, the complete workflow is:

```powershell
# 1. Verify Go
go version

# 2. Allow local PowerShell scripts
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 3. Install reconnaissance tools
.\install_tools.ps1

# 4. Verify tools
subfinder -version
amass -version
assetfinder -h
dnsx -version
httpx -version

# 5. Install Python dependencies
pip install -r requirements.txt

# 6. Run against an authorized target
python recon.py -d authorized-target.example
```

Results:

```text
output/
└── authorized-target.example/

reports/
└── authorized-target.example_recon.xlsx

logs/
└── authorized-target.example_<timestamp>.log
```

**DNS Recon Automation — Discover → Validate → Consolidate → Report**
