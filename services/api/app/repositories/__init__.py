from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.inspection_repository import InspectionRepository
from app.repositories.inspection_image_repository import InspectionImageRepository
from app.repositories.scan_repository import ScanRepository
from app.repositories.ocr_result_repository import OCRResultRepository
from app.repositories.declaration_repository import DeclarationRepository

__all__ = [
    "RoleRepository",
    "UserRepository",
    "ProductRepository",
    "InspectionRepository",
    "InspectionImageRepository",
    "ScanRepository",
    "OCRResultRepository",
    "DeclarationRepository",
]