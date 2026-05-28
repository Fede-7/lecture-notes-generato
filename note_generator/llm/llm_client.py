"""Minimal local LLM client helpers for LM Studio.

Uses LM Studio's OpenAI-compatible HTTP API and returns the assistant content
as plain text. The pipeline can still fall back to deterministic generation if
the local server is unavailable.
"""

from __future__ import annotations

from json import JSONDecodeError
import json
import os
from typing import Any
from urllib import error, request


DEFAULT_MODEL = "qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2"
DEFAULT_API_URL = "http://localhost:1234/v1"
DEFAULT_SYSTEM_PROMPT = "Sei un assistente preciso e coerente. Segui le istruzioni alla lettera."


def _models_endpoint(base_url: str) -> str:
    """Return the /models endpoint for a given base URL."""
    return base_url.rstrip("/") + "/models"


def _get_available_models(base_url: str, timeout: int = 5) -> list[str]:
    """Query LM Studio `/v1/models` and return list of model ids.

    On error returns an empty list.
    """
    url = _models_endpoint(base_url)
    req = request.Request(url, headers={"Content-Type": "application/json"}, method="GET")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            models = [m.get("id") for m in payload.get("data", []) if isinstance(m, dict) and m.get("id")]
            return models
    except Exception:
        return []


def _build_api_url(base_url: str) -> str:
    if base_url.rstrip("/").endswith("/chat/completions"):
        return base_url
    return base_url.rstrip("/") + "/chat/completions"


def _extract_content(payload: dict[str, Any]) -> str:
    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("LM Studio returned an unexpected response shape.") from exc


def generate(
    prompt: str,
    model: str = DEFAULT_MODEL,
    timeout: int = 60,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> str:
    """Generate text using LM Studio's OpenAI-compatible chat completions API."""
    api_base = base_url or os.getenv("LM_STUDIO_API_URL", DEFAULT_API_URL)
    api_url = _build_api_url(api_base)
    auth_token = api_key if api_key is not None else os.getenv("LM_STUDIO_API_KEY")

    # Build candidate model list: requested model first, then fallbacks from env
    fallback_env = os.getenv(
        "LM_STUDIO_FALLBACK_MODELS",
        ",".join([
            "qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2",
            "qwen2.5-7b-instruct-1m",
            "deepseek-coder-v2-lite-instruct",
        ]),
    )
    fallback_models = [m.strip() for m in fallback_env.split(",") if m.strip()]
    candidates = [model] + [m for m in fallback_models if m != model]

    # Query available models and prefer candidates present in LM Studio
    available = _get_available_models(api_base)
    # Make an ordered list preserving candidates order, but skip those not listed
    ordered = [c for c in candidates if (not available or c in available)]
    # If nothing matched the available list, fall back to original candidates order
    if not ordered:
        ordered = candidates

    last_exc: Exception | None = None
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    for candidate in ordered:
        payload = {
            "model": candidate,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        req = request.Request(api_url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=timeout) as resp:
                response_payload = json.loads(resp.read().decode("utf-8"))
                # If API returns an error field despite 200, treat as failure
                if isinstance(response_payload, dict) and response_payload.get("error"):
                    last_exc = RuntimeError(f"LM Studio error for model {candidate}: {response_payload.get('error')}")
                    continue
                return _extract_content(response_payload)
        except error.HTTPError as exc:
            # Read body for error details and decide whether to try next candidate
            try:
                details = exc.read().decode("utf-8", errors="replace")
            except Exception:
                details = str(exc)
            last_exc = RuntimeError(f"LM Studio returned HTTP {exc.code} for model {candidate}: {details.strip()}")
            # If the error mentions model loading or insufficient resources, try next
            if "load" in details.lower() or "resource" in details.lower() or "model loading" in details.lower():
                continue
            # otherwise break and raise
            break
        except error.URLError as exc:
            last_exc = RuntimeError(f"Unable to reach LM Studio at {api_url}: {exc.reason}")
            break
        except JSONDecodeError as exc:
            last_exc = RuntimeError("LM Studio returned invalid JSON.")
            break

    if last_exc:
        raise last_exc
    raise RuntimeError("LM Studio did not return a valid completion for any candidate model.")
