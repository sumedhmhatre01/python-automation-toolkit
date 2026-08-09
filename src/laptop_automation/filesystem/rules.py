from laptop_automation.filesystem.models import FileCategory

FILE_CATEGORIES = (
    FileCategory(
        name="Images",
        extensions=frozenset(
            {
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".webp",
                ".svg",
            }
        ),
    ),
    FileCategory(
        name="Documents",
        extensions=frozenset(
            {
                ".pdf",
                ".doc",
                ".docx",
                ".txt",
                ".rtf",
                ".odt",
            }
        ),
    ),
    FileCategory(
        name="Spreadsheets",
        extensions=frozenset(
            {
                ".xls",
                ".xlsx",
                ".csv",
                ".ods",
            }
        ),
    ),
    FileCategory(
        name="Presentations",
        extensions=frozenset(
            {
                ".ppt",
                ".pptx",
                ".odp",
            }
        ),
    ),
    FileCategory(
        name="Music",
        extensions=frozenset(
            {
                ".mp3",
                ".wav",
                ".flac",
                ".aac",
                ".ogg",
                ".m4a",
            }
        ),
    ),
    FileCategory(
        name="Videos",
        extensions=frozenset(
            {
                ".mp4",
                ".mkv",
                ".avi",
                ".mov",
                ".wmv",
                ".webm",
            }
        ),
    ),
    FileCategory(
        name="Archives",
        extensions=frozenset(
            {
                ".zip",
                ".rar",
                ".7z",
                ".tar",
                ".gz",
            }
        ),
    ),
)


def get_category_for_extension(
    extension: str,
) -> FileCategory | None:
    """Return the category matching a file extension."""

    normalized_extension = extension.lower()

    for category in FILE_CATEGORIES:
        if normalized_extension in category.extensions:
            return category

    return None
