import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_image_sync(
    file_bytes: bytes,
    folder: str,
    public_id: str | None = None,
) -> str:
    options: dict = {
        "folder": folder,
        "resource_type": "image",
        "overwrite": True,
    }
    if public_id:
        options["public_id"] = public_id

    result = cloudinary.uploader.upload(file_bytes, **options)
    return result["secure_url"]


def delete_image_sync(public_id: str) -> None:
    cloudinary.uploader.destroy(public_id)
