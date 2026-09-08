import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from datetime import date

from services.compliance.evaluator.evaluator import ComplianceEvaluator
from services.reports.exporters.exporter import export_csv, export_json
from services.reports.generators.pdf_generator import generate_report
from services.rules.applicability.applicability import ProductContext
from services.rules.engine.rules_engine import RulesEngine


def _sample_result(product_id="P1"):
    engine = RulesEngine()
    declaration = {
        "mrp": "", "net_quantity": "500 g", "manufacturer_name": "Acme",
        "mfg_date": "01/2026", "consumer_care": "1800-000-000",
    }
    ctx = ProductContext(category="grocery")
    rule_report = engine.evaluate(product_id, declaration, ctx, as_of=date.today())
    return ComplianceEvaluator(engine.version_manager).evaluate(rule_report)


def test_pdf_report_is_created():
    result = _sample_result()
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.pdf"
        path = generate_report(result, "Test Snack Pack", "INSP-100", "Officer Rao", str(out))
        assert Path(path).exists()
        assert Path(path).stat().st_size > 0


def test_json_export():
    result = _sample_result()
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "result.json"
        path = export_json(result, str(out))
        content = Path(path).read_text()
        assert "SUSPECTED NON-COMPLIANCE" in content


def test_csv_export():
    results = [_sample_result("P1"), _sample_result("P2")]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "results.csv"
        path = export_csv(results, str(out))
        rows = Path(path).read_text().splitlines()
        assert len(rows) > 1  # header + data


if __name__ == "__main__":
    test_pdf_report_is_created()
    test_json_export()
    test_csv_export()
    print("All reports tests passed.")
