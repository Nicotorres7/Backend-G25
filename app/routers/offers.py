from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.offer import OfferCreateIn, OfferUpdateIn, OfferOut
from app.schemas.application import ApplicationFullOut
from app.services.offer_service import create_offer, get_all_offers, get_my_offers, get_offer_detail, update_offer, delete_offer
from app.services.application_service import list_by_offer_filtered

router = APIRouter(prefix="/offers", tags=["offers"])


# ── Public endpoints (no auth) ─────────────────────────────────

@router.post("", response_model=OfferOut, status_code=201)
def create_offer_route(
    payload: OfferCreateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_offer(
        db=db,
        title=payload.title,
        description=payload.description,
        requirements=payload.requirements,
        category=payload.category,
        value_cop=payload.value_cop,
        date_time=payload.date_time,
        deadline=payload.deadline,
        duration_hours=payload.duration_hours,
        is_on_site=payload.is_on_site,
        location=payload.location,
        staff_id=current_user.id,
    )


@router.get("", response_model=list[OfferOut])
def list_offers(db: Session = Depends(get_db)):
    return get_all_offers(db)


@router.get("/{offer_id}/applications", response_model=list[ApplicationFullOut])
def get_applications(
    offer_id: int,
    gpa_min: Optional[float] = Query(default=None),
    semester: Optional[int] = Query(default=None),
    availability: Optional[str] = Query(default=None),
    sort_by: str = Query(default="gpa"),
    db: Session = Depends(get_db),
):
    return list_by_offer_filtered(
        db=db,
        offer_id=offer_id,
        gpa_min=gpa_min,
        semester=semester,
        availability=availability,
        sort_by=sort_by,
    )


# ── Auth-protected endpoints ───────────────────────────────────

@router.get("/my", response_model=list[OfferOut])
def my_offers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_offers(db, current_user)


@router.get("/{offer_id}", response_model=OfferOut)
def offer_detail(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_offer_detail(db, current_user, offer_id)


# ── Offer edit & delete (public, matching existing pattern) ────

@router.put("/{offer_id}", response_model=OfferOut)
def update_offer_route(
    offer_id: int,
    payload: OfferUpdateIn,
    db: Session = Depends(get_db),
):
    return update_offer(db, offer_id, payload.model_dump(exclude_unset=True))


@router.delete("/{offer_id}")
def delete_offer_route(
    offer_id: int,
    db: Session = Depends(get_db),
):
    delete_offer(db, offer_id)
    return {"detail": "Offer deleted successfully"}
