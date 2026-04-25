from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.application import Application


def search_applications(
    db: Session,
    q: str | None = None,
    semester: int | None = None,
    career: str | None = None,
) -> list[Application]:
    """
    Application Search – dynamically queries all applications across every offer.
    Functional scenario: Staff types a name/career query -> system returns matching
    applications from all offers in real time.
    Quality scenario (Usability): Results reflect current DB state; no caching.
    """
    query = db.query(Application)

    if q:
        term = f"%{q.lower()}%"
        query = query.filter(
            or_(
                Application.applicant_name.ilike(term),
                Application.career.ilike(term),
                Application.offer_title.ilike(term),
            )
        )

    if semester is not None:
        query = query.filter(Application.semester == semester)

    if career:
        query = query.filter(Application.career.ilike(f"%{career}%"))

    return query.order_by(Application.gpa.desc()).all()
