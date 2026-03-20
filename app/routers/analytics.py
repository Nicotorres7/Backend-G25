from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.analytics import OfferAcceptanceRateOut, OverallInsightsOut, GpaByOfferOut, TopApplicantOut
from app.services.analytics_service import (
    get_acceptance_rate_by_offer,
    get_overall_insights,
    get_gpa_by_offer,
    get_top_applicants,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/acceptance-rate", response_model=list[OfferAcceptanceRateOut])
def acceptance_rate(db: Session = Depends(get_db)):
    """
    BQ3 – Returns the acceptance rate of applications for each offer.
    """
    return get_acceptance_rate_by_offer(db)


@router.get("/insights", response_model=OverallInsightsOut)
def insights(db: Session = Depends(get_db)):
    """
    Smart Offer Insights – aggregated KPIs: most/least popular offer,
    overall acceptance rate, average applications per offer.
    """
    return get_overall_insights(db)


@router.get("/gpa-by-offer", response_model=list[GpaByOfferOut])
def gpa_by_offer(db: Session = Depends(get_db)):
    """
    BQ2 – Returns the average GPA of applicants per job offer.
    Only includes offers that have at least one application.
    """
    return get_gpa_by_offer(db)


@router.get("/top-applicants", response_model=list[TopApplicantOut])
def top_applicants(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Top Applicants Leaderboard – returns the highest-GPA applicants across all offers.
    """
    return get_top_applicants(db, limit=limit)