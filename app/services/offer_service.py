from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.offer import Offer
from app.models.user import User
from app.utils.exceptions import NotFound, Forbidden


def compute_offer_state(offer: Offer) -> str:
    """Compute offer state based on naive local time.

    All datetime comparisons use naive local time (no timezone info).
    offer.date_time is stored as naive in the DB (Flutter sends local ISO string).

    upcoming: now < date_time  AND closed_at is None
    active:   date_time <= now < date_time + duration_hours  AND closed_at is None
    closed:   closed_at is not None  OR  now >= date_time + duration_hours
    """
    now = datetime.now()  # naive local time — matches naive DB storage
    dt = offer.date_time
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)  # strip tz for consistent naive comparison

    end = dt + timedelta(hours=offer.duration_hours)

    # closed_at is only checked for existence here, not compared to now
    if offer.closed_at is not None or now >= end:
        return "closed"
    if now >= dt:
        return "active"
    return "upcoming"


def _with_state(offer: Offer) -> Offer:
    """Attach computed `state` attribute to ORM object so OfferOut can serialize it."""
    offer.state = compute_offer_state(offer)
    return offer


def create_offer(db: Session, title: str, description: str, requirements: str,
                 category, value_cop: int, date_time, deadline,
                 duration_hours: int, is_on_site: bool, location: str,
                 staff_id=None) -> Offer:
    offer = Offer(
        staff_id=staff_id, title=title, description=description,
        requirements=requirements, category=category, value_cop=value_cop,
        date_time=date_time, deadline=deadline, duration_hours=duration_hours,
        is_on_site=is_on_site, location=location,
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return _with_state(offer)


def get_all_offers(db: Session) -> list[Offer]:
    return [_with_state(o) for o in db.query(Offer).order_by(Offer.created_at.desc()).all()]


def get_my_offers(db: Session, user: User, state: str | None = None) -> list[Offer]:
    offers = db.query(Offer).filter(Offer.staff_id == user.id).order_by(Offer.id.desc()).all()
    offers = [_with_state(o) for o in offers]
    if state:
        offers = [o for o in offers if o.state == state]
    return offers


def get_offer_detail(db: Session, user: User, offer_id: int) -> Offer:
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise NotFound("Offer not found")
    if offer.staff_id != user.id:
        raise Forbidden("Not your offer")
    return _with_state(offer)


def get_offer_by_id(db: Session, offer_id: int) -> Offer:
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise NotFound("Offer not found")
    return _with_state(offer)


def update_offer(db: Session, offer_id: int, data: dict) -> Offer:
    offer = get_offer_by_id(db, offer_id)
    for key, value in data.items():
        if value is not None:
            setattr(offer, key, value)
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return _with_state(offer)


def close_offer(db: Session, user: User, offer_id: int) -> Offer:
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise NotFound("Offer not found")
    if offer.staff_id != user.id:
        raise Forbidden("Not your offer")
    if offer.closed_at is not None:
        return _with_state(offer)  # already closed, idempotent
    offer.closed_at = datetime.now()
    offer.closed_early = True
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return _with_state(offer)


def delete_offer(db: Session, offer_id: int) -> None:
    offer = get_offer_by_id(db, offer_id)
    db.delete(offer)
    db.commit()
