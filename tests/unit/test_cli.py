from pathlib import Path

from laptop_automation.cli.commands import (
    handle_organize_downloads,
)

from laptop_automation.cli.commands import handle_rename_files


def test_organize_downloads_dry_run(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    image = tmp_path / "photo.jpg"
    image.write_text(
        "test image",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "laptop_automation.cli.commands.get_downloads_directory",
        lambda: tmp_path,
    )

    handle_organize_downloads(dry_run=True)

    captured = capsys.readouterr()

    assert "DRY RUN" in captured.out
    assert "photo.jpg" in captured.out

    # The file must not be moved.
    assert image.exists()
    assert not (tmp_path / "Images" / "photo.jpg").exists()


def test_organize_downloads_cancelled(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    image = tmp_path / "photo.jpg"
    image.write_text(
        "test image",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "laptop_automation.cli.commands.get_downloads_directory",
        lambda: tmp_path,
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "n",
    )

    handle_organize_downloads()

    captured = capsys.readouterr()

    assert "Operation cancelled." in captured.out

    # The file must not be moved.
    assert image.exists()
    assert not (tmp_path / "Images" / "photo.jpg").exists()


def test_organize_downloads_confirmed(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    image = tmp_path / "photo.jpg"
    image.write_text(
        "test image",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "laptop_automation.cli.commands.get_downloads_directory",
        lambda: tmp_path,
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "y",
    )

    handle_organize_downloads()

    captured = capsys.readouterr()

    assert "Successfully moved 1 file(s)." in captured.out

    # The file should now be in Images.
    assert not image.exists()

    assert (tmp_path / "Images" / "photo.jpg").exists()


def test_rename_files_dry_run(
    tmp_path: Path,
    capsys,
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

    handle_rename_files(
        source=str(tmp_path),
        prefix="Vacation",
        dry_run=True,
    )

    captured = capsys.readouterr()

    assert "DRY RUN" in captured.out
    assert "IMG_001.jpg -> Vacation_001.jpg" in captured.out
    assert "IMG_002.jpg -> Vacation_002.jpg" in captured.out

    assert first.exists()
    assert second.exists()
    assert not (tmp_path / "Vacation_001.jpg").exists()
    assert not (tmp_path / "Vacation_002.jpg").exists()


def test_rename_files_cancelled(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    original = tmp_path / "IMG_001.jpg"

    original.write_text(
        "test",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "n",
    )

    handle_rename_files(
        source=str(tmp_path),
        prefix="Vacation",
    )

    captured = capsys.readouterr()

    assert "Operation cancelled." in captured.out
    assert original.exists()
    assert not (tmp_path / "Vacation_001.jpg").exists()


def test_rename_files_confirmed(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    original = tmp_path / "IMG_001.jpg"

    original.write_text(
        "test",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "y",
    )

    handle_rename_files(
        source=str(tmp_path),
        prefix="Vacation",
    )

    captured = capsys.readouterr()

    assert "Successfully renamed 1 file(s)." in captured.out
    assert not original.exists()
    assert (tmp_path / "Vacation_001.jpg").exists()

    assert (tmp_path / "Vacation_001.jpg").read_text(encoding="utf-8") == "test"


def test_rename_files_invalid_prefix(
    tmp_path: Path,
    capsys,
):
    handle_rename_files(
        source=str(tmp_path),
        prefix="Invalid/Prefix",
    )

    captured = capsys.readouterr()

    assert "Error:" in captured.out
    assert "invalid filename characters" in captured.out
