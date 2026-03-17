import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    offer_id = Column(Integer, ForeignKey("offers.id", ondelete="CASCADE"), index=True, nullable=False)
    offer_title = Column(String(200), nullable=False, default="")

    # Legacy fields (kept for old auth-based routes)
    student_name = Column(String(100), nullable=True)
    student_email = Column(String(150), nullable=True)

    # New fields required by Flutter spec
    applicant_name = Column(String(100), nullable=False, default="")
    career = Column(String(100), nullable=False, default="")
    semester = Column(Integer, nullable=False, default=1)
    gpa = Column(Float, nullable=False, default=0.0)
    availability = Column(String(20), nullable=False, default="flexible")
    motivation_letter = Column(Text, nullable=False, default="")

    status = Column(Enum(ApplicationStatus, name="application_status"), nullable=False, default=ApplicationStatus.pending)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
