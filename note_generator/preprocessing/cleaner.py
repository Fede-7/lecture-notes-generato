"""Text cleaning and sentence segmentation."""

from __future__ import annotations

import re
from typing import Any

from note_generator.config import DEFAULT_CONFIG, PipelineConfig
from note_generator.utils.nlp_utils import split_sentences


FILLER_TEMPLATE = r"(?:^|(?<=[\s,.;:!?]))({})(?=$|(?=[\s,.;:!?]))"


def clean_transcription(text: str, config: PipelineConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    """Normalize a raw lecture transcription."""

    cleaned = text.strip()
    if config.filler_words:
        filler_pattern = FILLER_TEMPLATE.format("|".join(map(re.escape, config.filler_words)))
        cleaned = re.sub(filler_pattern, " ", cleaned, flags=re.IGNORECASE)
    for pattern, replacement in config.math_replacements:
        cleaned = re.sub(pattern, f" {replacement} ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?<=\d)\s*x\s*(?=\d)", " * ", cleaned)
    cleaned = re.sub(r"\s+([,.;:!?])", r"\1", cleaned)
    cleaned = re.sub(r"([,.;:!?])(\w)", r"\1 \2", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    sentences = split_sentences(cleaned)
    return {"cleaned_text": cleaned, "sentences": sentences}
