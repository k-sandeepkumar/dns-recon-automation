from pathlib import Path


def create_directory(path):
    """
    Create directory if it doesn't exist.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def read_lines(file_path):
    """
    Read non-empty lines from a file.
    """
    path = Path(file_path)

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return [
            line.strip()
            for line in f
            if line.strip()
        ]


def write_lines(file_path, lines):
    """
    Write unique sorted lines to a file.
    """
    unique_lines = sorted(set(lines))

    with open(file_path, "w", encoding="utf-8") as f:
        for line in unique_lines:
            f.write(line + "\n")