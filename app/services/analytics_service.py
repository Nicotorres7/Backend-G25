from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func

from app.models.offer import Offer
from app.models.application import Application, ApplicationStatus
from collections import defaultdict


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


def get_gpa_by_offer(db: Session) -> list[dict]:
    """
    BQ2 – Average GPA of applicants per offer.
    Uses a single joined query for performance (quality scenario: < 2 s).
    Only includes offers that have at least one application.
    """
    rows = (
        db.query(
            Offer.id,
            Offer.title,
            Offer.category,
            sql_func.count(Application.id).label("total"),
            sql_func.avg(Application.gpa).label("avg_gpa"),
            sql_func.min(Application.gpa).label("min_gpa"),
            sql_func.max(Application.gpa).label("max_gpa"),
        )
        .join(Application, Application.offer_id == Offer.id)
        .group_by(Offer.id, Offer.title, Offer.category)
        .order_by(sql_func.avg(Application.gpa).desc())
        .all()
    )

    results = []
    for row in rows:
        results.append(
            {
                "offer_id": row.id,
                "offer_title": row.title,
                "category": row.category,
                "total_applicants": row.total,
                "average_gpa": round(float(row.avg_gpa), 2),
                "min_gpa": round(float(row.min_gpa), 2),
                "max_gpa": round(float(row.max_gpa), 2),
            }
        )
    return results


def get_top_applicants(db: Session, limit: int = 10) -> list[dict]:
    """
    Top Applicants Leaderboard – ranks candidates by GPA across all offers.
    Functional scenario: Staff opens leaderboard -> system queries all applications,
    deduplicates by applicant name, ranks by GPA descending.
    """
    rows = (
        db.query(Application)
        .order_by(Application.gpa.desc())
        .all()
    )

    # Deduplicate by applicant_name, keeping the one with highest GPA first
    seen: dict[str, dict] = {}
    for app in rows:
        name = app.applicant_name
        if name not in seen:
            seen[name] = {
                "applicant_name": name,
                "career": app.career,
                "semester": app.semester,
                "gpa": app.gpa,
                "total_applications": 0,
                "offers_applied": [],
                "status_summary": {"accepted": 0, "rejected": 0, "pending": 0},
            }
        entry = seen[name]
        entry["total_applications"] += 1
        if app.offer_title not in entry["offers_applied"]:
            entry["offers_applied"].append(app.offer_title)
        entry["status_summary"][app.status.value] += 1

    ranked = sorted(seen.values(), key=lambda x: x["gpa"], reverse=True)
    return ranked[:limit]


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
