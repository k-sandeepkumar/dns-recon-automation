from utils.command import check_tool, run_command


def run_httpx(
    input_file,
    output_file,
    binary="httpx",
    threads=50
):
    """
    Probe discovered hosts for HTTP/HTTPS services.
    """

    if not check_tool(binary):
        return False

    command = [
        binary,
        "-l",
        input_file,
        "-silent",
        "-status-code",
        "-title",
        "-tech-detect",
        "-web-server",
        "-ip",
        "-threads",
        str(threads)
    ]

    return run_command(
        command,
        output_file
    )