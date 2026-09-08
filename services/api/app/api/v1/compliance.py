"""
POST /api/v1/compliance/evaluate -- the core endpoint. Runs a declaration
through the rules engine + compliance evaluator, indexes the result for
similarity search, and fires a notification when the outcome needs
attention. This is what services/ai's pipeline calls after OCR/extraction.
"""
from __future__ import annotations

from fastapi import APIRouter

from services.api.app.core.dependencies import (
    compliance_evaluator,
    email_sender,
    rules_engine,
    violation_history,
)
from services.api.app.repositories import compliance_repo
from services.api.app.schemas.compliance import ComplianceResultOut, EvaluateComplianceIn, FindingOut
from services.compliance.findings.findings import Decision
from services.rules.applicability.applicability import ProductContext

router = APIRouter(prefix="/api/v1/compliance", tags=["compliance"])


@router.post("/evaluate", response_model=ComplianceResultOut)
def evaluate_compliance(payload: EvaluateComplianceIn):
    ctx = ProductContext(
        category=payload.product_context.category,
        is_packaged_for_retail_sale=payload.product_context.is_packaged_for_retail_sale,
        is_imported=payload.product_context.is_imported,
        extra_categories=payload.product_context.extra_categories,
    )

    rule_report = rules_engine.evaluate(
        product_id=payload.product_id,
        extracted_declaration=payload.declaration.to_dict(),
        product=ctx,
        as_of=payload.as_of,
    )
    result = compliance_evaluator.evaluate(rule_report)
    compliance_repo.save(result)

    # index for "similar past cases" search
    violation_history.index_result(result, manufacturer=payload.manufacturer)

    # notify if the outcome needs officer attention
    notified = False
    if result.decision in (Decision.REVIEW, Decision.SUSPECTED_NON_COMPLIANCE) and payload.notify_emails:
        email_sender.send_violation_alert(
            to=payload.notify_emails,
            product_id=result.product_id,
            decision=result.decision.value,
            findings_count=len(result.findings),
        )
        notified = True

    return ComplianceResultOut(
        product_id=result.product_id,
        decision=result.decision.value,
        score=result.score,
        findings=[
            FindingOut(
                rule_id=f.rule_id, field=f.field, severity=f.severity.value,
                message=f.message, legal_reference=f.legal_reference,
            )
            for f in result.findings
        ],
        notified=notified,
    )
