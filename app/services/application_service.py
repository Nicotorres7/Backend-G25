from typing import Optional
from sqlalchemy.orm import Session
from app.models.application import Application, ApplicationStatus
from app.models.offer import Offer
from app.models.user import User
from app.utils.exceptions import NotFound, Forbidden


def _staff_offer_ids(db: Session, user: User) -> list[int]:
    rows = db.query(Offer.id).filter(Offer.staff_id == user.id).all()
    return [r[0] for r in rows]


def list_by_status(db: Session, user: User, status: ApplicationStatus) -> list[Application]:
    offer_ids = _staff_offer_ids(db, user)
    if not offer_ids:
        return []
    return (
        db.query(Application)
        .filter(Application.offer_id.in_(offer_ids), Application.status == status)
        .order_by(Application.id.desc())
        .all()
    )


def list_my_applications(
    db: Session,
    user: User,
    status_filter: Optional[ApplicationStatus] = None,
) -> dict:
    """
    Returns all applications submitted by the authenticated student,
    optionally filtered by status, enriched with offer details.

    Also computes aggregated stats (total, pending, accepted, rejected)
    across ALL the student's applications regardless of the active filter —
    answering the Type 2 business question:
    'How many of my applications are in each status?'

    Filtering strategy: Application.student_email == user.email
    (Application stores student identity as plain strings, not a FK to users).
    """
    base_query = db.query(Application).filter(Application.student_email == user.email)

    filtered = base_query
    if status_filter:
        filtered = filtered.filter(Application.status == status_filter)
    applications = filtered.order_by(Application.id.desc()).all()

    for application in applications:
        application.offer = db.query(Offer).filter(Offer.id == application.offer_id).first()

    all_apps = base_query.all()
    stats = {
        "total": len(all_apps),
        "pending": sum(1 for a in all_apps if a.status == ApplicationStatus.pending),
        "accepted": sum(1 for a in all_apps if a.status == ApplicationStatus.accepted),
        "rejected": sum(1 for a in all_apps if a.status == ApplicationStatus.rejected),
    }

    return {"applications": applications, "stats": stats}


def update_status(db: Session, user: User, application_id: int, new_status: ApplicationStatus) -> Application:
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise NotFound("Application not found")

    offer = db.query(Offer).filter(Offer.id == app.offer_id).first()
    if not offer:
        raise NotFound("Offer not found")
    if offer.staff_id != user.id:
        raise Forbidden("Not your application")

    app.status = new_status
    db.add(app)
    db.commit()
    db.refresh(app)
    return app
