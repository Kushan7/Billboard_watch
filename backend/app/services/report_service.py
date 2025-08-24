from sqlalchemy.orm import Session
from app.db import models
from app.schemas import report as report_schema
import uuid
from fastapi import UploadFile
import shutil
from pathlib import Path
import json
from shapely.geometry import shape, Point

# --- Setup for Image Saving and GIS Check ---
IMAGE_DIR = Path("uploaded_images")
IMAGE_DIR.mkdir(exist_ok=True)
GIS_DATA_PATH = Path("gis_data/no_hoarding_zones.geojson")

def check_gis_violation(latitude: float, longitude: float) -> bool:
    """
    Checks if the given coordinates fall within a prohibited zone.
    """
    try:
        with open(GIS_DATA_PATH) as f:
            geojson_data = json.load(f)

        point = Point(longitude, latitude) # GeoJSON is (lon, lat)

        for feature in geojson_data['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return True # Violation found
        return False # No violation
    except Exception:
        # If file is not found or invalid, assume no violation
        return False

def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
    """Saves an uploaded file to a destination."""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

def create_report(db: Session, report: report_schema.ReportCreate, user_id: uuid.UUID, image: UploadFile):
    """
    Creates a new report, saves its image, and runs ONLY the GIS analysis.
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

    # --- RUN SIMPLIFIED ANALYSIS PIPELINE ---
    analysis_results = {}

    # 1. Object Recognition is BYPASSED
    analysis_results['object_detection'] = "Bypassed for prototype"

    # 2. Text Analysis is BYPASSED
    analysis_results['text_analysis'] = "Bypassed for prototype"

    # 3. GIS Analysis
    gis_violation = check_gis_violation(db_report.latitude, db_report.longitude)
    analysis_results['gis_analysis'] = {
        "is_in_prohibited_zone": gis_violation
    }

    # --- Save analysis results to the database ---
    db_report.violation_details = analysis_results
    db.commit()
    db.refresh(db_report)

    return db_report