from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func

from app.models.offer import Offer
from app.models.application import Application, ApplicationStatus


def get_acceptance_rate_by_offer(db: Session) -> list[dict]:
    """
    BQ3 – Acceptance rate per offer.
    Uses a single joined query for performance (quality scenario: < 2 s).
    """
    rows = (
        db.query(
            Offer.id,
            Offer.title,
            Offer.category,
            sql_func.count(Application.id).label("total"),
            sql_func.count(
                sql_func.nullif(Application.status != ApplicationStatus.accepted, True)
            ).label("accepted"),
            sql_func.count(
                sql_func.nullif(Application.status != ApplicationStatus.rejected, True)
            ).label("rejected"),
            sql_func.count(
                sql_func.nullif(Application.status != ApplicationStatus.pending, True)
            ).label("pending"),
        )
        .outerjoin(Application, Application.offer_id == Offer.id)
        .group_by(Offer.id, Offer.title, Offer.category)
        .order_by(Offer.id.desc())
        .all()
    )

    results = []
    for row in rows:
        total = row.total
        accepted = row.accepted
        rate = round((accepted / total) * 100, 2) if total > 0 else 0.0
        results.append(
            {
                "offer_id": row.id,
                "offer_title": row.title,
                "category": row.category,
                "total_applications": total,
                "accepted": accepted,
                "rejected": row.rejected,
                "pending": row.pending,
                "acceptance_rate": rate,
            }
        )
    return results


def get_overall_insights(db: Session) -> dict:
    """
    Smart insights – aggregated KPIs across all offers.
    Functional scenario: single endpoint returns everything the dashboard needs.
    """
    offers = db.query(Offer).all()
    if not offers:
        return {
            "total_offers": 0,
            "total_applications": 0,
            "overall_acceptance_rate": 0.0,
            "most_popular_offer": None,
            "most_popular_offer_applications": 0,
            "least_popular_offer": None,
            "least_popular_offer_applications": 0,
            "avg_applications_per_offer": 0.0,
        }

    offer_ids = [o.id for o in offers]
    offer_map = {o.id: o.title for o in offers}

    app_counts = (
        db.query(
            Application.offer_id,
            sql_func.count(Application.id).label("total"),
            sql_func.count(
                sql_func.nullif(Application.status != ApplicationStatus.accepted, True)
            ).label("accepted"),
        )
        .filter(Application.offer_id.in_(offer_ids))
        .group_by(Application.offer_id)
        .all()
    )

    total_apps = 0
    total_accepted = 0
    counts_by_offer: dict[int, int] = {oid: 0 for oid in offer_ids}

    for row in app_counts:
        counts_by_offer[row.offer_id] = row.total
        total_apps += row.total
        total_accepted += row.accepted

    overall_rate = round((total_accepted / total_apps) * 100, 2) if total_apps > 0 else 0.0
    avg_apps = round(total_apps / len(offers), 2)

    most_popular_id = max(counts_by_offer, key=counts_by_offer.get)
    least_popular_id = min(counts_by_offer, key=counts_by_offer.get)

    return {
        "total_offers": len(offers),
        "total_applications": total_apps,
        "overall_acceptance_rate": overall_rate,
        "most_popular_offer": offer_map[most_popular_id],
        "most_popular_offer_applications": counts_by_offer[most_popular_id],
        "least_popular_offer": offer_map[least_popular_id],
        "least_popular_offer_applications": counts_by_offer[least_popular_id],
        "avg_applications_per_offer": avg_apps,
    }
