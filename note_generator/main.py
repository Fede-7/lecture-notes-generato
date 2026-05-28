"""CLI entrypoint for the lecture notes generator."""

from __future__ import annotations

import argparse
from pathlib import Path

from note_generator.config import DEFAULT_CONFIG
from note_generator.pipeline import LectureNotesPipeline
from note_generator.utils.file_utils import read_text, write_text


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Generate structured lecture notes from raw Italian transcriptions.")
    parser.add_argument("--input", required=True, help="Path to the raw transcription text file.")
    parser.add_argument("--output", required=True, help="Path to the generated Markdown/LaTeX file.")
    parser.add_argument("--format", default=DEFAULT_CONFIG.default_output_format, choices=("markdown", "latex"))
    parser.add_argument("--model", default=DEFAULT_CONFIG.model_settings["default"], help="Optional LM Studio model name.")
    parser.add_argument("--use-llm", action="store_true", help="If set, use the configured LM Studio server with the provided model name and optional prompt path.")
    parser.add_argument("--llm-prompt", help="Path to a prompt template to use with LM Studio. If set, the prompt will be concatenated with the cleaned transcription.")
    return parser


def main() -> int:
    """Run the CLI command."""

    parser = build_parser()
    args = parser.parse_args()
    text = read_text(args.input)
    model_hint = args.model
    # If user requested LLM usage and supplied a prompt, pass prompt path via a
    # lightweight convention in the model_hint string: "{model}|prompt:{path}".
    if args.use_llm and args.llm_prompt:
        model_hint = f"{args.model}|prompt:{args.llm_prompt}"
    pipeline = LectureNotesPipeline(model_hint=model_hint)
    result = pipeline.run(text, output_format=args.format)
    output_path = Path(args.output)
    write_text(output_path, result.output)
    print(f"Generated {args.format} notes at {output_path} using model hint {result.model_hint}.")
    return 0
