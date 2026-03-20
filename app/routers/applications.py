"""
Router: /applications
Student-facing endpoint (Sprint 2, branch Nicotorres7):
  GET /applications/my → MyApplicationsScreen (View 2)

Staff-facing endpoints (Sprint 1):
  GET /applications/pending
  GET /applications/accepted
  GET /applications/rejected
  PUT /applications/{id}/status

Feature classification (rubric):
  - GET /applications/my → f (external service) + b (Type 2 question) + d (smart feature)
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.application import ApplicationStatus
from app.schemas.application import ApplicationOut, UpdateStatusIn, MyApplicationsResponse
from app.services.application_service import list_by_status, update_status, list_my_applications

from app.schemas.application import ApplicationOut, UpdateStatusIn, ApplyIn, TopOfferOut
from app.services.application_service import (
    list_by_status, update_status, apply_to_offer,
    get_my_applications, top_offers_by_applications
)

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get(
    "/my",
    response_model=MyApplicationsResponse,
    summary="Get my applications",
    description=(
        "Returns all applications submitted by the authenticated student, "
        "enriched with offer details and aggregated status stats. "
        "Accepts an optional ?status filter (pending | accepted | rejected). "
        "Stats always reflect totals across ALL applications regardless of the active filter."
    ),
)
def my_applications(
    status: Optional[str] = Query(default=None, pattern="^(pending|accepted|rejected)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_filter = ApplicationStatus(status) if status else None
    return list_my_applications(db, current_user, status_filter)


@router.get("/pending", response_model=list[ApplicationOut])
def pending(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_by_status(db, current_user, ApplicationStatus.pending)


@router.get("/accepted", response_model=list[ApplicationOut])
def accepted(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_by_status(db, current_user, ApplicationStatus.accepted)


@router.get("/rejected", response_model=list[ApplicationOut])
def rejected(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list_by_status(db, current_user, ApplicationStatus.rejected)


@router.put("/{application_id}/status", response_model=ApplicationOut)
def change_status(
    application_id: int,
    payload: UpdateStatusIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_status(db, current_user, application_id, ApplicationStatus(payload.status))

@router.post("", response_model=ApplicationOut)
def apply(
    payload: ApplyIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return apply_to_offer(db, current_user, payload.offer_id)


@router.get("/my", response_model=list[ApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_applications(db, current_user)


@router.get("/bq/top-offers", response_model=list[TopOfferOut])
def bq_top_offers(db: Session = Depends(get_db)):
    return top_offers_by_applications(db)