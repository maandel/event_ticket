from app.infrastructure.celery_app import celery_app
from app.infrastructure.cloudinary_client import (
    delete_image_sync,
    upload_image_sync,
)


@celery_app.task(name="media.upload_event_image", bind=True, max_retries=3)
def upload_event_image(self, file_bytes: bytes, event_id: str) -> str:
    try:
        url = upload_image_sync(
            file_bytes=file_bytes,
            folder="worldticket/events",
            public_id=f"event_{event_id}",
        )
        return url
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2**self.request.retries)


@celery_app.task(name="media.upload_section_image", bind=True, max_retries=3)
def upload_section_image(self, file_bytes: bytes, section_id: str) -> str:
    try:
        url = upload_image_sync(
            file_bytes=file_bytes,
            folder="worldticket/sections",
            public_id=f"section_{section_id}",
        )
        return url
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2**self.request.retries)


@celery_app.task(name="media.delete_image", bind=True, max_retries=3)
def delete_image(self, public_id: str) -> None:
    try:
        delete_image_sync(public_id)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2**self.request.retries)
