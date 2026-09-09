import re
from decimal import Decimal, InvalidOperation

from sqlalchemy.orm import Session

from app.models.declaration import Declaration
from app.models.ocr_result import OCRResult
from app.models.scan import Scan


class DeclarationExtractionService:

    @staticmethod
    def extract_from_scan(
        db: Session,
        scan_id: int,
    ) -> list[Declaration]:

        scan = db.get(Scan, scan_id)

        if scan is None:
            raise ValueError("Scan not found")

        ocr = (
            db.query(OCRResult)
            .filter(OCRResult.scan_id == scan_id)
            .order_by(OCRResult.id.desc())
            .first()
        )

        if ocr is None:
            raise ValueError("OCR result not found")

        text = ocr.raw_text or ""
        declarations: list[Declaration] = []

        def add_declaration(
            field_name: str,
            value_text: str,
            normalized_value: str | None = None,
            numeric_value: Decimal | None = None,
            unit: str | None = None,
            extraction_method: str = "regex",
        ) -> None:
            declarations.append(
                Declaration(
                    inspection_id=scan.inspection_id,
                    scan_id=scan.id,
                    image_id=scan.image_id,
                    field_name=field_name,
                    value_text=value_text,
                    normalized_value=normalized_value or value_text,
                    numeric_value=numeric_value,
                    unit=unit,
                    extraction_method=extraction_method,
                )
            )

        # Net quantity
        quantity_match = re.search(
            r"(?:NET\s*QUANTITY|NETQUANTITY)"
            r"\s*[:\-]?\s*"
            r"([0-9]+(?:\.[0-9]+)?)"
            r"\s*(kg|g|mg|l|ml)\b",
            text,
            re.IGNORECASE,
        )

        if quantity_match:
            value_text = quantity_match.group(1)
            unit = quantity_match.group(2).lower()

            try:
                numeric_value = Decimal(value_text)
            except InvalidOperation:
                numeric_value = None

            add_declaration(
                "net_quantity",
                f"{value_text} {unit}",
                f"{value_text} {unit}",
                numeric_value,
                unit,
                "regex",
            )

        # Batch number
        batch_match = re.search(
            r"(?:BATCH\s*NO\.?|BATCH\s*NUMBER|BN)"
            r"\s*(?:\([^)]*\))?"
            r"\s*[:\-]?\s*"
            r"([A-Z0-9][A-Z0-9\/\-_]{2,})",
            text,
            re.IGNORECASE,
        )

        if batch_match:
            candidate = batch_match.group(1).strip()

            invalid_candidates = {
                "NO",
                "NUMBER",
                "BATCH",
                "INCL",
                "TATA",
                "CONSUMER",
                "PRODUCTS",
                "LTD",
                "LIMITED",
            }

            if candidate.upper() not in invalid_candidates:
                add_declaration(
                    "batch_number",
                    candidate,
                    candidate,
                    extraction_method="regex",
                )

        # MRP
        mrp_patterns = [
            r"\bMRP\b\s*(?:RS\.?|INR)?\s*[:\-]?\s*"
            r"(?:RS\.?|INR)?\s*([0-9]+(?:\.[0-9]{1,2})?)",

            r"\bM\.R\.P\.?\b\s*(?:RS\.?|INR)?\s*[:\-]?\s*"
            r"(?:RS\.?|INR)?\s*([0-9]+(?:\.[0-9]{1,2})?)",

            r"\bMAXIMUM\s+RETAIL\s+PRICE\b\s*"
            r"(?:RS\.?|INR)?\s*[:\-]?\s*"
            r"(?:RS\.?|INR)?\s*([0-9]+(?:\.[0-9]{1,2})?)",
        ]

        for pattern in mrp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                mrp_value = match.group(1)

                try:
                    numeric_mrp = Decimal(mrp_value)

                    add_declaration(
                        "mrp",
                        f"Rs {mrp_value}",
                        mrp_value,
                        numeric_mrp,
                        "INR",
                        "regex",
                    )
                except InvalidOperation:
                    pass

                break

        # Manufacturer
        manufacturer_patterns = [
            r"TATA\s*CONSUMER\s*PRODUCTS\s*(?:LTD|LIMITED|TD)\b",
            r"TATACONSUMER\s*PRODUCTS\s*(?:LTD|LIMITED|TD)\b",
        ]

        for pattern in manufacturer_patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE,
            )

            if match:
                manufacturer = re.sub(
                    r"\s+",
                    " ",
                    match.group(0),
                ).strip()

                manufacturer = re.sub(
                    r"TATA\s*CONSUMER",
                    "TATA CONSUMER",
                    manufacturer,
                    flags=re.IGNORECASE,
                )

                manufacturer = re.sub(
                    r"\bTD\b$",
                    "LTD",
                    manufacturer,
                    flags=re.IGNORECASE,
                )

                add_declaration(
                    "manufacturer_name",
                    manufacturer,
                    manufacturer,
                    extraction_method="pattern+normalization",
                )

                break

        if declarations:
            db.add_all(declarations)
            db.commit()

            for declaration in declarations:
                db.refresh(declaration)

        return declarations
