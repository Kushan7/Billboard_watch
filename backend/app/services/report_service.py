from sqlalchemy.orm import Session
from app.db import models
from app.schemas import report as report_schema
import uuid
from fastapi import UploadFile
import shutil
from pathlib import Path

# Create a directory to store images
IMAGE_DIR = Path("uploaded_images")
IMAGE_DIR.mkdir(exist_ok=True)

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Saves an uploaded file to a destination."""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def create_report(db: Session, report: report_schema.ReportCreate, user_id: uuid.UUID, image: UploadFile):
    """
    Creates a new report and saves its associated image.
    """
    db_report = models.Report(
        latitude=report.latitude,
        longitude=report.longitude,
        user_id=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # Save the image file with a unique name
    image_filename = f"{db_report.report_id}.jpg"
    image_path = IMAGE_DIR / image_filename
    save_upload_file(image, image_path)

    # For now, we'll store a simple relative URL. In a real app, this would be a cloud URL.
    # We will assume this is the "anonymized" URL for now.
    db_image = models.Image(
        report_id=db_report.report_id,
        anonymized_image_url=str(image_path)
    )
    db.add(db_image)
    db.commit()

    return db_report