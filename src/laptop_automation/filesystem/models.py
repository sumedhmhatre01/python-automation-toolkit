from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileCategory:
    """Represents a file category and its supported extensions."""

    name: str
    extensions: frozenset[str]


@dataclass(frozen=True)
class FileOperation:
    """Represents a planned file move."""

    source: Path
    destination: Path
