"""Markdown formatter for lecture notes."""

from __future__ import annotations

from typing import Any

from note_generator.formatting.mermaid_generator import generate_mermaid_diagram

try:
    from jinja2 import Template
except Exception:  # pragma: no cover - optional dependency
    Template = None


def _render_content(item: dict[str, Any]) -> str:
    content_type = item["type"]
    if content_type == "definition":
        processed = item["processed"]
        return f"**{processed['term']}**: {processed['description']}"
    if content_type == "example":
        return f"> **Esempio**: {item['processed']}"
    if content_type == "code":
        return f"```{item.get('language', 'text')}\n{item['processed']}\n```"
    if content_type == "table":
        return item["processed"]
    if content_type == "diagram":
        return f"```mermaid\n{generate_mermaid_diagram(item['processed'])}\n```"
    return item["processed"]


def _build_toc(sections: list[dict[str, Any]]) -> str:
    lines = ["## Indice"]
    for section in sections:
        lines.append(f"- [{section['id']} {section['title']}](#{section['id']}-{section['title'].lower().replace(' ', '-')})")
        for subsection in section.get("subsections", []):
            lines.append(
                f"  - [{subsection['id']} {subsection['title']}](#{subsection['id']}-{subsection['title'].lower().replace(' ', '-')})"
            )
    return "\n".join(lines)


def format_markdown(document: dict[str, Any]) -> str:
    """Render the hierarchical structure as Markdown."""

    sections = document["structure"]
    section_blocks: list[str] = []
    for section in sections:
        blocks = [f"## {section['id']} {section['title']}"]
        for item in section.get("content", []):
            blocks.append(_render_content(item))
        for subsection in section.get("subsections", []):
            blocks.append(f"### {subsection['id']} {subsection['title']}")
            for item in subsection.get("content", []):
                blocks.append(_render_content(item))
        if section.get("cross_references"):
            references = ", ".join(
                f"Section {reference['id']} ({reference['title']})" for reference in section["cross_references"]
            )
            blocks.append(f"See {references}.")
        if section.get("exercises"):
            blocks.append("### Esercizi")
            blocks.extend(f"- {exercise}" for exercise in section["exercises"])
        section_blocks.append("\n\n".join(blocks))

    context = {
        "title": document.get("title", "Automated Lecture Notes"),
        "toc": _build_toc(sections),
        "sections": "\n\n---\n\n".join(section_blocks),
    }
    if Template is not None:
        template = Template("# {{ title }}\n\n{{ toc }}\n\n---\n\n{{ sections }}\n")
        return template.render(**context)
    return f"# {context['title']}\n\n{context['toc']}\n\n---\n\n{context['sections']}\n"
