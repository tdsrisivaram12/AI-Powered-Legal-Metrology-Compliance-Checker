"""
GET /api/v1/rules -- browse the active legal rule set. Used by the frontend's
rules/ page and by other services that want a human-readable rule catalog.
"""
from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Query

from services.api.app.core.dependencies import version_manager
from services.api.app.schemas.compliance import RuleOut

router = APIRouter(prefix="/api/v1/rules", tags=["rules"])


@router.get("", response_model=List[RuleOut])
def list_active_rules(as_of: Optional[date] = Query(default=None)):
    rules = version_manager.active_rules(as_of)
    return [
        RuleOut(
            rule_id=r.rule_id,
            title=r.title,
            field=r.field.value,
            severity=r.severity.value,
            legal_reference=r.legal_reference,
            version=r.version,
            required=r.required,
        )
        for r in rules
    ]


@router.get("/{rule_id}", response_model=RuleOut)
def get_rule(rule_id: str):
    from fastapi import HTTPException

    rule = version_manager.get_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail=f"Rule '{rule_id}' not found")
    return RuleOut(
        rule_id=rule.rule_id,
        title=rule.title,
        field=rule.field.value,
        severity=rule.severity.value,
        legal_reference=rule.legal_reference,
        version=rule.version,
        required=rule.required,
    )
