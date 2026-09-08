import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from services.compliance.evaluator.evaluator import ComplianceEvaluator
from services.rules.applicability.applicability import ProductContext
from services.rules.engine.rules_engine import RulesEngine
from services.search.indexing.indexer import SearchIndex
from services.search.similarity.similarity import ViolationHistoryIndex


def _evaluate(product_id, missing_field):
    engine = RulesEngine()
    declaration = {
        "mrp": "Rs.99.00", "net_quantity": "500 g", "manufacturer_name": "Acme",
        "mfg_date": "01/2026", "consumer_care": "1800-000-000",
    }
    declaration[missing_field] = ""
    ctx = ProductContext(category="grocery")
    rule_report = engine.evaluate(product_id, declaration, ctx, as_of=date.today())
    return ComplianceEvaluator(engine.version_manager).evaluate(rule_report)


def test_basic_tfidf_search_ranks_relevant_doc_first():
    idx = SearchIndex()
    idx.add("doc1", "missing MRP declaration violation")
    idx.add("doc2", "manufacturer address incomplete")
    idx.add("doc3", "expired product date issue")

    results = idx.search("MRP violation")
    assert results[0][0] == "doc1"


def test_similar_case_finder_surfaces_same_violation_type():
    history = ViolationHistoryIndex()
    r1 = _evaluate("PROD-A", "mrp")
    r2 = _evaluate("PROD-B", "mrp")
    r3 = _evaluate("PROD-C", "manufacturer_name")

    history.index_result(r1, manufacturer="Acme")
    history.index_result(r3, manufacturer="Globex")

    similar = history.find_similar(r2, top_k=5)
    assert any(c.product_id == "PROD-A" for c in similar)


if __name__ == "__main__":
    test_basic_tfidf_search_ranks_relevant_doc_first()
    test_similar_case_finder_surfaces_same_violation_type()
    print("All search tests passed.")
