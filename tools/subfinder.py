from utils.command import check_tool, run_command


def run_subfinder(
    domain,
    output_file,
    binary="subfinder",
    use_all=True
):
    """
    Run Subfinder against the target domain.
    """

    if not check_tool(binary):
        return False

    command = [
        binary,
        "-d",
        domain,
        "-silent"
    ]

    if use_all:
        command.append("-all")

    return run_command(
        command,
        output_file
    )