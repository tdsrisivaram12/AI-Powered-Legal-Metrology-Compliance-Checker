from dataclasses import asdict

from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.services.legal_rule_registry import get_applicable_rules
from app.services.product_classification_service import ProductClassificationService


class RuleApplicabilityService:

    @staticmethod
    def get_rules_for_inspection(
        db: Session,
        inspection_id: int,
    ) -> dict:

        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise ValueError("Inspection not found")

        classification = (
            ProductClassificationService.classify_inspection(
                db,
                inspection_id,
            )
        )

        category = classification["category"]

        if not category or category == "unknown":
            return {
                "inspection_id": inspection_id,
                "category": category,
                "rules": [],
                "rule_count": 0,
                "status": "REVIEW",
                "reason": "Product category could not be determined",
            }

        rules = get_applicable_rules(category)

        return {
            "inspection_id": inspection_id,
            "category": category,
            "rules": [asdict(rule) for rule in rules],
            "rule_count": len(rules),
            "status": "READY" if rules else "REVIEW",
            "reason": (
                None
                if rules
                else "No rules registered for this category"
            ),
        }
