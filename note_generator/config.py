"""Project configuration values."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    """Runtime configuration for the lecture notes pipeline."""

    filler_words: tuple[str, ...] = (
        "ok",
        "okay",
        "allora",
        "vabbè",
        "cioè",
        "diciamo",
        "praticamente",
    )
    math_replacements: tuple[tuple[str, str], ...] = (
        (r"\bpi[uù]\b", "+"),
        (r"\bmeno\b", "-"),
        (r"\bper\b", "*"),
        (r"\bdiviso(?: per)?\b", "/"),
    )
    stopwords: tuple[str, ...] = (
        "il",
        "lo",
        "la",
        "i",
        "gli",
        "le",
        "un",
        "una",
        "uno",
        "di",
        "a",
        "da",
        "in",
        "con",
        "su",
        "per",
        "tra",
        "fra",
        "e",
        "o",
        "ma",
        "che",
        "del",
        "della",
        "dello",
        "degli",
        "delle",
        "dei",
        "questa",
        "questo",
        "quello",
        "quella",
        "abbiamo",
        "visto",
        "parliamo",
    )
    max_topics: int = 4
    sentences_per_topic: int = 3
    default_output_format: str = "markdown"
    cache_dir: Path = field(default_factory=lambda: Path(".cache") / "lecture_notes")
    model_settings: dict[str, str] = field(
        default_factory=lambda: {
            "default": "qwen3:8b",
            "coding": "deepseek-coder-v2:16b",
            "reasoning": "qwen2.5:14b",
        }
    )


DEFAULT_CONFIG = PipelineConfig()
