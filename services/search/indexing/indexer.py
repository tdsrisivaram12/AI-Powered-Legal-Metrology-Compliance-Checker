"""
Lightweight in-memory search index over products and past inspections, so
services/api/app/api/v1 can offer "find similar/previous violations for this
manufacturer" without standing up Elasticsearch for the MVP. Swappable for
a real search backend later behind the same `search()` interface.
"""
from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List


TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text.lower())


@dataclass
class IndexedDocument:
    doc_id: str
    text: str
    metadata: dict = field(default_factory=dict)


class SearchIndex:
    """A minimal TF-IDF index. Good for thousands of docs; not for millions."""

    def __init__(self):
        self._docs: Dict[str, IndexedDocument] = {}
        self._term_freqs: Dict[str, Counter] = {}
        self._doc_freq: Counter = Counter()

    def add(self, doc_id: str, text: str, metadata: dict | None = None) -> None:
        tokens = tokenize(text)
        self._docs[doc_id] = IndexedDocument(doc_id, text, metadata or {})
        tf = Counter(tokens)
        self._term_freqs[doc_id] = tf
        for term in tf.keys():
            self._doc_freq[term] += 1

    def remove(self, doc_id: str) -> None:
        tf = self._term_freqs.pop(doc_id, None)
        self._docs.pop(doc_id, None)
        if tf:
            for term in tf:
                self._doc_freq[term] -= 1

    def _idf(self, term: str) -> float:
        n = len(self._docs) or 1
        df = self._doc_freq.get(term, 0)
        return math.log((n + 1) / (df + 1)) + 1

    def _vector(self, tf: Counter) -> Dict[str, float]:
        return {term: count * self._idf(term) for term, count in tf.items()}

    def search(self, query: str, top_k: int = 5) -> List[tuple[str, float]]:
        query_tf = Counter(tokenize(query))
        query_vec = self._vector(query_tf)
        q_norm = math.sqrt(sum(v * v for v in query_vec.values())) or 1.0

        scores = []
        for doc_id, tf in self._term_freqs.items():
            doc_vec = self._vector(tf)
            dot = sum(query_vec.get(t, 0.0) * w for t, w in doc_vec.items())
            d_norm = math.sqrt(sum(v * v for v in doc_vec.values())) or 1.0
            score = dot / (q_norm * d_norm)
            if score > 0:
                scores.append((doc_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def get(self, doc_id: str) -> IndexedDocument | None:
        return self._docs.get(doc_id)
