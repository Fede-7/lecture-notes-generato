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
    parser.add_argument("--model", default=DEFAULT_CONFIG.model_settings["default"], help="Optional Ollama model hint.")
    return parser


def main() -> int:
    """Run the CLI command."""

    parser = build_parser()
    args = parser.parse_args()
    text = read_text(args.input)
    pipeline = LectureNotesPipeline(model_hint=args.model)
    result = pipeline.run(text, output_format=args.format)
    output_path = Path(args.output)
    write_text(output_path, result.output)
    print(f"Generated {args.format} notes at {output_path} using model hint {result.model_hint}.")
    return 0
