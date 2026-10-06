from pathlib import Path

from laptop_automation.core.exceptions import ValidationError


def validate_prefix(prefix: str) -> None:
    """Validate the filename prefix."""

    cleaned_prefix = prefix.strip()

    if not cleaned_prefix:
        raise ValidationError("Prefix cannot be empty.")

    invalid_characters = {
        "<",
        ">",
        ":",
        '"',
        "/",
        "\\",
        "|",
        "?",
        "*",
    }

    if any(character in cleaned_prefix for character in invalid_characters):
        raise ValidationError("Prefix contains invalid filename " "characters.")


def validate_padding(padding: int) -> None:
    """Validate the numeric padding."""

    if padding < 1:
        raise ValidationError("Padding must be at least 1.")
