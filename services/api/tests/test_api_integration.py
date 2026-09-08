import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from services.api.app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_list_active_rules():
    resp = client.get("/api/v1/rules")
    assert resp.status_code == 200
    rule_ids = {r["rule_id"] for r in resp.json()}
    assert "LM-MRP-001" in rule_ids


def test_full_pipeline_missing_mrp_flows_through_reports_and_search():
    # 1. Evaluate compliance for a product missing its MRP
    payload = {
        "product_id": "PROD-INTEG-1",
        "declaration": {
            "mrp": "",
            "net_quantity": "500 g",
            "manufacturer_name": "Acme Pvt Ltd",
            "mfg_date": "01/2026",
            "consumer_care": "1800-000-000",
        },
        "product_context": {"category": "grocery", "is_imported": False},
        "manufacturer": "Acme Pvt Ltd",
        "notify_emails": ["inspector@example.gov.in"],
    }
    resp = client.post("/api/v1/compliance/evaluate", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["decision"] == "SUSPECTED NON-COMPLIANCE"
    assert body["notified"] is True
    assert any(f["rule_id"] == "LM-MRP-001" for f in body["findings"])

    # 2. Upload evidence for the same inspection
    files = {"file": ("front.jpg", b"fake-jpeg-bytes", "image/jpeg")}
    data = {"inspection_id": "INSP-INTEG-1", "actor": "officer_1"}
    ev_resp = client.post("/api/v1/evidence/upload", data=data, files=files)
    assert ev_resp.status_code == 200
    evidence_id = ev_resp.json()["evidence_id"]

    audit_resp = client.get(f"/api/v1/evidence/INSP-INTEG-1/{evidence_id}/audit")
    assert audit_resp.status_code == 200
    assert audit_resp.json()[0]["action"] == "CAPTURED"

    chain_resp = client.get("/api/v1/evidence/verify-chain")
    assert chain_resp.json()["valid"] is True

    # 3. Generate the PDF report for that product
    report_resp = client.get(
        "/api/v1/reports/PROD-INTEG-1/pdf",
        params={"product_name": "Test Snack Pack", "inspection_id": "INSP-INTEG-1", "officer_name": "Officer Rao"},
    )
    assert report_resp.status_code == 200
    assert report_resp.headers["content-type"] == "application/pdf"
    assert len(report_resp.content) > 0

    # 4. A second, similar product (also missing MRP) should surface in similarity search
    payload2 = dict(payload)
    payload2["product_id"] = "PROD-INTEG-2"
    client.post("/api/v1/compliance/evaluate", json=payload2)

    similar_resp = client.get("/api/v1/search/similar/PROD-INTEG-2")
    assert similar_resp.status_code == 200
    similar_ids = {c["product_id"] for c in similar_resp.json()}
    assert "PROD-INTEG-1" in similar_ids


def test_report_404_when_no_compliance_result_exists():
    resp = client.get("/api/v1/reports/UNKNOWN-PRODUCT/pdf")
    assert resp.status_code == 404


if __name__ == "__main__":
    test_health()
    test_list_active_rules()
    test_full_pipeline_missing_mrp_flows_through_reports_and_search()
    test_report_404_when_no_compliance_result_exists()
    print("All API integration tests passed.")
