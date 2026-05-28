# Lecture Notes Generator

Python pipeline for turning lecture transcriptions into structured study notes.

## Features

- Six-step modular pipeline: preprocessing, topic analysis, content extraction, structure generation, formatting, and post-processing.
- Markdown output by default, with optional LaTeX rendering.
- Italian-friendly sentence segmentation with spaCy fallbacks.
- Mermaid diagrams, code block preservation, section numbering, cross-references, TOC generation, and end-of-section exercises.
- Hardware-aware defaults for Ryzen AI + RTX laptops, including cache-ready topic extraction via `joblib` and configurable LM Studio model hints.

## Project Layout

- `note_generator`: package modules for each pipeline step.
- `examples/input`: sample lecture transcriptions.
- `examples/output`: sample rendered notes.
- `tests`: focused unit tests for preprocessing, pipeline behavior, and CLI usage.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download it_core_news_sm
```

## LM Studio Backend

The optional LLM path uses LM Studio's OpenAI-compatible API.

Set these environment variables if you want to customize the connection:

```bash
export LLM_BACKEND=lm_studio
export LM_STUDIO_API_URL="http://localhost:1234/v1"
export LM_STUDIO_MODEL="qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2"
export LM_STUDIO_API_KEY="your-api-key"  # optional
export LM_STUDIO_FALLBACK_MODELS="qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2,qwen2.5-7b-instruct-1m,deepseek-coder-v2-lite-instruct"
```

## Usage

```bash
python main.py --input examples/input/ml_lecture.txt --output notes.md --format markdown --model jackrong/qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2 --use-llm --llm-prompt prompt-appunti.md
python main.py --input examples/input/ml_lecture.txt --output notes.tex --format latex --model deepseek-ai/deepseek-coder-v2-lite-instruct --use-llm --llm-prompt prompt-appunti.md
```

## Notes

- Install the Pandoc CLI separately if you want to export generated Markdown to PDF.
- The pipeline gracefully falls back to lightweight heuristics when optional NLP dependencies or Italian spaCy models are unavailable.
- If the LM Studio server is not reachable, the pipeline falls back to deterministic note generation.
