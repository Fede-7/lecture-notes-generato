"""Helpers to build Mermaid diagrams from textual descriptions."""

from __future__ import annotations

import re


EXPRESSION_RE = re.compile(r"(?P<a>\d+)\s*(?P<op1>[+\-*/])\s*(?P<b>\d+)\s*(?P<op2>[+\-*/])\s*(?P<c>\d+)")


def generate_mermaid_diagram(text: str) -> str:
    """Generate a small Mermaid graph for tree/flow descriptions."""

    match = EXPRESSION_RE.search(text)
    if match:
        groups = match.groupdict()
        return "\n".join(
            [
                "graph TD",
                f"    A[{groups['op1']}] --> B[{groups['a']}]",
                f"    A --> C[{groups['op2']}]",
                f"    C --> D[{groups['b']}]",
                f"    C --> E[{groups['c']}]",
            ]
        )
    return "\n".join(
        [
            "graph TD",
            "    A[Argomento] --> B[Concetto Chiave]",
            "    A --> C[Dettaglio]",
        ]
    )
