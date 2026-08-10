from pathlib import Path

from laptop_automation.cli.parser import create_parser
from laptop_automation.core.exceptions import FileOperationError
from laptop_automation.core.logger import setup_logger
from laptop_automation.filesystem.organizer import (
    execute_organization,
    plan_organization,
)

VERSION = "0.1.0"


def get_downloads_directory() -> Path:
    """Return the current user's Downloads directory."""

    return Path.home() / "Downloads"


def display_organization_plan(
    operations,
    downloads_directory: Path,
) -> None:
    """Display the files that will be organized."""

    for operation in operations:
        relative_destination = operation.destination.relative_to(downloads_directory)

        print(f"{operation.source.name}" f" -> " f"{relative_destination}")


def handle_organize_downloads(
    source: str | None = None,
    dry_run: bool = False,
) -> None:
    """Handle the organize-downloads command."""

    logger = setup_logger()

    if source is None:
        downloads_directory = get_downloads_directory()
    else:
        downloads_directory = Path(source).expanduser()

    logger.info(
        "Checking organization directory: %s",
        downloads_directory,
    )

    try:
        operations = plan_organization(downloads_directory)

    except FileOperationError as exc:
        print(f"Error: {exc}")

    logger.error(
        "Could not access organization directory: %s",
        exc,
    )

    return

    if not operations:
        print("No supported files found.")
        return

    print()

    if dry_run:
        print("DRY RUN")
        print("=" * 50)
        print("No files will be moved.")
        print()

        display_organization_plan(
            operations,
            downloads_directory,
        )

        return

    print("ORGANIZATION PLAN")
    print("=" * 50)
    print()

    display_organization_plan(
        operations,
        downloads_directory,
    )

    print()
    print(f"{len(operations)} file(s) " "will be moved.")

    print()

    confirmation = input("Do you want to continue? [y/N]: ").strip().lower()

    if confirmation not in {"y", "yes"}:
        print("Operation cancelled.")

        logger.info("File organization cancelled by user.")

        return

    print()
    print("Organizing files...")

    try:
        moved_files = execute_organization(operations)

    except Exception:
        logger.exception("File organization failed.")

        print("An error occurred while organizing " "the files.")

        return

    print()

    print(f"Successfully moved " f"{len(moved_files)} file(s).")

    logger.info(
        "Successfully moved %d file(s).",
        len(moved_files),
    )


def main() -> None:
    """Main CLI entry point."""

    parser = create_parser()
    args = parser.parse_args()

    if args.command == "version":
        print(f"Laptop Automation Toolkit v{VERSION}")

    elif args.command == "system-info":
        print("System information module coming soon.")

    elif args.command == "screenshot":
        print("Screenshot module coming soon.")

    elif args.command == "organize-downloads":
        handle_organize_downloads(
            source=args.source,
            dry_run=args.dry_run,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
