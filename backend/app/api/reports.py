from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.schemas import report as report_schema
from app.services import report_service
from app.db.database import get_db
from app.db import models
from app.api.auth import get_current_user
import json

router = APIRouter()

@router.post("/reports/", response_model=report_schema.Report, status_code=201)
def submit_new_report(
    report_data: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Endpoint to submit a new billboard report with an image.
    The report data (lat/lon) must be a JSON string in a form field.
    """
    try:
        report_create = report_schema.ReportCreate(**json.loads(report_data))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in report_data field.")

    return report_service.create_report(
        db=db, report=report_create, user_id=current_user.user_id, image=image
    )