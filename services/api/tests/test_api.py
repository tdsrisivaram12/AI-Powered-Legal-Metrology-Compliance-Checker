from fastapi.testclient import TestClient
from uuid import uuid4
from uuid import uuid4
from uuid import uuid4

from app.main import app


client = TestClient(app)


def get_token():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "officer@legalmetrology.local",
            "password": "ChangeMe123!",
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


def auth_headers():
    return {
        "Authorization": f"Bearer {get_token()}",
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in {"healthy", "unhealthy"}


def test_login():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "officer@legalmetrology.local",
            "password": "ChangeMe123!",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["user_id"] == 1
    assert body["role"] == "Legal Metrology Officer"


def test_login_invalid_password():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "officer@legalmetrology.local",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_protected_inspections_without_token():
    assert client.get("/api/v1/inspections").status_code == 401


def test_protected_products_without_token():
    assert client.get("/api/v1/products").status_code == 401


def test_declarations_without_token():
    assert client.get("/api/v1/inspections/1/declarations").status_code == 401


def test_compliance_without_token():
    assert client.get("/api/v1/inspections/1/compliance").status_code == 401


def test_evidence_without_token():
    assert client.get("/api/v1/inspections/1/evidence").status_code == 401


def test_report_without_token():
    assert client.get("/api/v1/inspections/1/report").status_code == 401


def test_verification_without_token():
    response = client.post(
        "/api/v1/inspections/1/verification",
        json={
            "decision": "REVIEW",
            "remarks": "test",
        },
    )
    assert response.status_code == 401


def test_scan_processing_without_token():
    assert client.post(
        "/api/v1/inspections/1/scans/2/process"
    ).status_code == 401


def test_authenticated_inspection_list():
    response = client.get(
        "/api/v1/inspections",
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_product_list():
    response = client.get(
        "/api/v1/products",
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_declarations():
    response = client.get(
        "/api/v1/inspections/1/declarations",
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_authenticated_compliance():
    response = client.get(
        "/api/v1/inspections/1/compliance",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert "overall_status" in body
    assert "findings" in body


def test_authenticated_evidence():
    response = client.get(
        "/api/v1/inspections/1/evidence",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["inspection_id"] == 1
    assert "evidence" in body


def test_authenticated_report():
    response = client.get(
        "/api/v1/inspections/1/report",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["report_type"] == "Legal Metrology Inspection Report"
    assert body["inspection"]["inspection_number"] == "INS-2026-0001"


def test_verification_history():
    response = client.get(
        "/api/v1/inspections/1/verifications",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert isinstance(body, list)
    assert len(body) >= 1


def test_scan_processing():
    create_response = client.post(
        "/api/v1/inspections/1/scans",
        json={
            "image_id": 1,
            "scan_type": "label",
        },
        headers=auth_headers(),
    )

    assert create_response.status_code == 200

    scan_id = create_response.json()["id"]

    response = client.post(
        f"/api/v1/inspections/1/scans/{scan_id}/process",
        headers=auth_headers(),
    )

    assert response.status_code == 200

    body = response.json()

    assert body["scan_id"] == scan_id
    assert body["status"] == "completed"
    assert "ocr_result" in body
    assert "declarations" in body
    assert "compliance" in body
    assert "overall_status" in body["compliance"]
    assert "findings" in body["compliance"]


def test_cross_officer_scan_access_denied():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "rbac.test@legalmetrology.local",
            "password": "RBACtest123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.post(
        "/api/v1/inspections/1/scans/2/process",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_invalid_inspection_status():
    response = client.post(
        "/api/v1/inspections",
        json={
            "inspection_number": "INS-TEST-INVALID-STATUS",
            "status": "banana",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_invalid_status_transition():
    response = client.post(
        "/api/v1/inspections",
        json={
            "inspection_number": f"INS-T-LIFE-001-{uuid4().hex[:8]}",
            "status": "draft",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 201

    inspection_id = response.json()["id"]

    response = client.patch(
        f"/api/v1/inspections/{inspection_id}",
        json={
            "status": "completed",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]


def test_valid_inspection_lifecycle():
    response = client.post(
        "/api/v1/inspections",
        json={
            "inspection_number": f"INS-T-LIFE-002-{uuid4().hex[:8]}",
            "status": "draft",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 201

    inspection_id = response.json()["id"]

    for next_status in ["in_progress", "review", "completed", "closed"]:
        response = client.patch(
            f"/api/v1/inspections/{inspection_id}",
            json={"status": next_status},
            headers=auth_headers(),
        )

        assert response.status_code == 200
        assert response.json()["status"] == next_status

def get_test_officer_token():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "rbac.test@legalmetrology.local",
            "password": "RBACtest123!",
        },
    )

    assert response.status_code == 200
    return response.json()["access_token"]


def test_authenticated_pdf_report():
    response = client.get(
        "/api/v1/inspections/1/report/pdf",
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert len(response.content) > 0


def test_cross_officer_evidence_access_denied():
    token = get_test_officer_token()

    response = client.get(
        "/api/v1/inspections/1/evidence",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_cross_officer_verification_access_denied():
    token = get_test_officer_token()

    response = client.post(
        "/api/v1/inspections/1/verification",
        json={
            "decision": "REVIEW",
            "remarks": "RBAC test",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_cross_officer_report_access_denied():
    token = get_test_officer_token()

    response = client.get(
        "/api/v1/inspections/1/report",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_cross_officer_pdf_access_denied():
    token = get_test_officer_token()

    response = client.get(
        "/api/v1/inspections/1/report/pdf",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403



from uuid import uuid4




