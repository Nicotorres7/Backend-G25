from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.analytics import OfferAcceptanceRateOut, OverallInsightsOut
from app.services.analytics_service import get_acceptance_rate_by_offer, get_overall_insights

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
