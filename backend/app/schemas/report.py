from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Any

# Data received from the user when creating a report
class ReportCreate(BaseModel):
    latitude: float
    longitude: float

# Data returned to the user after a report is created
class Report(BaseModel):
    report_id: uuid.UUID
    user_id: uuid.UUID
    timestamp: datetime
    latitude: float
    longitude: float
    status: str
    anonymized_image_url: str | None = None # Add this line
    violation_details: dict[str, Any] | None = None

    class Config:
        from_attributes = True # Replaces orm_mode = True