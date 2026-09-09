from app.models.role import Role
from app.models.user import User
from app.models.product import Product
from app.models.inspection import Inspection
from app.models.inspection_image import InspectionImage
from app.models.scan import Scan
from app.models.ocr_result import OCRResult
from app.models.declaration import Declaration

__all__ = [
    "Role",
    "User",
    "Product",
    "Inspection",
    "InspectionImage",
    "Scan",
    "OCRResult",
    "Declaration",
]
from app.models.compliance_verification import ComplianceVerification
