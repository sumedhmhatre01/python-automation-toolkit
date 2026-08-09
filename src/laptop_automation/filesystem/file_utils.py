from pathlib import Path

from laptop_automation.core.exceptions import FileOperationError


def is_file(path: Path) -> bool:
    """Return True if the path exists and is a file."""
    return path.is_file()


def ensure_directory(path: Path) -> None:
    """Create a directory if it does not already exist."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise FileOperationError(f"Could not create directory: {path}") from exc


def get_unique_destination(destination: Path) -> Path:
    """
    Return a unique destination path.

    If the destination already exists, a numbered suffix is added.

    Example:
        report.pdf
        report_1.pdf
        report_2.pdf
    """

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = f"{destination.stem}_{counter}" f"{destination.suffix}"

        candidate = destination.with_name(new_name)

        if not candidate.exists():
            return candidate

        counter += 1
