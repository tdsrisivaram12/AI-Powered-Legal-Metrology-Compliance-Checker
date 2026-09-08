"""
Non-PDF export formats for compliance results: JSON (for the API/dashboard)
and CSV (for bulk officer review / spreadsheets).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List

from services.compliance.evaluator.evaluator import ComplianceResult


def export_json(result: ComplianceResult, output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, indent=2)
    return output_path


def export_csv(results: List[ComplianceResult], output_path: str) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["product_id", "decision", "score", "rule_id", "field", "severity", "message", "legal_reference"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            if not result.findings:
                writer.writerow({
                    "product_id": result.product_id, "decision": result.decision.value,
                    "score": result.score, "rule_id": "", "field": "", "severity": "",
                    "message": "", "legal_reference": "",
                })
            for finding in result.findings:
                writer.writerow({
                    "product_id": result.product_id,
                    "decision": result.decision.value,
                    "score": result.score,
                    "rule_id": finding.rule_id,
                    "field": finding.field,
                    "severity": finding.severity.value,
                    "message": finding.message,
                    "legal_reference": finding.legal_reference,
                })
    return output_path
