from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import report as report_schema
from app.services import report_service
from app.db.database import get_db
from app.db import models
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/reports/", response_model=report_schema.Report, status_code=201)
def submit_new_report(
    report: report_schema.ReportCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Endpoint to submit a new billboard report.
    Requires the user to be authenticated.
    """
    return report_service.create_report(
        db=db, report=report, user_id=current_user.user_id
    )