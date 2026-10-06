import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="laptop-automation",
        description="Python Laptop Automation Toolkit",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
    )

    subparsers.add_parser(
        "version",
        help="Show toolkit version.",
    )

    subparsers.add_parser(
        "system-info",
        help="Display system information.",
    )

    subparsers.add_parser(
        "screenshot",
        help="Take a screenshot.",
    )

    organize_parser = subparsers.add_parser(
        "organize-downloads",
        help="Organize files in a selected folder.",
    )

    organize_parser.add_argument(
        "--source",
        type=str,
        help="Folder to organize. Defaults to the Downloads folder.",
    )

    organize_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files.",
    )

    rename_parser = subparsers.add_parser(
        "rename-files",
        help="Batch rename files in a selected folder.",
    )

    rename_parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="Folder containing the files to rename.",
    )

    rename_parser.add_argument(
        "--prefix",
        type=str,
        required=True,
        help="Prefix to use for the new filenames.",
    )

    rename_parser.add_argument(
        "--padding",
        type=int,
        default=3,
        help="Number of digits for numbering. Defaults to 3.",
    )

    rename_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without renaming files.",
    )

    return parser
