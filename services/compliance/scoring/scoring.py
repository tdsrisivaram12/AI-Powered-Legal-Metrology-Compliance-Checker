"""
Turns a list of Findings into a 0-100 compliance score. Weights are
deliberately simple and centralized here so Member 5 (Legal + Compliance)
can tune them without touching the evaluator logic.
"""
from __future__ import annotations

from typing import List

from services.compliance.findings.findings import Finding
from services.rules.schemas.rule_schema import RuleSeverity

SEVERITY_PENALTY = {
    RuleSeverity.CRITICAL: 40,
    RuleSeverity.MAJOR: 15,
    RuleSeverity.MINOR: 5,
}


def compute_score(findings: List[Finding]) -> int:
    score = 100
    for f in findings:
        score -= SEVERITY_PENALTY.get(f.severity, 5)
    return max(score, 0)


def has_critical_finding(findings: List[Finding]) -> bool:
    return any(f.severity == RuleSeverity.CRITICAL for f in findings)
