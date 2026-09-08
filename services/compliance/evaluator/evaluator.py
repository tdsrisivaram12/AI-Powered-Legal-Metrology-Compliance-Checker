"""
Public entry point for the compliance service. Consumes a RuleEngineReport
(from services/rules) and produces a ComplianceResult: score, decision,
and the list of Findings that evidence/reports/dashboard consume next.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from services.compliance.findings.findings import Decision, Finding
from services.compliance.scoring.scoring import compute_score, has_critical_finding
from services.rules.engine.rules_engine import RuleEngineReport
from services.rules.versions.version_manager import VersionManager

REVIEW_THRESHOLD = 85   # score >= this and no critical -> PASS
                         # below this (or any critical) -> REVIEW / SUSPECTED


@dataclass
class ComplianceResult:
    product_id: str
    decision: Decision
    score: int
    findings: List[Finding] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "product_id": self.product_id,
            "decision": self.decision.value,
            "score": self.score,
            "findings": [f.to_dict() for f in self.findings],
        }


class ComplianceEvaluator:
    def __init__(self, version_manager: VersionManager | None = None):
        self.version_manager = version_manager or VersionManager()

    def evaluate(self, rule_report: RuleEngineReport) -> ComplianceResult:
        findings: List[Finding] = []
        for violation in rule_report.violations:
            rule = self.version_manager.get_rule(violation.rule_id)
            severity = rule.severity if rule else None
            legal_ref = rule.legal_reference if rule else "unknown"
            if severity is None:
                continue
            findings.append(
                Finding.from_validation_result(
                    product_id=rule_report.product_id,
                    result=violation,
                    severity=severity,
                    legal_reference=legal_ref,
                )
            )

        score = compute_score(findings)
        decision = self._decide(findings, score)
        return ComplianceResult(product_id=rule_report.product_id, decision=decision, score=score, findings=findings)

    @staticmethod
    def _decide(findings: List[Finding], score: int) -> Decision:
        if not findings:
            return Decision.PASS
        if has_critical_finding(findings):
            return Decision.SUSPECTED_NON_COMPLIANCE
        if score >= REVIEW_THRESHOLD:
            return Decision.PASS
        return Decision.REVIEW


if __name__ == "__main__":
    from datetime import date

    from services.rules.applicability.applicability import ProductContext
    from services.rules.engine.rules_engine import RulesEngine

    engine = RulesEngine()
    declaration = {"mrp": "", "net_quantity": "500 g", "manufacturer_name": "Acme Pvt Ltd", "mfg_date": "01/2026"}
    ctx = ProductContext(category="grocery")
    rule_report = engine.evaluate("PROD-001", declaration, ctx, as_of=date.today())

    evaluator = ComplianceEvaluator(engine.version_manager)
    result = evaluator.evaluate(rule_report)
    print(result.decision.value, result.score)
    for f in result.findings:
        print(" -", f.message)
