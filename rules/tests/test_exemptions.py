import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from services.compliance.evaluator.evaluator import ComplianceEvaluator
from services.compliance.findings.findings import Decision
from services.rules.applicability.applicability import ProductContext
from services.rules.engine.rules_engine import RulesEngine


def _run(declaration, category, extra_categories=None, is_imported=False, as_of=None):
    engine = RulesEngine()
    ctx = ProductContext(category=category, is_imported=is_imported, extra_categories=extra_categories or [])
    rule_report = engine.evaluate("P", declaration, ctx, as_of=as_of or date.today())
    return ComplianceEvaluator(engine.version_manager).evaluate(rule_report), rule_report


def test_institutional_package_is_exempt_from_core_declarations():
    # An institutional/industrial package with NO consumer declarations at all
    # should not be flagged for missing MRP/net qty/mfg date/consumer care --
    # Rule 3 exempts these -- but it MUST carry 'not for retail sale'.
    result, report = _run(
        declaration={"not_for_retail_sale": ""},
        category="bulk_chemicals",
        extra_categories=["institutional"],
    )
    core_ids = {"LM-MRP-001", "LM-NETQTY-001", "LM-MFR-001", "LM-DATE-001", "LM-CARE-001"}
    violated_ids = {f.rule_id for f in result.findings}
    assert not (core_ids & violated_ids)
    assert "LM-NRS-001" in violated_ids  # missing the required marking


def test_institutional_package_with_nrs_marking_passes():
    result, _ = _run(
        declaration={"not_for_retail_sale": "Not for retail sale"},
        category="bulk_chemicals",
        extra_categories=["institutional"],
    )
    assert result.decision == Decision.PASS


def test_garment_loose_exempt_from_net_qty_and_consumer_care_but_needs_mrp():
    result, _ = _run(
        declaration={"manufacturer_name": "Acme Apparel"},  # MRP missing on purpose
        category="apparel",
        extra_categories=["garment_loose"],
    )
    violated_ids = {f.rule_id for f in result.findings}
    assert "LM-NETQTY-001" not in violated_ids
    assert "LM-CARE-001" not in violated_ids
    assert "LM-DATE-001" not in violated_ids
    assert "LM-GARMENT-MRP-2023-001" in violated_ids  # MRP still required for garments


def test_garment_loose_with_mrp_and_manufacturer_passes():
    result, _ = _run(
        declaration={"manufacturer_name": "Acme Apparel", "mrp": "Rs.499.00"},
        category="apparel",
        extra_categories=["garment_loose"],
    )
    assert result.decision == Decision.PASS


def test_de_minimis_package_is_exempt_from_all_core_declarations():
    result, _ = _run(
        declaration={},
        category="snacks",
        extra_categories=["de_minimis_package"],
    )
    assert result.decision == Decision.PASS


def test_ordinary_retail_grocery_still_fully_regulated():
    # Sanity check: exemptions must not leak into ordinary retail products.
    result, _ = _run(declaration={}, category="grocery")
    core_ids = {"LM-MRP-001", "LM-NETQTY-001", "LM-MFR-001", "LM-DATE-001", "LM-CARE-001"}
    violated_ids = {f.rule_id for f in result.findings}
    assert core_ids <= violated_ids


if __name__ == "__main__":
    test_institutional_package_is_exempt_from_core_declarations()
    test_institutional_package_with_nrs_marking_passes()
    test_garment_loose_exempt_from_net_qty_and_consumer_care_but_needs_mrp()
    test_garment_loose_with_mrp_and_manufacturer_passes()
    test_de_minimis_package_is_exempt_from_all_core_declarations()
    test_ordinary_retail_grocery_still_fully_regulated()
    print("All exemption tests passed.")
