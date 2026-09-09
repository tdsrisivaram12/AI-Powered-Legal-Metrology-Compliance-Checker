from hashlib import sha256
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.models.inspection import Inspection
from app.models.inspection_image import InspectionImage


STORAGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "storage"
    / "inspection-images"
)

MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class InspectionImageService:

    @staticmethod
    async def upload_image(
        db: Session,
        inspection_id: int,
        file: UploadFile,
    ) -> InspectionImage:

        inspection = db.get(Inspection, inspection_id)

        if inspection is None:
            raise HTTPException(
                status_code=404,
                detail="Inspection not found",
            )

        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG, PNG, and WebP images are allowed",
            )

        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty",
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Image size must not exceed 10 MB",
            )

        try:
            image_stream = BytesIO(content)

            with Image.open(image_stream) as image:
                image.verify()

            image_stream.seek(0)

            with Image.open(image_stream) as image:
                width, height = image.size
                detected_format = image.format

        except (UnidentifiedImageError, OSError):
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is not a valid image",
            )

        expected_format = {
            "image/jpeg": "JPEG",
            "image/png": "PNG",
            "image/webp": "WEBP",
        }[file.content_type]

        if detected_format != expected_format:
            raise HTTPException(
                status_code=400,
                detail="Image content does not match the declared file type",
            )

        file_hash = sha256(content).hexdigest()

        extension = ALLOWED_TYPES[file.content_type]
        filename = f"{uuid4().hex}{extension}"

        inspection_dir = STORAGE_DIR / str(inspection_id)
        inspection_dir.mkdir(parents=True, exist_ok=True)

        storage_path = inspection_dir / filename
        storage_path.write_bytes(content)

        relative_path = (
            Path("inspection-images")
            / str(inspection_id)
            / filename
        )

        image = InspectionImage(
            inspection_id=inspection_id,
            image_type="package",
            storage_path=relative_path.as_posix(),
            original_filename=file.filename,
            mime_type=file.content_type,
            sha256=file_hash,
            width=width,
            height=height,
        )

        db.add(image)
        db.commit()
        db.refresh(image)

        return image
