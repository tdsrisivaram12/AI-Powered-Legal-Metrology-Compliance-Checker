"""
GET /api/v1/reports/{product_id}/pdf -- generates (or regenerates) the
officer-facing PDF report for a product's most recent compliance result
and streams it back. Requires POST /api/v1/compliance/evaluate to have run
first for that product_id.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from services.api.app.repositories import compliance_repo
from services.reports.generators.pdf_generator import generate_report

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/{product_id}/pdf")
def get_report_pdf(
    product_id: str,
    product_name: str = Query(default="Unnamed product"),
    inspection_id: str = Query(default=None),
    officer_name: str = Query(default="Unassigned"),
):
    result = compliance_repo.get(product_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No compliance result found for product '{product_id}'. Run /api/v1/compliance/evaluate first.")

    inspection_id = inspection_id or f"INSP-{product_id}"
    out_dir = Path(tempfile.gettempdir()) / "lm_reports"
    out_path = out_dir / f"{inspection_id}.pdf"

    generate_report(
        result=result,
        product_name=product_name,
        inspection_id=inspection_id,
        officer_name=officer_name,
        output_path=str(out_path),
    )

    return FileResponse(path=str(out_path), media_type="application/pdf", filename=f"{inspection_id}_report.pdf")
