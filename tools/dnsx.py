from utils.command import check_tool, run_command


def run_dnsx(
    input_file,
    output_file,
    binary="dnsx"
):
    """
    Resolve discovered subdomains using DNSx.
    """

    if not check_tool(binary):
        return False

    command = [
        binary,
        "-l",
        input_file,
        "-silent"
    ]

    return run_command(
        command,
        output_file
    )