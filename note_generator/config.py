"""Project configuration values."""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path


@dataclass(frozen=True)
class PipelineConfig:
    """Runtime configuration for the lecture notes pipeline."""

    filler_words: tuple[str, ...] = (
        "quindi",
        "allora",
        "cioè",
        "diciamo",
        "eh",
        "comunque",
        "tipo",
        "niente",
        "dunque",
        "praticamente",
    )
    math_replacements: tuple[tuple[str, str], ...] = (
        (r"\bpi[uù]\b", "+"),
        (r"\bmeno\b", "-"),
        (r"\bper\b", "*"),
        (r"\bdiviso(?: per)?\b", "/"),
    )
    stopwords: tuple[str, ...] = (
        "però",
        "poi",
        "anche",
        "ovviamente",
        "così",
        "sempre",
        "molto",
        "invece",
        "ancora",
        "già",
    )
    max_topics: int = 4
    sentences_per_topic: int = 3
    default_output_format: str = "markdown"
    cache_dir: Path = field(default_factory=lambda: Path(".cache") / "lecture_notes")
    model_settings: dict[str, str] = field(
        default_factory=lambda: {
            "default": os.getenv(
                "LM_STUDIO_MODEL",
                "qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2",
            ),
            "coding": "deepseek-ai/deepseek-coder-v2-lite-instruct",
            "reasoning": os.getenv(
                "LM_STUDIO_REASONING_MODEL",
                "jackrong/qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2",
            ),
        }
    )
    llm_backend: str = field(default_factory=lambda: os.getenv("LLM_BACKEND", "lm_studio"))
    lm_studio_api_url: str = field(default_factory=lambda: os.getenv("LM_STUDIO_API_URL", "http://localhost:1234/v1"))
    lm_studio_api_key: str | None = field(default_factory=lambda: os.getenv("LM_STUDIO_API_KEY"))
    lm_studio_system_prompt: str = field(
        default_factory=lambda: os.getenv(
            "LM_STUDIO_SYSTEM_PROMPT",
            "Sei un assistente preciso e coerente. Segui le istruzioni alla lettera.",
        )
    )


DEFAULT_CONFIG = PipelineConfig()
