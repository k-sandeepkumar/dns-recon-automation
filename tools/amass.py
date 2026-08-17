from utils.command import check_tool, run_command


def run_amass(
    domain,
    output_file,
    binary="amass"
):
    """
    Run Amass passive enumeration.
    """

    if not check_tool(binary):
        return False

    command = [
        binary,
        "enum",
        "-passive",
        "-d",
        domain
    ]

    return run_command(
        command,
        output_file
    )