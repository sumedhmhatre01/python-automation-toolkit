import shutil
from pathlib import Path

from laptop_automation.core.exceptions import FileOperationError
from laptop_automation.filesystem.file_utils import (
    ensure_directory,
    get_unique_destination,
)
from laptop_automation.filesystem.folder_utils import (
    get_files,
)
from laptop_automation.filesystem.models import (
    FileOperation,
)
from laptop_automation.filesystem.rules import (
    get_category_for_extension,
)


def plan_organization(
    directory: Path,
) -> list[FileOperation]:
    """
    Create a plan for organizing files.

    This function does not move, rename, or delete files.
    It only determines where supported files should go.
    """

    operations: list[FileOperation] = []

    files = get_files(directory)

    for file_path in files:
        category = get_category_for_extension(file_path.suffix)

        # Leave unsupported file types untouched.
        if category is None:
            continue

        destination_directory = directory / category.name

        destination = destination_directory / file_path.name

        destination = get_unique_destination(destination)

        operations.append(
            FileOperation(
                source=file_path,
                destination=destination,
            )
        )

    return operations


def execute_operation(
    operation: FileOperation,
) -> Path:
    """
    Move one file to its planned destination.

    The destination directory is created automatically.
    """

    try:
        ensure_directory(operation.destination.parent)

        shutil.move(
            str(operation.source),
            str(operation.destination),
        )

        return operation.destination

    except OSError as exc:
        raise FileOperationError(
            f"Could not move file: "
            f"{operation.source} -> "
            f"{operation.destination}"
        ) from exc


def execute_organization(
    operations: list[FileOperation],
) -> list[Path]:
    """
    Execute a previously generated organization plan.

    Returns the destinations of successfully
    moved files.
    """

    moved_files: list[Path] = []

    for operation in operations:
        destination = execute_operation(operation)

        moved_files.append(destination)

    return moved_files
