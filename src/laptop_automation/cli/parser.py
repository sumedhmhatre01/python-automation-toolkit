import argparse


def create_parser() -> argparse.ArgumentParser:
    """Create the main command-line parser."""

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
        help=("Folder to organize. " "Defaults to the Downloads folder."),
    )

    organize_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files.",
    )

    return parser
