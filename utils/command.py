import os
import shutil
import subprocess
import logging


def resolve_tool(tool_name):
    """
    Find a reconnaissance tool.

    Search order:
    1. Windows/Linux PATH
    2. Standard Windows Go bin directory
    """

    # --------------------------------------------------
    # 1. Search PATH
    # --------------------------------------------------

    path = shutil.which(tool_name)

    if path:
        return path

    # --------------------------------------------------
    # 2. Search standard Go bin directory
    # --------------------------------------------------

    go_bin = os.path.join(
        os.path.expanduser("~"),
        "go",
        "bin"
    )

    candidates = [
        os.path.join(go_bin, tool_name),
        os.path.join(go_bin, tool_name + ".exe")
    ]

    for candidate in candidates:

        if os.path.isfile(candidate):
            return candidate

    return None


def check_tool(tool_name):
    """
    Check whether a command-line tool exists.
    """

    path = resolve_tool(tool_name)

    if not path:

        logging.error(
            "%s was not found in PATH or Go bin directory.",
            tool_name
        )

        return False

    logging.info(
        "%s found at: %s",
        tool_name,
        path
    )

    return True


def run_command(command, output_file=None):
    """
    Execute a command and optionally save stdout.

    Example:

        run_command(
            [
                "subfinder",
                "-d",
                "example.com",
                "-silent"
            ],
            "output.txt"
        )
    """

    if not command:

        logging.error(
            "No command was provided."
        )

        return False

    # --------------------------------------------------
    # Resolve executable
    # --------------------------------------------------

    tool_name = command[0]

    tool_path = resolve_tool(
        tool_name
    )

    if not tool_path:

        logging.error(
            "%s could not be located.",
            tool_name
        )

        return False

    # Replace command name with absolute path
    command = [
        tool_path
    ] + command[1:]

    logging.info(
        "Running: %s",
        " ".join(command)
    )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    try:

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        # --------------------------------------------------
        # Save stdout
        # --------------------------------------------------

        if output_file:

            with open(
                output_file,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    process.stdout
                )

        # --------------------------------------------------
        # Handle command failure
        # --------------------------------------------------

        if process.returncode != 0:

            logging.error(
                "%s failed with return code %s",
                tool_name,
                process.returncode
            )

            if process.stderr:

                logging.error(
                    process.stderr.strip()
                )

            return False

        logging.info(
            "%s completed successfully.",
            tool_name
        )

        # Debug output from tools
        if process.stderr:

            logging.debug(
                process.stderr.strip()
            )

        return True

    except FileNotFoundError:

        logging.error(
            "Executable not found: %s",
            tool_path
        )

        return False

    except PermissionError:

        logging.error(
            "Permission denied: %s",
            tool_path
        )

        return False

    except Exception as exc:

        logging.exception(
            "Unexpected error while executing %s: %s",
            tool_name,
            exc
        )

        return False