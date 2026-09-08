import sys
from pathlib import Path

# allow running standalone: python -m pytest services/rules/tests
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from datetime import date

from services.rules.applicability.applicability import ProductContext
from services.rules.engine.rules_engine import RulesEngine


def test_missing_mrp_is_violation():
    engine = RulesEngine()
    declaration = {"net_quantity": "1 kg", "manufacturer_name": "Acme Pvt Ltd", "mfg_date": "01/2026"}
    ctx = ProductContext(category="grocery")
    report = engine.evaluate("P1", declaration, ctx)
    assert any(v.rule_id == "LM-MRP-001" for v in report.violations)


def test_complete_declaration_passes_core_rules():
    engine = RulesEngine()
    declaration = {
        "mrp": "Rs.99.00",
        "net_quantity": "250 g",
        "manufacturer_name": "Acme Pvt Ltd",
        "mfg_date": "03/2026",
        "consumer_care": "1800-000-000",
    }
    ctx = ProductContext(category="snacks")
    report = engine.evaluate("P2", declaration, ctx)
    core_ids = {"LM-MRP-001", "LM-NETQTY-001", "LM-MFR-001", "LM-DATE-001", "LM-CARE-001"}
    assert not (core_ids & {v.rule_id for v in report.violations})


def test_2026_country_of_origin_rule_only_applies_to_imported():
    engine = RulesEngine()
    declaration = {
        "mrp": "Rs.499.00",
        "net_quantity": "1 pcs",
        "manufacturer_name": "Global Foods Ltd",
        "mfg_date": "02/2026",
        "consumer_care": "help@example.com",
        "country_of_origin": "",
    }
    domestic_ctx = ProductContext(category="grocery", is_imported=False)
    imported_ctx = ProductContext(category="grocery", is_imported=True)

    domestic_report = engine.evaluate("P3", declaration, domestic_ctx, as_of=date(2026, 6, 1))
    imported_report = engine.evaluate("P4", declaration, imported_ctx, as_of=date(2026, 6, 1))

    assert "LM-COO-2026-001" not in {v.rule_id for v in domestic_report.violations}
    assert "LM-COO-2026-001" in {v.rule_id for v in imported_report.violations}


def test_rule_not_active_before_effective_date():
    engine = RulesEngine()
    declaration = {"country_of_origin": ""}
    ctx = ProductContext(category="grocery", is_imported=True)
    report = engine.evaluate("P5", declaration, ctx, as_of=date(2020, 1, 1))
    assert "LM-COO-2026-001" not in {r.rule_id for r in report.results}


if __name__ == "__main__":
    test_missing_mrp_is_violation()
    test_complete_declaration_passes_core_rules()
    test_2026_country_of_origin_rule_only_applies_to_imported()
    test_rule_not_active_before_effective_date()
    print("All rules engine tests passed.")
