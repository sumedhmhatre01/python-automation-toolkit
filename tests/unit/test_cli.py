from pathlib import Path

from laptop_automation.cli.commands import (
    handle_organize_downloads,
)


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
