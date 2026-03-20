from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal, Optional

Status = Literal["pending", "accepted", "rejected"]


class ApplicationOut(BaseModel):
    id: int
    offer_id: int
    student_name: str
    student_email: EmailStr
    status: Status

    class Config:
        from_attributes = True


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