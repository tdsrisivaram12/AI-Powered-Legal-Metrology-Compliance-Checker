from app.core.database import SessionLocal
from app.models.declaration import Declaration
from app.services.rule_applicability_service import RuleApplicabilityService


class ComplianceEvaluator:

    @staticmethod
    def evaluate_inspection(
        db,
        inspection_id: int,
    ) -> dict:

        applicable = RuleApplicabilityService.get_rules_for_inspection(
            db,
            inspection_id,
        )

        rules = applicable["rules"]

        declarations = (
            db.query(Declaration)
            .filter(Declaration.inspection_id == inspection_id)
            .order_by(Declaration.id)
            .all()
        )

        declaration_map = {}

        for declaration in declarations:
            declaration_map.setdefault(
                declaration.field_name,
                declaration,
            )

        findings = []

        for rule in rules:
            field = rule["parameters"].get("field")
            declaration = declaration_map.get(field)

            if declaration is not None and declaration.value_text:
                status = "PASS"
                reason = "Required declaration was extracted."
            else:
                status = "REVIEW"
                reason = "Required declaration was not reliably extracted."

            findings.append(
                {
                    "rule_id": rule["rule_id"],
                    "rule_name": rule["rule_name"],
                    "field": field,
                    "status": status,
                    "reason": reason,
                    "value": (
                        declaration.value_text
                        if declaration is not None
                        else None
                    ),
                    "source": rule["source"],
                    "source_version": rule["source_version"],
                }
            )

        statuses = [finding["status"] for finding in findings]

        if not findings:
            overall_status = "REVIEW"
        elif "SUSPECTED_NON_COMPLIANCE" in statuses:
            overall_status = "SUSPECTED_NON_COMPLIANCE"
        elif "REVIEW" in statuses:
            overall_status = "REVIEW"
        else:
            overall_status = "PASS"

        return {
            "inspection_id": inspection_id,
            "category": applicable["category"],
            "overall_status": overall_status,
            "rule_count": len(findings),
            "findings": findings,
            "disclaimer": (
                "AI-assisted screening result. "
                "Final legal determination requires officer verification."
            ),
        }
