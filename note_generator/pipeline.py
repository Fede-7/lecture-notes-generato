"""Main pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from note_generator.analysis.content_classifier import classify_contents
from note_generator.analysis.topic_extractor import extract_topics
from note_generator.config import DEFAULT_CONFIG, PipelineConfig
from note_generator.formatting.latex_formatter import format_latex
from note_generator.formatting.markdown_formatter import format_markdown
from note_generator.postprocessing.cross_referencer import add_cross_references
from note_generator.postprocessing.validator import validate_structure
from note_generator.preprocessing.cleaner import clean_transcription
from note_generator.structuring.hierarchy_builder import build_hierarchy


@dataclass
class PipelineArtifacts:
    """Intermediate pipeline outputs for debugging and extension."""

    cleaned: dict[str, Any]
    topics: dict[str, Any]
    contents: dict[str, Any]
    structure: dict[str, Any]
    output: str
    model_hint: str


class LectureNotesPipeline:
    """Six-step pipeline that converts lecture transcripts into structured notes."""

    def __init__(self, config: PipelineConfig = DEFAULT_CONFIG, model_hint: str | None = None) -> None:
        self.config = config
        self.model_hint = model_hint or config.model_settings["default"]

    def run(self, text: str, output_format: str | None = None) -> PipelineArtifacts:
        """Execute the full pipeline and return all intermediate artifacts."""

        chosen_format = (output_format or self.config.default_output_format).lower()
        cleaned = clean_transcription(text, self.config)
        topics = extract_topics(cleaned["sentences"], self.config)
        contents = classify_contents(cleaned["sentences"])
        structure = build_hierarchy(topics["topics"], contents["contents"])
        structure = add_cross_references(validate_structure(structure))
        if chosen_format == "latex":
            output = format_latex(structure)
        else:
            output = format_markdown(structure)
        return PipelineArtifacts(
            cleaned=cleaned,
            topics=topics,
            contents=contents,
            structure=structure,
            output=output,
            model_hint=self.model_hint,
        )
