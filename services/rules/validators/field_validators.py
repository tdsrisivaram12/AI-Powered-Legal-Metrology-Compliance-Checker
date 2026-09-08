"""
Validates a single extracted declaration field (from OCR/extraction) against
its corresponding Rule. Returns a ValidationResult, never raises on bad data
-- bad/missing data is exactly what we're trying to detect.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Optional

from services.rules.schemas.rule_schema import Rule


@dataclass
class ValidationResult:
    rule_id: str
    field: str
    passed: bool
    reason: str
    extracted_value: Optional[str] = None


def validate_field(rule: Rule, extracted_value: Optional[Any]) -> ValidationResult:
    value = None if extracted_value is None else str(extracted_value).strip()

    # Missing required field
    if rule.required and not value:
        return ValidationResult(
            rule_id=rule.rule_id,
            field=rule.field.value,
            passed=False,
            reason=f"Required field '{rule.field.value}' was not declared on the package.",
            extracted_value=value,
        )

    if not value:
        # Not required and absent -> passes (nothing to check)
        return ValidationResult(rule.rule_id, rule.field.value, True, "Not required; not present.", value)

    # Regex-based format validation
    if rule.validation_regex:
        if re.match(rule.validation_regex, value, flags=re.IGNORECASE):
            return ValidationResult(rule.rule_id, rule.field.value, True, "Matches required format.", value)
        return ValidationResult(
            rule_id=rule.rule_id,
            field=rule.field.value,
            passed=False,
            reason=f"Value '{value}' does not match required format for {rule.field.value}.",
            extracted_value=value,
        )

    # No regex defined -> presence check only
    return ValidationResult(rule.rule_id, rule.field.value, True, "Present; no format rule defined.", value)
