"""Helpers for lightweight Italian NLP with graceful fallbacks."""

from __future__ import annotations

import re
from functools import lru_cache


@lru_cache(maxsize=1)
def get_nlp():
    """Return a spaCy Italian pipeline when available, else a blank sentencizer pipeline."""

    try:
        import spacy

        for model in ("it_core_news_sm", "it_core_news_md"):
            try:
                return spacy.load(model)
            except OSError:
                continue
        nlp = spacy.blank("it")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
        return nlp
    except ImportError:
        return None


def split_sentences(text: str) -> list[str]:
    """Split text into sentences using spaCy when possible."""

    nlp = get_nlp()
    if nlp is not None:
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        if sentences:
            return sentences
    return [chunk.strip() for chunk in re.split(r"(?<=[.!?])\s+", text) if chunk.strip()]


def extract_keywords(text: str, stopwords: set[str], limit: int = 4) -> list[str]:
    """Extract simple content-bearing keywords from Italian text."""

    words = re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9_-]*", text)
    keywords: list[str] = []
    seen: set[str] = set()
    for word in words:
        lowered = word.lower()
        if len(word) <= 1 or lowered in stopwords:
            continue
        if word not in seen:
            keywords.append(word)
            seen.add(word)
        if len(keywords) >= limit:
            break
    return keywords
