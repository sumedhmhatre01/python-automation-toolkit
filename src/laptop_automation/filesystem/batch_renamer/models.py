from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RenameOperation:
    """Represents a planned file rename."""

    source: Path
    destination: Path