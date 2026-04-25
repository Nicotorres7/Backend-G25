from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.offer import Offer
from app.models.application import Application

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/time-to-first-application")
def time_to_first_application(db: Session = Depends(get_db)):
    """BQ7 (Santiago Reyes): Average days between job offer publication and first application.

    Iterates every offer, finds its earliest application, computes the delta in days,
    and returns the mean across all offers that have at least one application.
    """
    offers = db.query(Offer).all()

    total_days = 0.0
    offers_with_apps = 0

    for offer in offers:
        first_app = (
            db.query(Application)
            .filter(Application.offer_id == offer.id)
            .order_by(Application.created_at.asc())
            .first()
        )

        if first_app is None:
            continue

        if offer.created_at is None or first_app.created_at is None:
            continue

        # Normalize to naive datetimes so subtraction always works
        offer_ts = offer.created_at.replace(tzinfo=None)
        app_ts = first_app.created_at.replace(tzinfo=None)

        delta_seconds = abs((app_ts - offer_ts).total_seconds())
        total_days += delta_seconds / 86400.0
        offers_with_apps += 1

    avg_days = round(total_days / offers_with_apps, 2) if offers_with_apps > 0 else 0.0

    return {
        "average_days_to_first_application": avg_days,
        "offers_with_applications": offers_with_apps,
        "total_offers": len(offers),
    }
