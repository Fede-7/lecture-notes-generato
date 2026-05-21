# Automated Lecture Notes Generator

A Python starter project that turns raw Italian lecture transcriptions into structured academic notes.

## Features
- Six-step modular pipeline: preprocessing, topic analysis, content extraction, structure generation, formatting, and post-processing.
- Markdown output by default, with optional LaTeX rendering.
- Italian-friendly sentence segmentation with spaCy fallbacks.
- Mermaid diagrams, code block preservation, section numbering, cross-references, TOC generation, and end-of-section exercises.
- Hardware-aware defaults for Ryzen AI + RTX laptops, including cache-ready topic extraction via `joblib` and configurable Ollama model hints.

## Project Layout
- `/note_generator`: package modules for each pipeline step.
- `/examples/input`: sample lecture transcriptions.
- `/examples/output`: sample rendered notes.
- `/tests`: focused unit tests for preprocessing, pipeline behavior, and CLI usage.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download it_core_news_sm
```

## Usage
```bash
python main.py --input examples/input/ml_lecture.txt --output notes.md --format markdown --model qwen3:8b
python main.py --input examples/input/ml_lecture.txt --output notes.tex --format latex --model deepseek-coder-v2:16b
```

## Notes
- Install the Pandoc CLI separately if you want to export generated Markdown to PDF.
- The pipeline gracefully falls back to lightweight heuristics when optional NLP dependencies or Italian spaCy models are unavailable.
