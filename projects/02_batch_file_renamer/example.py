from pathlib import Path

from laptop_automation.filesystem.batch_renamer.renamer import (
    plan_renames,
)


def main() -> None:
    """Show a batch rename plan without changing files."""
    directory = Path("test_renamer")

    operations = plan_renames(
        directory=directory,
        prefix="Vacation",
        padding=3,
    )

    print("Rename Plan")
    print("=" * 50)

    for operation in operations:
        print(f"{operation.source.name} -> " f"{operation.destination.name}")


if __name__ == "__main__":
    main()
