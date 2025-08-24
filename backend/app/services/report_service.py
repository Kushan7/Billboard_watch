from sqlalchemy.orm import Session
from app.db import models
from app.schemas import report as report_schema
import uuid
from fastapi import UploadFile
import shutil
from pathlib import Path

# --- Import all our analysis tools ---
from transformers import pipeline
from google.cloud import vision
from .banned_words import check_text_for_violations
from .analysis_service import check_gis_violation # We'll reuse the GIS check

# --- Load Models ---
text_classifier = pipeline('text-classification', model='unitary/toxic-bert')
IMAGE_DIR = Path("uploaded_images")
IMAGE_DIR.mkdir(exist_ok=True)

def perform_ocr(image_path: Path) -> str:
    """Detects text in the image file using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description if texts else ""

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Saves an uploaded file to a destination."""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def create_report(db: Session, report: report_schema.ReportCreate, user_id: uuid.UUID, image: UploadFile):
    """
    Creates a new report, saves its image, and runs the full analysis pipeline.
    """
    db_report = models.Report(
        latitude=report.latitude,
        longitude=report.longitude,
        user_id=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    # --- Image Handling ---
    image_filename = f"{db_report.report_id}.jpg"
    image_path = IMAGE_DIR / image_filename
    save_upload_file(image, image_path)
    db_image = models.Image(report_id=db_report.report_id, anonymized_image_url=str(image_path))
    db.add(db_image)

    # --- RUN ANALYSIS PIPELINE ---
    analysis_results = {}

    # 1. Text Analysis (OCR + BERT)
    try:
        detected_text = perform_ocr(image_path)
        if detected_text:
            text_violations = text_classifier(detected_text)
            analysis_results['text_analysis'] = {
                "detected_text": detected_text[:200] + "...",
                "violations": [res for res in text_violations if res['label'] != 'clean' and res['score'] > 0.8]
            }
        else:
            analysis_results['text_analysis'] = "No text found"
    except Exception as e:
        analysis_results['text_analysis'] = f"Error: {e}"

    # 2. GIS Analysis
    gis_violation = check_gis_violation(db_report.latitude, db_report.longitude)
    analysis_results['gis_analysis'] = {
        "is_in_prohibited_zone": gis_violation
    }

    # --- Save analysis results to the database ---
    db_report.violation_details = analysis_results
    db.commit()
    db.refresh(db_report)

    return db_report