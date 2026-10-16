"""Topic loading, filtering, and TF-IDF content-based recommendations."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any

_PACKAGE_DIR = Path(__file__).resolve().parent
_TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]+")


def tokenize(text: str) -> list[str]:
    """Return lowercase alphanumeric tokens from text."""
    return _TOKEN_PATTERN.findall(text.casefold())


@lru_cache(maxsize=1)
def load_topics() -> tuple[dict[str, Any], ...]:
    """Load the bundled topic catalogue."""
    topics_path = _PACKAGE_DIR / "topics.json"
    with topics_path.open(encoding="utf-8") as topic_file:
        topics = json.load(topic_file)

    if not isinstance(topics, list):
        raise ValueError("The topic catalogue must contain a JSON array.")

    return tuple(topics)


def filter_topics(domain: str | None = None) -> list[dict[str, Any]]:
    """Return all topics, optionally filtered by domain."""
    topics = load_topics()

    if not domain:
        return [dict(topic) for topic in topics]

    normalized_domain = domain.strip().casefold()
    return [
        dict(topic)
        for topic in topics
        if topic["domain"].casefold() == normalized_domain
    ]


def _topic_text(topic: dict[str, Any]) -> str:
    """Combine searchable fields into one document."""
    fields = [
        topic["title"],
        topic["domain"],
        topic["summary"],
        topic["level"],
        *topic["methods"],
        *topic["datasets"],
        *topic["keywords"],
    ]
    return " ".join(fields)


def recommend_topics(
    interests: str,
    limit: int = 5,
    domain: str | None = None,
) -> list[dict[str, Any]]:
    """Rank topics by cosine similarity between TF-IDF vectors."""
    query_tokens = tokenize(interests)
    if not query_tokens:
        return []

    topics = filter_topics(domain)
    if not topics:
        return []

    documents = [tokenize(_topic_text(topic)) for topic in topics]
    document_frequency: Counter[str] = Counter()
    for document in documents:
        document_frequency.update(set(document))

    document_count = len(documents)
    idf = {
        term: math.log((document_count + 1) / (count + 1)) + 1
        for term, count in document_frequency.items()
    }

    query_counts = Counter(query_tokens)
    query_vector = {
        term: count * idf.get(term, 0.0)
        for term, count in query_counts.items()
        if term in idf
    }

    if not query_vector:
        return []

    query_norm = math.sqrt(sum(weight * weight for weight in query_vector.values()))
    ranked: list[dict[str, Any]] = []

    for topic, document in zip(topics, documents):
        term_counts = Counter(document)
        document_length = max(len(document), 1)
        document_vector = {
            term: (count / document_length) * idf[term]
            for term, count in term_counts.items()
            if term in idf
        }
        document_norm = math.sqrt(
            sum(weight * weight for weight in document_vector.values())
        )

        dot_product = sum(
            weight * document_vector.get(term, 0.0)
            for term, weight in query_vector.items()
        )
        score = (
            dot_product / (query_norm * document_norm)
            if query_norm and document_norm
            else 0.0
        )

        if score > 0:
            ranked.append({**topic, "score": round(score, 4)})

    ranked.sort(key=lambda topic: topic["score"], reverse=True)
    return ranked[: max(1, limit)]
