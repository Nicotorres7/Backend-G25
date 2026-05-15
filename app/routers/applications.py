"""
Router: /applications
Student-facing endpoints (Sprint 2):
  POST /applications → apply to offer
  GET /applications/my → MyApplicationsScreen (View 2)
  GET /applications/bq/top-offers → BQ analytics

Staff-facing endpoints:
  GET /applications/pending
  GET /applications/accepted
  GET /applications/rejected
  PUT /applications/{id}/status
  PATCH /applications/{id}/status (public, no auth)
  GET /applications/search → search across all applications
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.application import ApplicationStatus
from app.schemas.application import (
    ApplicationOut, ApplicationFullOut, UpdateStatusIn,
    ApplyIn, TopOfferOut, MyApplicationsResponse,
    ApplicationSearchOut, RateApplicationIn, AvgApplicationsPerSemesterOut
)
from app.services.application_service import (
    list_by_status, update_status, update_status_public,
    apply_to_offer, list_my_applications,
    get_my_applications, top_offers_by_applications, rate_application, avg_applications_per_semester
)
from app.services.search_service import search_applications

router = APIRouter(prefix="/applications", tags=["applications"])


# ── Public endpoints (no auth) ─────────────────────────────────

@router.get("/search", response_model=list[ApplicationSearchOut])
def search(
    q: Optional[str] = Query(default=None),
    semester: Optional[int] = Query(default=None),
    career: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    Application Search – searches across ALL offers by applicant name, career, or offer title.
    Functional scenario: Staff types a query -> system dynamically queries and returns matches.
    Quality scenario (Performance): Response time < 2 s regardless of query complexity.
    """
    return search_applications(db, q=q, semester=semester, career=career)


@router.patch("/{application_id}/status", response_model=ApplicationFullOut)
def change_status_public(
    application_id: int,
    payload: UpdateStatusIn,
    db: Session = Depends(get_db),
):
    return update_status_public(db, application_id, ApplicationStatus(payload.status))


# ── Student endpoints ───────────────────────────────────────────

@router.post("", response_model=ApplicationOut)
def apply(
    payload: ApplyIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return apply_to_offer(db, current_user, payload)


@router.get(
    "/my",
    response_model=MyApplicationsResponse,
    summary="Get my applications",
    description=(
        "Returns all applications submitted by the authenticated student, "
        "enriched with offer details and aggregated status stats. "
        "Accepts an optional ?status filter (pending | accepted | rejected). "
        "Stats always reflect totals across ALL applications regardless of the active filter. "
        "Use ?detailed=true to include full application profile (student info, ratings, feedback)."
    ),
)
def my_applications(
    status: Optional[str] = Query(default=None, pattern="^(pending|accepted|rejected)$"),
    detailed: bool = Query(default=False, description="Include full application details (profile, ratings, feedback)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_filter = ApplicationStatus(status) if status else None
    return list_my_applications(db, current_user, status_filter, detailed=detailed)


@router.get("/bq/top-offers", response_model=list[TopOfferOut])
def bq_top_offers(db: Session = Depends(get_db)):
    return top_offers_by_applications(db)

@router.get("/bq/avg-per-semester", response_model=list[AvgApplicationsPerSemesterOut])
def bq_avg_per_semester(db: Session = Depends(get_db)):
    return avg_applications_per_semester(db)


# ── Staff endpoints ─────────────────────────────────────────────

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


@router.post("/{application_id}/rate", response_model=ApplicationFullOut)
def rate_application_route(
    application_id: int,
    payload: RateApplicationIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return rate_application(
        db=db,
        user=current_user,
        application_id=application_id,
        rating=payload.rating,
        rating_feedback=payload.rating_feedback,
        rating_punctuality=payload.rating_punctuality,
        rating_quality=payload.rating_quality,
        rating_attitude=payload.rating_attitude,
    )