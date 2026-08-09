from laptop_automation.filesystem.rules import (
    get_category_for_extension,
)

from laptop_automation.core.exceptions import FileOperationError


def test_jpg_is_image():
    category = get_category_for_extension(".jpg")

    assert category is not None
    assert category.name == "Images"


def test_pdf_is_document():
    category = get_category_for_extension(".pdf")

    assert category is not None
    assert category.name == "Documents"


def test_extension_is_case_insensitive():
    category = get_category_for_extension(".JPG")

    assert category is not None
    assert category.name == "Images"


def test_unknown_extension_returns_none():
    category = get_category_for_extension(".unknown")

    assert category is None


from pathlib import Path

from laptop_automation.filesystem.file_utils import (
    ensure_directory,
    get_unique_destination,
    is_file,
)


def test_is_file(tmp_path: Path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello", encoding="utf-8")

    assert is_file(file_path)


def test_is_file_returns_false_for_directory(tmp_path: Path):
    directory = tmp_path / "folder"
    directory.mkdir()

    assert not is_file(directory)


def test_ensure_directory_creates_directory(tmp_path: Path):
    directory = tmp_path / "new_folder"

    ensure_directory(directory)

    assert directory.exists()
    assert directory.is_dir()


def test_unique_destination_when_file_exists(tmp_path: Path):
    existing_file = tmp_path / "report.pdf"
    existing_file.write_text("existing", encoding="utf-8")

    destination = get_unique_destination(existing_file)

    assert destination == tmp_path / "report_1.pdf"


def test_unique_destination_multiple_files(tmp_path: Path):
    first = tmp_path / "report.pdf"
    second = tmp_path / "report_1.pdf"

    first.write_text("one", encoding="utf-8")
    second.write_text("two", encoding="utf-8")

    destination = get_unique_destination(first)

    assert destination == tmp_path / "report_2.pdf"


from laptop_automation.filesystem.folder_utils import (
    get_files,
    validate_directory,
)


def test_validate_directory_accepts_directory(tmp_path: Path):
    directory = tmp_path / "folder"
    directory.mkdir()

    validate_directory(directory)


import pytest


def test_validate_directory_rejects_missing_directory(
    tmp_path: Path,
):
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileOperationError):
        validate_directory(missing_directory)


def test_get_files_returns_only_files(tmp_path: Path):
    file_one = tmp_path / "one.txt"
    file_two = tmp_path / "two.pdf"

    file_one.write_text("one", encoding="utf-8")
    file_two.write_text("two", encoding="utf-8")

    folder = tmp_path / "subfolder"
    folder.mkdir()

    files = get_files(tmp_path)

    assert file_one in files
    assert file_two in files
    assert folder not in files


def test_get_files_does_not_scan_subdirectories(
    tmp_path: Path,
):
    subfolder = tmp_path / "subfolder"
    subfolder.mkdir()

    nested_file = subfolder / "nested.txt"
    nested_file.write_text(
        "nested",
        encoding="utf-8",
    )

    files = get_files(tmp_path)

    assert nested_file not in files


from laptop_automation.filesystem.organizer import (
    plan_organization,
)


def test_plan_organization_creates_image_operation(
    tmp_path: Path,
):
    image = tmp_path / "photo.jpg"
    image.write_text("image", encoding="utf-8")

    operations = plan_organization(tmp_path)

    assert len(operations) == 1
    assert operations[0].source == image
    assert operations[0].destination == tmp_path / "Images" / "photo.jpg"


def test_plan_organization_creates_document_operation(
    tmp_path: Path,
):
    document = tmp_path / "report.pdf"
    document.write_text("report", encoding="utf-8")

    operations = plan_organization(tmp_path)

    assert len(operations) == 1
    assert operations[0].destination == tmp_path / "Documents" / "report.pdf"


def test_plan_organization_ignores_unknown_extensions(
    tmp_path: Path,
):
    unknown_file = tmp_path / "file.xyz"
    unknown_file.write_text("unknown", encoding="utf-8")

    operations = plan_organization(tmp_path)

    assert operations == []


def test_plan_organization_does_not_modify_files(
    tmp_path: Path,
):
    image = tmp_path / "photo.jpg"
    image.write_text("image", encoding="utf-8")

    plan_organization(tmp_path)

    assert image.exists()
    assert not (tmp_path / "Images").exists()


from laptop_automation.filesystem.organizer import (
    execute_organization,
    plan_organization,
)


def test_execute_organization_moves_file(
    tmp_path: Path,
):
    image = tmp_path / "photo.jpg"
    image.write_text("image", encoding="utf-8")

    operations = plan_organization(tmp_path)

    moved_files = execute_organization(operations)

    destination = tmp_path / "Images" / "photo.jpg"

    assert not image.exists()
    assert destination.exists()
    assert destination in moved_files


def test_execute_organization_preserves_existing_file(
    tmp_path: Path,
):
    first_image = tmp_path / "photo.jpg"
    first_image.write_text(
        "first",
        encoding="utf-8",
    )

    operations = plan_organization(tmp_path)
    execute_organization(operations)

    second_image = tmp_path / "photo.jpg"
    second_image.write_text(
        "second",
        encoding="utf-8",
    )

    operations = plan_organization(tmp_path)
    execute_organization(operations)

    first_destination = tmp_path / "Images" / "photo.jpg"

    second_destination = tmp_path / "Images" / "photo_1.jpg"

    assert first_destination.read_text(encoding="utf-8") == "first"

    assert second_destination.read_text(encoding="utf-8") == "second"
