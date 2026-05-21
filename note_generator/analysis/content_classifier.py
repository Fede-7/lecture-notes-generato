"""Sentence-level content classification."""

from __future__ import annotations

import re
from typing import Any


DEFINITION_RE = re.compile(
    r"^(?:Il|Lo|La|I|Gli|Le|Un|Una)\s+(?P<term>[A-Za-zÀ-ÿ0-9_ -]+?)\s+(?:è|e|rappresenta|sono)\s+(?P<description>.+)$"
)
EXAMPLE_RE = re.compile(r"^(?:Ad esempio|Per esempio|Esempio)[:,\s]+(?P<body>.+)$", re.IGNORECASE)
CODE_RE = re.compile(r"```(?P<lang>[A-Za-z0-9_+-]*)\n(?P<body>[\s\S]+?)```")


def _detect_language(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("fun ") or " val " in f" {stripped} ":
        return "ml"
    if stripped.startswith(("def ", "class ", "import ", "from ")):
        return "python"
    if stripped.startswith("#include") or ";" in stripped:
        return "c"
    return "text"


def classify_contents(sentences: list[str]) -> dict[str, list[dict[str, Any]]]:
    """Classify sentences into formatting-oriented content types."""

    contents: list[dict[str, Any]] = []
    for index, sentence in enumerate(sentences):
        code_match = CODE_RE.search(sentence)
        if code_match:
            language = code_match.group("lang") or _detect_language(code_match.group("body"))
            contents.append(
                {
                    "index": index,
                    "type": "code",
                    "raw": sentence,
                    "processed": code_match.group("body").strip(),
                    "language": language,
                }
            )
            continue
        if sentence.strip().startswith(("fun ", "def ", "#include")):
            contents.append(
                {
                    "index": index,
                    "type": "code",
                    "raw": sentence,
                    "processed": sentence.strip(),
                    "language": _detect_language(sentence),
                }
            )
            continue
        definition_match = DEFINITION_RE.match(sentence.strip())
        if definition_match:
            contents.append(
                {
                    "index": index,
                    "type": "definition",
                    "raw": sentence,
                    "processed": {
                        "term": definition_match.group("term").strip(),
                        "description": definition_match.group("description").strip(),
                    },
                }
            )
            continue
        example_match = EXAMPLE_RE.match(sentence.strip())
        if example_match:
            contents.append(
                {
                    "index": index,
                    "type": "example",
                    "raw": sentence,
                    "processed": example_match.group("body").strip(),
                }
            )
            continue
        if "|" in sentence:
            contents.append({"index": index, "type": "table", "raw": sentence, "processed": sentence.strip()})
            continue
        if any(token in sentence.lower() for token in ("albero", "diagramma", "flusso", "grafo")):
            contents.append({"index": index, "type": "diagram", "raw": sentence, "processed": sentence.strip()})
            continue
        contents.append({"index": index, "type": "text", "raw": sentence, "processed": sentence.strip()})
    return {"contents": contents}
