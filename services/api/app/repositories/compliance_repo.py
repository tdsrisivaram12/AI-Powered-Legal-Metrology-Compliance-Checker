"""
In-memory store of the latest ComplianceResult per product_id. This is a
stand-in for the real Postgres-backed repository Member 3 (Backend) will
build under database/migrations + services/api/app/models; the interface
(save/get) is intentionally the only thing other routers depend on, so
swapping this for a real DB-backed repo later is a one-file change.
"""
from __future__ import annotations

from typing import Dict, Optional

from services.compliance.evaluator.evaluator import ComplianceResult

_results: Dict[str, ComplianceResult] = {}


def save(result: ComplianceResult) -> None:
    _results[result.product_id] = result


def get(product_id: str) -> Optional[ComplianceResult]:
    return _results.get(product_id)


def all_results() -> list[ComplianceResult]:
    return list(_results.values())
