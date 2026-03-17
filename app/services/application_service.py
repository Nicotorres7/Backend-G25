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


def list_by_offer_filtered(
    db: Session,
    offer_id: int,
    gpa_min: Optional[float] = None,
    semester: Optional[int] = None,
    availability: Optional[str] = None,
    sort_by: str = "gpa",
) -> list[Application]:
    query = db.query(Application).filter(Application.offer_id == offer_id)

    if gpa_min is not None:
        query = query.filter(Application.gpa >= gpa_min)
    if semester is not None:
        query = query.filter(Application.semester == semester)
    if availability is not None:
        query = query.filter(Application.availability == availability)

    if sort_by == "semester":
        query = query.order_by(Application.semester.asc())
    elif sort_by == "date":
        query = query.order_by(Application.created_at.desc())
    else:  # default: gpa descending
        query = query.order_by(Application.gpa.desc())

    return query.all()


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


def update_status_public(db: Session, application_id: int, new_status: ApplicationStatus) -> Application:
    """Update application status without requiring auth."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise NotFound("Application not found")

    app.status = new_status
    db.add(app)
    db.commit()
    db.refresh(app)
    return app
