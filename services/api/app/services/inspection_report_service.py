from sqlalchemy.orm import Session

from app.models.compliance_verification import ComplianceVerification
from app.models.declaration import Declaration
from app.models.inspection import Inspection
from app.models.product import Product
from app.services.compliance_evaluator import ComplianceEvaluator


class InspectionReportService:

    @staticmethod
    def generate_report(
        db: Session,
        inspection_id: int,
    ) -> dict:

        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise ValueError("Inspection not found")

        product = None

        if inspection.product_id is not None:
            product = db.get(Product, inspection.product_id)

        declarations = (
            db.query(Declaration)
            .filter(
                Declaration.inspection_id == inspection_id
            )
            .order_by(Declaration.id)
            .all()
        )

        verifications = (
            db.query(ComplianceVerification)
            .filter(
                ComplianceVerification.inspection_id == inspection_id
            )
            .order_by(ComplianceVerification.id.desc())
            .all()
        )

        compliance = ComplianceEvaluator.evaluate_inspection(
            db,
            inspection_id,
        )

        return {
            "report_type": "Legal Metrology Inspection Report",
            "inspection": {
                "id": inspection.id,
                "inspection_number": inspection.inspection_number,
                "officer_id": inspection.officer_id,
                "status": inspection.status,
                "notes": inspection.notes,
                "started_at": inspection.started_at,
                "completed_at": inspection.completed_at,
            },
            "product": (
                {
                    "id": product.id,
                    "product_name": product.product_name,
                    "brand_name": product.brand_name,
                    "category": product.category,
                    "manufacturer_name": product.manufacturer_name,
                    "manufacturer_address": product.manufacturer_address,
                    "country_of_origin": product.country_of_origin,
                    "barcode": product.barcode,
                }
                if product is not None
                else None
            ),
            "declarations": [
                {
                    "id": d.id,
                    "field_name": d.field_name,
                    "value": d.value_text,
                    "normalized_value": d.normalized_value,
                    "unit": d.unit,
                    "confidence": (
                        float(d.confidence)
                        if d.confidence is not None
                        else None
                    ),
                    "extraction_method": d.extraction_method,
                }
                for d in declarations
            ],
            "compliance": compliance,
            "officer_verifications": [
                {
                    "id": v.id,
                    "officer_id": v.officer_id,
                    "decision": v.decision,
                    "remarks": v.remarks,
                    "verified_at": v.verified_at,
                }
                for v in verifications
            ],
        }
