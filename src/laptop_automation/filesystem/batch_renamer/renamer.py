from pathlib import Path

from laptop_automation.core.exceptions import FileOperationError
from laptop_automation.filesystem.batch_renamer.models import RenameOperation
from laptop_automation.filesystem.batch_renamer.rules import generate_filename
from laptop_automation.filesystem.batch_renamer.validator import (
    validate_padding,
    validate_prefix,
)


def get_files(directory: Path) -> list[Path]:
    """
    Return files directly inside the directory.

    Subdirectories are not scanned.
    """
    if not directory.exists():
        raise FileOperationError(f"Directory does not exist: {directory}")

    if not directory.is_dir():
        raise FileOperationError(f"Path is not a directory: {directory}")

    try:
        return sorted(
            (path for path in directory.iterdir() if path.is_file()),
            key=lambda path: path.name.lower(),
        )
    except OSError as exc:
        raise FileOperationError(f"Could not read directory: {directory}") from exc


def plan_renames(
    directory: Path,
    prefix: str,
    padding: int = 3,
) -> list[RenameOperation]:
    """Create a rename plan without changing any files."""
    validate_prefix(prefix)
    validate_padding(padding)

    files = get_files(directory)

    operations: list[RenameOperation] = []

    for index, file_path in enumerate(files, start=1):
        new_name = generate_filename(
            prefix=prefix,
            index=index,
            original_file=file_path,
            padding=padding,
        )

        destination = directory / new_name

        operations.append(
            RenameOperation(
                source=file_path,
                destination=destination,
            )
        )

    return operations


def validate_rename_operations(
    operations: list[RenameOperation],
) -> None:
    """
    Validate a rename plan before modifying any files.

    Existing destination files are never overwritten.
    """
    source_paths = {operation.source.resolve() for operation in operations}

    for operation in operations:
        source = operation.source
        destination = operation.destination

        if destination.exists():
            destination_resolved = destination.resolve()

            if destination_resolved not in source_paths:
                raise FileOperationError(
                    "Rename destination already exists: " f"{destination}"
                )


def execute_rename(operation: RenameOperation) -> Path:
    """
    Rename one file.

    The destination must not already contain an unrelated file.
    """
    source = operation.source
    destination = operation.destination

    if not source.exists():
        raise FileOperationError(f"Source file does not exist: {source}")

    if destination.exists() and destination.resolve() != source.resolve():
        raise FileOperationError("Rename destination already exists: " f"{destination}")

    try:
        source.rename(destination)
    except OSError as exc:
        raise FileOperationError(
            f"Could not rename file: " f"{source} -> {destination}"
        ) from exc

    return destination


def execute_renames(
    operations: list[RenameOperation],
) -> list[Path]:
    """
    Execute a validated rename plan.

    All operations are validated before any file is renamed.
    """
    validate_rename_operations(operations)

    renamed_files: list[Path] = []

    for operation in operations:
        destination = execute_rename(operation)
        renamed_files.append(destination)

    return renamed_files
