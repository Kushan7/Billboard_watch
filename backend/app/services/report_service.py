from sqlalchemy.orm import Session
from app.db import models
from app.schemas import report as report_schema
import uuid # Add this import
def create_report(db: Session, report: report_schema.ReportCreate, user_id: uuid.UUID):
    """
    Creates a new report in the database linked to a user.
    """
    db_report = models.Report(
        latitude=report.latitude,
        longitude=report.longitude,
        user_id=user_id
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report