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
    is_completed: bool
    completed_at: Optional[datetime] = None
    rating: Optional[float] = None
    rating_feedback: Optional[str] = None
    rating_punctuality: Optional[float] = None
    rating_quality: Optional[float] = None
    rating_attitude: Optional[float] = None
    rated_at: Optional[datetime] = None
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
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    value_cop: int
    duration_hours: int
    date_time: datetime
    is_on_site: bool


class MyApplicationOut(BaseModel):
    """Single application as seen by the student, enriched with offer details.

    When ?detailed=false (default): Returns only basic application info for backward compatibility.
    When ?detailed=true: Returns full student profile and rating details.
    """
    model_config = ConfigDict(from_attributes=True)

    # Basic fields (always present)
    id: int
    offer_id: int
    status: Status
    created_at: datetime
    offer: OfferSummary

    # Student profile fields (present when detailed=true, None otherwise)
    applicant_name: Optional[str] = None
    career: Optional[str] = None
    semester: Optional[int] = None
    gpa: Optional[float] = None
    availability: Optional[str] = None
    motivation_letter: Optional[str] = None

    # Completion & rating fields (present when completed and detailed=true)
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    rating: Optional[float] = None
    rating_feedback: Optional[str] = None
    rating_punctuality: Optional[float] = None
    rating_quality: Optional[float] = None
    rating_attitude: Optional[float] = None
    rated_at: Optional[datetime] = None


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
    applicant_name: str
    career: str
    semester: int
    gpa: float
    availability: str
    motivation_letter: str


class TopOfferOut(BaseModel):
    title: str
    total: int


class RateApplicationIn(BaseModel):
    rating: float
    rating_feedback: str
    rating_punctuality: float
    rating_quality: float
    rating_attitude: float

class AvgApplicationsPerSemesterOut(BaseModel):
    semester: int
    avg_applications: float
    total_students: int
    total_applications: int