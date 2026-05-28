"""Main pipeline orchestration."""

from __future__ import annotations

import json
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
from note_generator.llm.llm_client import generate as llm_generate


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

        # If a model_hint begins with "prompt:", treat the rest as a path
        # to a prompt template file and call the local LLM. This keeps all
        # preprocessing but delegates structure/rendering to the model when
        # available. The `model_hint` still selects the model name.
        prompt_path = None
        # Backwards-compatible: allow passing prompt path via model_hint like
        # "qwen3:8b|prompt:path/to/prompt.md" (simple convention).
        if isinstance(self.model_hint, str) and "|prompt:" in self.model_hint:
            parts = self.model_hint.split("|prompt:")
            self.model_hint = parts[0]
            prompt_path = parts[1]

        # If a prompt_path was supplied, invoke the LLM with the prompt + cleaned text.
        if prompt_path:
            try:
                with open(prompt_path, "r", encoding="utf-8") as fh:
                    prompt_template = fh.read()
            except Exception:
                prompt_template = ""
            model_prompt = prompt_template + "\n\nTRASCRIZIONE:\n" + cleaned.get("cleaned_text", "")
            try:
                llm_out = llm_generate(
                    model_prompt,
                    model=self.model_hint,
                    base_url=self.config.lm_studio_api_url,
                    api_key=self.config.lm_studio_api_key,
                    system_prompt=self.config.lm_studio_system_prompt,
                )
                # Try to parse JSON structure+rendered_markdown returned by model
                try:
                    parsed = json.loads(llm_out)
                    structure = parsed.get("structure")
                    output = parsed.get("rendered_markdown") or parsed.get("rendered_markdown", "")
                    topics = {}
                    contents = {}
                except Exception:
                    # If model returned plain markdown, use it as output and
                    # fall back to local structure generation for artifacts.
                    output = llm_out
                    topics = extract_topics(cleaned["sentences"], self.config)
                    contents = classify_contents(cleaned["sentences"])
                    structure = build_hierarchy(topics["topics"], contents["contents"])
                    structure = add_cross_references(validate_structure(structure))
            except RuntimeError as exc:
                # LLM not available: fallback to deterministic pipeline
                topics = extract_topics(cleaned["sentences"], self.config)
                contents = classify_contents(cleaned["sentences"])
                structure = build_hierarchy(topics["topics"], contents["contents"])
                structure = add_cross_references(validate_structure(structure))
                if chosen_format == "latex":
                    output = format_latex(structure)
                else:
                    output = format_markdown(structure)
        else:
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
