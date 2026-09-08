"""
A Finding is the compliance service's normalized unit of output -- one per
rule violation, enriched with severity and a human-readable message, ready
to hand to services/evidence and services/reports.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum

from services.rules.schemas.rule_schema import RuleSeverity
from services.rules.validators.field_validators import ValidationResult


class Decision(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    SUSPECTED_NON_COMPLIANCE = "SUSPECTED NON-COMPLIANCE"


@dataclass
class Finding:
    product_id: str
    rule_id: str
    field: str
    severity: RuleSeverity
    message: str
    legal_reference: str
    detected_at: datetime

    @classmethod
    def from_validation_result(
        cls,
        product_id: str,
        result: ValidationResult,
        severity: RuleSeverity,
        legal_reference: str,
    ) -> "Finding":
        return cls(
            product_id=product_id,
            rule_id=result.rule_id,
            field=result.field,
            severity=severity,
            message=result.reason,
            legal_reference=legal_reference,
            detected_at=datetime.now(timezone.utc),
        )

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "rule_id": self.rule_id,
            "field": self.field,
            "severity": self.severity.value,
            "message": self.message,
            "legal_reference": self.legal_reference,
            "detected_at": self.detected_at.isoformat(),
        }
