import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    environment: str = os.getenv(
        "AUTOMATION_ENV",
        "development",
    )

    log_level: str = os.getenv(
        "LOG_LEVEL",
        "INFO",
    )

    data_dir: Path = Path(
        os.getenv(
            "AUTOMATION_DATA_DIR",
            "data",
        )
    )

    backup_dir: Path = Path(
        os.getenv(
            "AUTOMATION_BACKUP_DIR",
            "data/backups",
        )
    )
