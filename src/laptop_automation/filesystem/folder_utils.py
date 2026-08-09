from pathlib import Path

from laptop_automation.core.exceptions import FileOperationError


def validate_directory(path: Path) -> None:
    """Validate that the supplied path exists and is a directory."""

    if not path.exists():
        raise FileOperationError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise FileOperationError(f"Path is not a directory: {path}")


def get_files(directory: Path) -> list[Path]:
    """
    Return files directly inside a directory.

    Subdirectories are not scanned.
    """

    validate_directory(directory)

    try:
        return [item for item in directory.iterdir() if item.is_file()]
    except OSError as exc:
        raise FileOperationError(f"Could not read directory: {directory}") from exc
