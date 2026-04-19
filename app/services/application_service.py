from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc
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
    detailed: bool = False,
) -> dict:
    base_query = db.query(Application).filter(Application.student_email == user.email)

    filtered = base_query
    if status_filter:
        filtered = filtered.filter(Application.status == status_filter)
    applications = filtered.order_by(Application.id.desc()).all()

    for application in applications:
        application.offer = db.query(Offer).filter(Offer.id == application.offer_id).first()
        # If detailed mode is enabled, ensure all fields are populated from the model
        # (they already are since SQLAlchemy loads them from DB)

    all_apps = base_query.all()
    stats = {
        "total": len(all_apps),
        "pending": sum(1 for a in all_apps if a.status == ApplicationStatus.pending),
        "accepted": sum(1 for a in all_apps if a.status == ApplicationStatus.accepted),
        "rejected": sum(1 for a in all_apps if a.status == ApplicationStatus.rejected),
    }

    return {"applications": applications, "stats": stats}


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
    else:
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


def apply_to_offer(db: Session, user: User, payload: "ApplyIn") -> Application:  # type: ignore
    from app.schemas.application import ApplyIn

    if user.role != "student":
        raise Forbidden("Only students can apply to offers")

    offer = db.query(Offer).filter(Offer.id == payload.offer_id).first()
    if not offer:
        raise NotFound("Offer not found")

    existing = db.query(Application).filter(
        Application.offer_id == payload.offer_id,
        Application.student_email == user.email
    ).first()
    if existing:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Already applied to this offer")

    app = Application(
        offer_id=payload.offer_id,
        student_name=user.name,
        student_email=user.email,
        applicant_name=payload.applicant_name,
        career=payload.career,
        semester=payload.semester,
        gpa=payload.gpa,
        availability=payload.availability,
        motivation_letter=payload.motivation_letter,
        status=ApplicationStatus.pending
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def get_my_applications(db: Session, user: User) -> list[Application]:
    return (
        db.query(Application)
        .filter(Application.student_email == user.email)
        .order_by(Application.id.desc())
        .all()
    )


def top_offers_by_applications(db: Session) -> list[dict]:
    rows = (
        db.query(Offer.title, sqlfunc.count(Application.id).label("total"))
        .join(Application, Application.offer_id == Offer.id)
        .group_by(Offer.id, Offer.title)
        .order_by(sqlfunc.count(Application.id).desc())
        .limit(10)
        .all()
    )
    return [{"title": r.title, "total": r.total} for r in rows]


def get_staff_apps_by_offer(
    db: Session,
    user: User,
    offer_id: int,
) -> list[Application]:
    """
    Returns applications filtered by offer lifecycle state:
      upcoming  -> all statuses (pending / accepted / rejected)
      active    -> only accepted
      closed    -> only accepted
    Auth: offer must belong to user (enforced via get_offer_detail).
    """
    from app.services.offer_service import get_offer_detail, compute_offer_state
    offer = get_offer_detail(db, user, offer_id)
    state = compute_offer_state(offer)

    query = db.query(Application).filter(Application.offer_id == offer_id)
    if state in ("active", "closed"):
        query = query.filter(Application.status == ApplicationStatus.accepted)
    return query.order_by(Application.gpa.desc()).all()


def rate_application(
    db: Session,
    user: User,
    application_id: int,
    rating: float,
    rating_feedback: str,
    rating_punctuality: float,
    rating_quality: float,
    rating_attitude: float,
) -> Application:
    from app.services.offer_service import get_offer_by_id, compute_offer_state
    from datetime import datetime, timezone as _tz
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise NotFound("Application not found")
    offer = get_offer_by_id(db, app.offer_id)
    if offer.staff_id != user.id:
        raise Forbidden("Not your application")
    state = compute_offer_state(offer)
    if state != "closed":
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Can only rate applications for closed offers")
    if app.status != ApplicationStatus.accepted:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Can only rate accepted applicants")

    app.is_completed = True
    app.completed_at = datetime.now(_tz.utc)
    app.rating = rating
    app.rating_feedback = rating_feedback
    app.rating_punctuality = rating_punctuality
    app.rating_quality = rating_quality
    app.rating_attitude = rating_attitude
    app.rated_at = datetime.now(_tz.utc)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app