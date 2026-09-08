"""
Generates the officer-facing PDF inspection report from a ComplianceResult.
Uses fpdf2 (pure-python, no system deps) so it runs the same in Docker as
on a dev machine.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from services.compliance.evaluator.evaluator import ComplianceResult
from services.compliance.findings.findings import Decision

DECISION_COLORS = {
    Decision.PASS: (39, 174, 96),
    Decision.REVIEW: (243, 156, 18),
    Decision.SUSPECTED_NON_COMPLIANCE: (192, 57, 43),
}


class InspectionReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Legal Metrology Compliance Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def generate_report(
    result: ComplianceResult,
    product_name: str,
    inspection_id: str,
    officer_name: str,
    output_path: Optional[str] = None,
) -> str:
    pdf = InspectionReportPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, f"Inspection ID: {inspection_id}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"Product: {product_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"Officer: {officer_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    color = DECISION_COLORS.get(result.decision, (0, 0, 0))
    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 12, f"  Decision: {result.decision.value}   |   Score: {result.score}/100", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Findings ({len(result.findings)})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)

    if not result.findings:
        pdf.cell(0, 8, "No violations detected.", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        for f in result.findings:
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "B", 10)
            pdf.multi_cell(0, 6, f"[{f.severity.value.upper()}] {f.rule_id} - {f.field}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, f"  {f.message}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_x(pdf.l_margin)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 6, f"  Ref: {f.legal_reference}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

    if output_path is None:
        output_path = f"{inspection_id}_report.pdf"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    pdf.output(output_path)
    return output_path
