import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from services.compliance.evaluator.evaluator import ComplianceEvaluator
from services.compliance.findings.findings import Decision
from services.rules.applicability.applicability import ProductContext
from services.rules.engine.rules_engine import RulesEngine


def _run(declaration, category="grocery", is_imported=False, as_of=None):
    engine = RulesEngine()
    ctx = ProductContext(category=category, is_imported=is_imported)
    rule_report = engine.evaluate("P", declaration, ctx, as_of=as_of or date.today())
    return ComplianceEvaluator(engine.version_manager).evaluate(rule_report)


def test_complete_declaration_is_pass():
    result = _run({
        "mrp": "Rs.99.00", "net_quantity": "250 g", "manufacturer_name": "Acme",
        "mfg_date": "03/2026", "consumer_care": "1800-000-000",
    })
    assert result.decision == Decision.PASS
    assert result.score == 100


def test_missing_mrp_is_suspected_non_compliance():
    result = _run({
        "mrp": "", "net_quantity": "250 g", "manufacturer_name": "Acme",
        "mfg_date": "03/2026", "consumer_care": "1800-000-000",
    })
    assert result.decision == Decision.SUSPECTED_NON_COMPLIANCE


def test_minor_only_violation_can_still_pass_or_review():
    result = _run({
        "mrp": "Rs.99.00", "net_quantity": "250 g", "manufacturer_name": "Acme",
        "mfg_date": "03/2026", "consumer_care": "",  # minor, required -> -5
    })
    assert result.decision in (Decision.PASS, Decision.REVIEW)
    assert result.score == 95


if __name__ == "__main__":
    test_complete_declaration_is_pass()
    test_missing_mrp_is_suspected_non_compliance()
    test_minor_only_violation_can_still_pass_or_review()
    print("All compliance tests passed.")
