from pathlib import Path

import pytest

from laptop_automation.core.exceptions import (
    FileOperationError,
    ValidationError,
)
from laptop_automation.filesystem.batch_renamer.renamer import (
    plan_renames,
)
from laptop_automation.filesystem.batch_renamer.rules import (
    generate_filename,
)
from laptop_automation.filesystem.batch_renamer.validator import (
    validate_padding,
    validate_prefix,
)


def test_generate_filename():
    filename = generate_filename(
        "Vacation",
        1,
        Path("IMG_001.jpg"),
    )

    assert filename == "Vacation_001.jpg"


def test_generate_filename_preserves_extension():
    filename = generate_filename(
        "Report",
        12,
        Path("document.pdf"),
    )

    assert filename == "Report_012.pdf"


def test_generate_filename_padding():
    filename = generate_filename(
        "Photo",
        7,
        Path("image.png"),
        padding=4,
    )

    assert filename == "Photo_0007.png"


def test_validate_prefix_rejects_empty_prefix():
    with pytest.raises(ValidationError):
        validate_prefix("")


def test_validate_prefix_rejects_invalid_character():
    with pytest.raises(ValidationError):
        validate_prefix("Vacation/Photos")


def test_validate_prefix_accepts_valid_prefix():
    validate_prefix("Vacation_2026")


def test_validate_padding_rejects_zero():
    with pytest.raises(ValidationError):
        validate_padding(0)


def test_plan_renames_files(
    tmp_path: Path,
):
    first = tmp_path / "IMG_001.jpg"
    second = tmp_path / "IMG_002.jpg"

    first.write_text(
        "one",
        encoding="utf-8",
    )

    second.write_text(
        "two",
        encoding="utf-8",
    )

    operations = plan_renames(
        tmp_path,
        "Vacation",
    )

    assert len(operations) == 2

    assert operations[0].source == first
    assert operations[0].destination == tmp_path / "Vacation_001.jpg"

    assert operations[1].source == second
    assert operations[1].destination == tmp_path / "Vacation_002.jpg"


def test_plan_renames_does_not_modify_files(
    tmp_path: Path,
):
    original = tmp_path / "IMG_001.jpg"

    original.write_text(
        "test",
        encoding="utf-8",
    )

    plan_renames(
        tmp_path,
        "Vacation",
    )

    assert original.exists()
    assert not (tmp_path / "Vacation_001.jpg").exists()


def test_plan_renames_rejects_missing_directory(
    tmp_path: Path,
):
    missing = tmp_path / "missing"

    with pytest.raises(FileOperationError):
        plan_renames(
            missing,
            "Vacation",
        )


from laptop_automation.filesystem.batch_renamer.models import RenameOperation
from laptop_automation.filesystem.batch_renamer.renamer import (
    execute_rename,
    execute_renames,
)


def test_execute_rename(tmp_path: Path):
    original = tmp_path / "IMG_001.jpg"
    destination = tmp_path / "Vacation_001.jpg"

    original.write_text(
        "photo",
        encoding="utf-8",
    )

    operation = RenameOperation(
        source=original,
        destination=destination,
    )

    result = execute_rename(operation)

    assert result == destination
    assert destination.exists()
    assert not original.exists()
    assert destination.read_text(encoding="utf-8") == "photo"


def test_execute_rename_rejects_existing_destination(
    tmp_path: Path,
):
    original = tmp_path / "IMG_001.jpg"
    destination = tmp_path / "Vacation_001.jpg"

    original.write_text(
        "original",
        encoding="utf-8",
    )

    destination.write_text(
        "existing",
        encoding="utf-8",
    )

    operation = RenameOperation(
        source=original,
        destination=destination,
    )

    with pytest.raises(FileOperationError):
        execute_rename(operation)

    assert original.exists()
    assert destination.exists()

    assert original.read_text(encoding="utf-8") == "original"

    assert destination.read_text(encoding="utf-8") == "existing"


def test_execute_rename_rejects_missing_source(
    tmp_path: Path,
):
    source = tmp_path / "missing.jpg"
    destination = tmp_path / "Vacation_001.jpg"

    operation = RenameOperation(
        source=source,
        destination=destination,
    )

    with pytest.raises(FileOperationError):
        execute_rename(operation)


def test_execute_renames(tmp_path: Path):
    first = tmp_path / "IMG_001.jpg"
    second = tmp_path / "IMG_002.jpg"

    first.write_text(
        "one",
        encoding="utf-8",
    )

    second.write_text(
        "two",
        encoding="utf-8",
    )

    operations = plan_renames(
        tmp_path,
        "Vacation",
    )

    renamed_files = execute_renames(operations)

    assert renamed_files == [
        tmp_path / "Vacation_001.jpg",
        tmp_path / "Vacation_002.jpg",
    ]

    assert not first.exists()
    assert not second.exists()

    assert (tmp_path / "Vacation_001.jpg").read_text(encoding="utf-8") == "one"

    assert (tmp_path / "Vacation_002.jpg").read_text(encoding="utf-8") == "two"
