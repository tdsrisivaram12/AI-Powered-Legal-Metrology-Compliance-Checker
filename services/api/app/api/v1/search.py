"""
GET /api/v1/search/similar/{product_id} -- surfaces past products with a
similar violation pattern, so an officer reviewing a REVIEW/SUSPECTED case
can quickly check "has this manufacturer done this before".
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Query

from services.api.app.repositories import compliance_repo
from services.api.app.schemas.compliance import SimilarCaseOut
from services.api.app.core.dependencies import violation_history

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.get("/similar/{product_id}", response_model=List[SimilarCaseOut])
def find_similar(product_id: str, top_k: int = Query(default=5, ge=1, le=20)):
    result = compliance_repo.get(product_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No compliance result found for product '{product_id}'.")

    similar = violation_history.find_similar(result, top_k=top_k)
    return [
        SimilarCaseOut(product_id=c.product_id, score=c.score, decision=c.decision, manufacturer=c.manufacturer)
        for c in similar
    ]
