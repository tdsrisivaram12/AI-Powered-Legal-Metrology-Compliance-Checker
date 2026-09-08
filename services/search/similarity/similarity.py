"""
Higher-level helpers built on top of SearchIndex specific to this domain:
finding manufacturers/products with a similar violation history, so an
officer reviewing "REVIEW" or "SUSPECTED NON-COMPLIANCE" cases can quickly
see related past cases.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from services.compliance.evaluator.evaluator import ComplianceResult
from services.search.indexing.indexer import SearchIndex


@dataclass
class SimilarCase:
    product_id: str
    score: float
    decision: str
    manufacturer: str | None = None


class ViolationHistoryIndex:
    def __init__(self):
        self.index = SearchIndex()

    def index_result(self, result: ComplianceResult, manufacturer: str | None = None) -> None:
        # Build a searchable text blob from rule ids, fields, and messages.
        text_parts = [result.decision.value]
        for f in result.findings:
            text_parts.extend([f.rule_id, f.field, f.message])
        text = " ".join(text_parts)

        self.index.add(
            doc_id=result.product_id,
            text=text,
            metadata={"decision": result.decision.value, "manufacturer": manufacturer},
        )

    def find_similar(self, result: ComplianceResult, top_k: int = 5) -> List[SimilarCase]:
        query = " ".join([f.rule_id for f in result.findings] + [f.field for f in result.findings])
        if not query.strip():
            return []

        hits = self.index.search(query, top_k=top_k + 1)  # +1 in case the doc matches itself
        cases = []
        for doc_id, score in hits:
            if doc_id == result.product_id:
                continue
            doc = self.index.get(doc_id)
            cases.append(SimilarCase(
                product_id=doc_id,
                score=round(score, 4),
                decision=doc.metadata.get("decision", "UNKNOWN") if doc else "UNKNOWN",
                manufacturer=doc.metadata.get("manufacturer") if doc else None,
            ))
        return cases[:top_k]
