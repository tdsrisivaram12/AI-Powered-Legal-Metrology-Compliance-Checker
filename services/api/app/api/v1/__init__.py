from .inspections import router as inspections_router
from .products import router as products_router
from .inspection_images import router as inspection_images_router
from .scans import router as scans_router

__all__ = [
    "inspections_router",
    "products_router",
    "inspection_images_router",
    "scans_router",
]
