"""Minimal local LLM client helpers.

Tries to invoke a local Ollama CLI if available. If not present, raises
RuntimeError with instructions. The function returns raw text from the model.
"""

from __future__ import annotations

import shutil
import subprocess
from typing import Optional


def _ollama_available() -> bool:
    return shutil.which("ollama") is not None


def generate(prompt: str, model: str = "qwen3:8b", timeout: int = 60) -> str:
    """Generate text using a local Ollama CLI if present.

    Returns the model output as text. Raises RuntimeError if no supported
    local client is available.
    """
    if _ollama_available():
        cmd = ["ollama", "generate", model]
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=timeout)
        except Exception as exc:  # pragma: no cover - runtime environment dependent
            raise RuntimeError(f"Error running ollama: {exc}")
        if proc.returncode != 0:
            raise RuntimeError(f"Ollama returned non-zero exit: {proc.stderr.strip()}")
        return proc.stdout

    raise RuntimeError(
        "No local LLM client available. Install Ollama (https://ollama.com) "
        "or provide your own `generate` implementation in note_generator.llm.llm_client.generate."
    )
