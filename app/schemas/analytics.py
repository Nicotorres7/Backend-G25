from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict


class OfferAcceptanceRateOut(BaseModel):
    """
    BQ3: "What is the acceptance rate of job applications per job offer?"
    Functional scenario: Staff requests acceptance-rate report -> system
    aggregates application statuses per offer -> returns breakdown.
    Quality scenario (Performance): Response time < 2 s for up to 500 offers.
    """

    model_config = ConfigDict(from_attributes=True)

    offer_id: int
    offer_title: str
    category: Optional[str]
    total_applications: int
    accepted: int
    rejected: int
    pending: int
    acceptance_rate: float


class OverallInsightsOut(BaseModel):
    """
    Smart Offer Insights – automatically computed KPIs.
    Functional scenario: Staff opens insights dashboard -> system computes
    aggregated metrics across all their offers -> returns summary.
    Quality scenario (Usability): Single-request payload; no extra clicks.
    """

    total_offers: int
    total_applications: int
    overall_acceptance_rate: float
    most_popular_offer: Optional[str]
    most_popular_offer_applications: int
    least_popular_offer: Optional[str]
    least_popular_offer_applications: int
    avg_applications_per_offer: float


class GpaByOfferOut(BaseModel):
    """
    BQ2: "What is the average GPA of applicants per job offer?"
    Functional scenario: Staff requests GPA report -> system aggregates GPA
    data from applications grouped by offer -> returns breakdown per offer.
    Quality scenario (Performance): Response time < 2 s for up to 500 offers.
    """

    model_config = ConfigDict(from_attributes=True)

    offer_id: int
    offer_title: str
    category: Optional[str]
    total_applicants: int
    average_gpa: float
    min_gpa: float
    max_gpa: float


class TopApplicantOut(BaseModel):
    """
    Top Applicants Leaderboard – automatically ranks best candidates by GPA.
    Functional scenario: Staff opens leaderboard -> system queries all applications,
    ranks by GPA -> returns ordered list.
    Quality scenario (Usability): Single request; no manual filtering needed.
    """

    model_config = ConfigDict(from_attributes=True)

    applicant_name: str
    career: str
    semester: int
    gpa: float
    total_applications: int
    offers_applied: list[str]
    status_summary: Dict[str, int]
