from utils.command import check_tool, run_command


def run_assetfinder(
    domain,
    output_file,
    binary="assetfinder"
):
    """
    Run Assetfinder.
    """

    if not check_tool(binary):
        return False

    command = [
        binary,
        "--subs-only",
        domain
    ]

    return run_command(
        command,
        output_file
    )