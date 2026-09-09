from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from app.services.inspection_report_service import InspectionReportService


REPORT_DIR = (
    Path(__file__).resolve().parents[2]
    / "storage"
    / "reports"
)


class InspectionPDFService:

    @staticmethod
    def generate_pdf(
        db,
        inspection_id: int,
    ) -> Path:

        report = InspectionReportService.generate_report(
            db,
            inspection_id,
        )

        REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        inspection_number = report["inspection"]["inspection_number"]

        output_path = REPORT_DIR / (
            f"{inspection_number}_inspection_report.pdf"
        )

        styles = getSampleStyleSheet()

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            title="Legal Metrology Inspection Report",
        )

        story = []

        story.append(
            Paragraph(
                "LEGAL METROLOGY INSPECTION REPORT",
                styles["Title"],
            )
        )

        story.append(Spacer(1, 8))

        inspection = report["inspection"]
        product = report["product"]
        compliance = report["compliance"]

        inspection_table = Table(
            [
                ["Inspection Number", inspection["inspection_number"]],
                ["Officer ID", str(inspection["officer_id"])],
                ["Status", inspection["status"]],
                ["Compliance Status", compliance["overall_status"]],
            ],
            colWidths=[55 * mm, 115 * mm],
        )

        inspection_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ]
            )
        )

        story.append(
            Paragraph(
                "Inspection Details",
                styles["Heading2"],
            )
        )

        story.append(inspection_table)
        story.append(Spacer(1, 10))

        if product is not None:
            story.append(
                Paragraph(
                    "Product Details",
                    styles["Heading2"],
                )
            )

            product_table = Table(
                [
                    ["Product", product["product_name"] or "-"],
                    ["Brand", product["brand_name"] or "-"],
                    ["Category", product["category"] or "-"],
                    [
                        "Manufacturer",
                        product["manufacturer_name"] or "-",
                    ],
                    [
                        "Manufacturer Address",
                        product["manufacturer_address"] or "-",
                    ],
                    [
                        "Country of Origin",
                        product["country_of_origin"] or "-",
                    ],
                    ["Barcode", product["barcode"] or "-"],
                ],
                colWidths=[55 * mm, 115 * mm],
            )

            product_table.setStyle(
                TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.lightgrey,
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (0, -1),
                            "Helvetica-Bold",
                        ),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )

            story.append(product_table)
            story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "Extracted Declarations",
                styles["Heading2"],
            )
        )

        declaration_rows = [
            ["Field", "Value", "Method"]
        ]

        for declaration in report["declarations"]:
            declaration_rows.append(
                [
                    declaration["field_name"],
                    declaration["value"] or "-",
                    declaration["extraction_method"] or "-",
                ]
            )

        declaration_table = Table(
            declaration_rows,
            colWidths=[50 * mm, 70 * mm, 50 * mm],
        )

        declaration_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )

        story.append(declaration_table)
        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "Compliance Findings",
                styles["Heading2"],
            )
        )

        finding_rows = [
            ["Rule", "Status", "Value", "Reason"]
        ]

        for finding in compliance["findings"]:
            finding_rows.append(
                [
                    finding["rule_id"],
                    finding["status"],
                    finding["value"] or "-",
                    finding["reason"],
                ]
            )

        finding_table = Table(
            finding_rows,
            colWidths=[35 * mm, 30 * mm, 35 * mm, 70 * mm],
            repeatRows=1,
        )

        finding_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )

        story.append(finding_table)
        story.append(Spacer(1, 10))

        story.append(
            Paragraph(
                "Officer Verification",
                styles["Heading2"],
            )
        )

        verification_rows = [
            ["Officer", "Decision", "Remarks"]
        ]

        for verification in report["officer_verifications"]:
            verification_rows.append(
                [
                    str(verification["officer_id"]),
                    verification["decision"],
                    verification["remarks"] or "-",
                ]
            )

        verification_table = Table(
            verification_rows,
            colWidths=[30 * mm, 35 * mm, 105 * mm],
        )

        verification_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )

        story.append(verification_table)
        story.append(Spacer(1, 12))

        story.append(
            Paragraph(
                compliance["disclaimer"],
                styles["Normal"],
            )
        )

        document.build(story)

        return output_path
