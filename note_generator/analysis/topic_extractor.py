"""Topic extraction and lightweight hierarchical grouping."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any

from note_generator.config import DEFAULT_CONFIG, PipelineConfig
from note_generator.utils.nlp_utils import extract_keywords

try:
    from joblib import Memory
except ImportError:  # pragma: no cover - optional dependency
    Memory = None


@dataclass(frozen=True)
class TopicChunk:
    title: str
    sentences: tuple[str, ...]
    keywords: tuple[str, ...]


memory = Memory(location=DEFAULT_CONFIG.cache_dir, verbose=0) if Memory is not None else None


def _cacheable(function):
    if memory is None:
        return function
    return memory.cache(function)


def _build_title(sentences: tuple[str, ...], stopwords: set[str]) -> str:
    source = sentences[0] if sentences else "Argomento"
    keywords = extract_keywords(source, stopwords, limit=3)
    if keywords:
        return " ".join(keyword.capitalize() for keyword in keywords)
    return source[:60].strip().rstrip(".") or "Argomento"


@_cacheable
def _cached_extract_topics(sentences: tuple[str, ...], max_topics: int, sentences_per_topic: int, stopwords: tuple[str, ...]) -> dict[str, Any]:
    stopword_set = set(stopwords)
    if not sentences:
        return {"topics": {}}
    chunk_size = max(1, sentences_per_topic)
    inferred_topics = min(max_topics, ceil(len(sentences) / chunk_size))
    topics: dict[str, Any] = {}
    for index in range(inferred_topics):
        start = index * chunk_size
        chunk = tuple(sentences[start : start + chunk_size])
        if not chunk:
            continue
        title = _build_title(chunk, stopword_set)
        topic_id = f"topic_{index + 1}"
        subtopics: dict[str, Any] = {}
        for sub_index, sentence in enumerate(chunk[1:], start=1):
            keywords = extract_keywords(sentence, stopword_set, limit=2)
            if not keywords:
                continue
            subtopics[f"{topic_id}_{sub_index}"] = {
                "title": " ".join(word.capitalize() for word in keywords),
                "sentences": [sentence],
                "subtopics": {},
            }
        topics[topic_id] = {
            "title": title,
            "sentences": list(chunk),
            "keywords": extract_keywords(" ".join(chunk), stopword_set, limit=5),
            "subtopics": subtopics,
        }
    return {"topics": topics}


def extract_topics(sentences: list[str], config: PipelineConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    """Split sentences into coarse lecture topics."""

    return _cached_extract_topics(tuple(sentences), config.max_topics, config.sentences_per_topic, tuple(config.stopwords))
