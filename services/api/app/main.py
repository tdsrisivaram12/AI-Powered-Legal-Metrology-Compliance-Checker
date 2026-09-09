from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.auth import router as auth_router
from app.api.v1.inspections import router as inspections_router
from app.api.v1.products import router as products_router
from app.api.v1.inspection_images import router as inspection_images_router
from app.api.v1.scans import router as scans_router
from app.api.v1.declarations import router as declarations_router
from app.api.v1.compliance import router as compliance_router
from app.api.v1.evidence import router as evidence_router
from app.api.v1.verification import router as verification_router
from app.api.v1.verification_history import router as verification_history_router
from app.api.v1.reports import router as reports_router
from app.api.v1.report_pdf import router as report_pdf_router
from app.core.database import engine


app = FastAPI(
    title="AI-Powered Legal Metrology Compliance Checker",
    description="Backend API for AI-assisted packaged commodity compliance inspection.",
    version="1.0.0",
)


app.include_router(auth_router, prefix="/api/v1")
app.include_router(inspections_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(inspection_images_router, prefix="/api/v1")
app.include_router(scans_router, prefix="/api/v1")
app.include_router(declarations_router, prefix="/api/v1")
app.include_router(compliance_router, prefix="/api/v1")
app.include_router(evidence_router, prefix="/api/v1")
app.include_router(verification_router, prefix="/api/v1")
app.include_router(verification_history_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(report_pdf_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "AI-Powered Legal Metrology Compliance Checker",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(exc),
        }
