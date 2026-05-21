"""Cross-reference helpers."""

from __future__ import annotations

from typing import Any


def add_cross_references(document: dict[str, Any]) -> dict[str, Any]:
    """Add lightweight section-to-section cross references."""

    sections = document.get("structure", [])
    for index, section in enumerate(sections[:-1]):
        current_keywords = set(section.get("keywords", []))
        matches = []
        for candidate in sections[index + 1 :]:
            if current_keywords & set(candidate.get("keywords", [])):
                matches.append({"id": candidate["id"], "title": candidate["title"]})
        if not matches and index + 1 < len(sections):
            candidate = sections[index + 1]
            matches.append({"id": candidate["id"], "title": candidate["title"]})
        section["cross_references"] = matches[:2]
    return document
