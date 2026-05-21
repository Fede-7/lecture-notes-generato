"""File I/O helpers."""

from __future__ import annotations

from pathlib import Path


def read_text(path: str | Path) -> str:
    """Read UTF-8 text from a file."""

    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    """Write UTF-8 text to a file, creating parents as needed."""

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
