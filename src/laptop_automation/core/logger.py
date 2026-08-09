import logging
from pathlib import Path

DEFAULT_LOG_DIR = Path("logs")
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "automation.log"


def setup_logger(
    name: str = "laptop_automation",
    level: int = logging.INFO,
) -> logging.Logger:
    """Create and configure the application logger."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        DEFAULT_LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
