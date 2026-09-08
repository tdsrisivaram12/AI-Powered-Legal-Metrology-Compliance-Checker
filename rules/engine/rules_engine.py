"""
Public entry point for the rules service. This is what services/compliance
and services/api/app/api/v1/rules.py should import.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional

from services.rules.applicability.applicability import ProductContext, applicable_rules
from services.rules.validators.field_validators import ValidationResult, validate_field
from services.rules.versions.version_manager import VersionManager


@dataclass
class RuleEngineReport:
    product_id: str
    checked_on: date
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def violations(self) -> List[ValidationResult]:
        return [r for r in self.results if not r.passed]

    @property
    def passed(self) -> bool:
        return len(self.violations) == 0


class RulesEngine:
    def __init__(self, version_manager: Optional[VersionManager] = None):
        self.version_manager = version_manager or VersionManager()

    def evaluate(
        self,
        product_id: str,
        extracted_declaration: Dict[str, str],
        product: ProductContext,
        as_of: Optional[date] = None,
    ) -> RuleEngineReport:
        as_of = as_of or date.today()
        active = self.version_manager.active_rules(as_of)
        relevant = applicable_rules(active, product)

        results = [
            validate_field(rule, extracted_declaration.get(rule.field.value))
            for rule in relevant
        ]
        return RuleEngineReport(product_id=product_id, checked_on=as_of, results=results)


if __name__ == "__main__":
    engine = RulesEngine()
    demo_declaration = {
        "mrp": "Rs.199.00",
        "net_quantity": "500 g",
        "manufacturer_name": "",  # missing -> should violate
        "mfg_date": "13/2026",    # invalid month -> should violate
        "consumer_care": "care@example.com",
    }
    ctx = ProductContext(category="grocery", is_imported=False)
    report = engine.evaluate("PROD-001", demo_declaration, ctx)
    print(f"Passed: {report.passed}, Violations: {len(report.violations)}")
    for v in report.violations:
        print(f"  [{v.rule_id}] {v.field}: {v.reason}")
