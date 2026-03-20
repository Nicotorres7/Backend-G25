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
