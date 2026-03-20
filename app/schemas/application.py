from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Literal, Optional

Status = Literal["pending", "accepted", "rejected"]


class ApplicationOut(BaseModel):
    """Legacy schema for auth-based routes."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    offer_id: int
    student_name: Optional[str]
    student_email: Optional[EmailStr]
    status: Status


class ApplicationFullOut(BaseModel):
    """Full schema for public Flutter-facing routes."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    offer_id: int
    offer_title: str
    applicant_name: str
    career: str
    semester: int
    gpa: float
    availability: str
    motivation_letter: str
    status: Status
    created_at: datetime


class ApplicationSearchOut(BaseModel):
    """Schema for application search results across all offers."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    offer_id: int
    offer_title: str
    applicant_name: str
    career: str
    semester: int
    gpa: float
    availability: str
    status: Status
    created_at: datetime


class UpdateStatusIn(BaseModel):
    status: Status


# --- Student-facing schemas (GET /applications/my) ---

class OfferSummary(BaseModel):
    """Minimal offer data embedded in each student application card."""
    id: int
    title: str
    value_cop: int
    duration_hours: int
    date_time: datetime
    is_on_site: bool

    class Config:
        from_attributes = True


class MyApplicationOut(BaseModel):
    """Single application as seen by the student, enriched with offer details."""
    id: int
    offer_id: int
    status: Status
    created_at: datetime
    offer: OfferSummary

    class Config:
        from_attributes = True


class ApplicationStats(BaseModel):
    """
    Aggregated counters across all student applications.
    Answers the Type 2 business question:
    'How many of my applications are pending / accepted / rejected?'
    """
    total: int
    pending: int
    accepted: int
    rejected: int


class MyApplicationsResponse(BaseModel):
    """Full response for GET /applications/my."""
    applications: list[MyApplicationOut]
    stats: ApplicationStats


class ApplyIn(BaseModel):
    offer_id: int


class TopOfferOut(BaseModel):
    title: str
    total: int