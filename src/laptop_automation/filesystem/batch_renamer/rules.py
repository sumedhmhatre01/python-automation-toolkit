from pathlib import Path


def generate_filename(
    prefix: str,
    index: int,
    original_file: Path,
    padding: int = 3,
) -> str:
    """
    Generate a new filename while preserving the
    original file extension.

    Example:
        prefix = "Vacation"
        index = 1
        original_file = photo.jpg

    Result:
        Vacation_001.jpg
    """

    number = str(index).zfill(padding)

    return f"{prefix}_{number}" f"{original_file.suffix}"
