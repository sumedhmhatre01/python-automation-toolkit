from laptop_automation.cli.parser import create_parser
from laptop_automation.core.logger import setup_logger

VERSION = "0.1.0"


def main() -> None:
    """Main CLI entry point."""

    logger = setup_logger()

    parser = create_parser()
    args = parser.parse_args()

    if args.command == "version":
        print(f"Laptop Automation Toolkit v{VERSION}")

    elif args.command == "system-info":
        print("System information module coming soon.")

    elif args.command == "screenshot":
        print("Screenshot module coming soon.")

    elif args.command == "organize-downloads":
        print("File organizer module coming soon.")

    else:
        parser.print_help()

        logger.debug("No valid command was provided.")


if __name__ == "__main__":
    main()
