"""Build a hierarchical outline from topics and classified content."""

from __future__ import annotations

from typing import Any


SECTION_TITLES = {
    "definition": "Definizioni e concetti chiave",
    "example": "Esempi",
    "code": "Codice",
    "table": "Confronti",
    "diagram": "Visualizzazioni",
    "text": "Spiegazione",
}


def _exercise_prompts(title: str) -> list[str]:
    return [
        f"Riassumi i concetti principali della sezione {title}.",
        f"Applica {title.lower()} a un caso di studio discusso a lezione.",
    ]


def build_hierarchy(topics: dict[str, Any], contents: list[dict[str, Any]]) -> dict[str, Any]:
    """Create nested sections and subsections with section identifiers."""

    sections: list[dict[str, Any]] = []
    for section_number, topic in enumerate(topics.values(), start=1):
        topic_sentences = set(topic.get("sentences", []))
        section_contents = [item for item in contents if item["raw"] in topic_sentences]
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in section_contents:
            grouped.setdefault(item["type"], []).append(item)
        subsections: list[dict[str, Any]] = []
        for subsection_number, (content_type, grouped_contents) in enumerate(grouped.items(), start=1):
            subsections.append(
                {
                    "id": f"{section_number}.{subsection_number}",
                    "title": SECTION_TITLES.get(content_type, content_type.capitalize()),
                    "content": grouped_contents,
                    "subsections": [],
                }
            )
        sections.append(
            {
                "id": str(section_number),
                "title": topic.get("title", f"Sezione {section_number}"),
                "keywords": topic.get("keywords", []),
                "content": [],
                "subsections": subsections,
                "exercises": _exercise_prompts(topic.get("title", f"Sezione {section_number}")),
                "cross_references": [],
            }
        )
    return {"title": "Automated Lecture Notes", "structure": sections}
