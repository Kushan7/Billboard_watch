import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    DECIMAL,
    Boolean,
    ForeignKey,
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    VERIFIED_VIOLATION = "verified_violation"

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False) # <--- ADD THIS LINE
    points = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    reports = relationship("Report", back_populates="user")

class Report(Base):
    __tablename__ = "reports"
    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    latitude = Column(DECIMAL, nullable=False)
    longitude = Column(DECIMAL, nullable=False)
    status = Column(SAEnum(ReportStatus), default=ReportStatus.PENDING)
    violation_flags = Column(JSONB) # e.g., {"unlicensed_agency": true, "prohibited_zone": false}
    violation_details = Column(JSONB, nullable=True)

    user = relationship("User", back_populates="reports")
    images = relationship("Image", back_populates="report", cascade="all, delete-orphan")
    ocr_extractions = relationship("OCRExtraction", back_populates="report", cascade="all, delete-orphan")

class Image(Base):
    __tablename__ = "images"
    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.report_id"), nullable=False)
    original_image_url = Column(String, nullable=True) # URL for the original image in cloud storage
    anonymized_image_url = Column(String, nullable=False) # URL for the PII-redacted image

    report = relationship("Report", back_populates="images")

class OCRExtraction(Base):
    __tablename__ = "ocrextractions"
    ocr_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id = Column(UUID(as_uuid=True), ForeignKey("reports.report_id"), nullable=False)
    extracted_text = Column(String)
    confidence_score = Column(DECIMAL)

    report = relationship("Report", back_populates="ocr_extractions")

class OfficialDataAgency(Base):
    __tablename__ = "officialdata_agencies"
    agency_id = Column(Integer, primary_key=True, autoincrement=True)
    agency_name = Column(String, nullable=False, unique=True)
    is_authorized = Column(Boolean, default=True)