"""Structure validation helpers."""

from __future__ import annotations

from typing import Any


def validate_structure(document: dict[str, Any]) -> dict[str, Any]:
    """Remove empty sections and subsections from the generated structure."""

    valid_sections: list[dict[str, Any]] = []
    for section in document.get("structure", []):
        subsections = [
            subsection
            for subsection in section.get("subsections", [])
            if subsection.get("content") or subsection.get("subsections")
        ]
        if section.get("content") or subsections or section.get("exercises"):
            section["subsections"] = subsections
            valid_sections.append(section)
    document["structure"] = valid_sections
    return document
