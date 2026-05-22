"""LaTeX formatter for lecture notes."""

from __future__ import annotations

from typing import Any


SECTION_COMMANDS = {1: "section", 2: "subsection", 3: "subsubsection"}


def _render_content(item: dict[str, Any]) -> str:
    if item["type"] == "definition":
        processed = item["processed"]
        return f"\\textbf{{{processed['term']}}}: {processed['description']}"
    if item["type"] == "example":
        return f"\\begin{{quote}}\\textbf{{Esempio}}: {item['processed']}\\end{{quote}}"
    if item["type"] == "code":
        return "\\begin{verbatim}\n" + item["processed"] + "\n\\end{verbatim}"
    return item["processed"].replace("_", "\\_") if isinstance(item["processed"], str) else str(item["processed"])


def _render_section(section: dict[str, Any], level: int = 1) -> str:
    command = SECTION_COMMANDS.get(level, "paragraph")
    blocks = [f"\\{command}{{{section['id']} {section['title']}}}"]
    for item in section.get("content", []):
        blocks.append(_render_content(item))
    for subsection in section.get("subsections", []):
        blocks.append(_render_section(subsection, level + 1))
    if section.get("cross_references"):
        references = ", ".join(f"Section {reference['id']}" for reference in section["cross_references"])
        blocks.append(f"See {references}.")
    if section.get("exercises"):
        blocks.append("\\paragraph{Esercizi}")
        blocks.append("\\begin{itemize}")
        blocks.extend(f"\\item {exercise}" for exercise in section["exercises"])
        blocks.append("\\end{itemize}")
    return "\n\n".join(blocks)


def format_latex(document: dict[str, Any]) -> str:
    """Render the hierarchical structure as a LaTeX document."""

    body = "\n\n".join(_render_section(section) for section in document["structure"])
    return (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\begin{document}\n"
        f"\\title{{{document.get('title', 'Automated Lecture Notes')}}}\n"
        "\\maketitle\n"
        f"{body}\n"
        "\\end{document}\n"
    )
