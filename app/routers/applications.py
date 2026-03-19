from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.application import ApplicationStatus
from app.schemas.application import ApplicationOut, ApplicationFullOut, UpdateStatusIn
from app.services.application_service import list_by_status, update_status, update_status_public

router = APIRouter(prefix="/applications", tags=["applications"])


# ── Public endpoints (no auth) ─────────────────────────────────

@router.patch("/{application_id}/status", response_model=ApplicationFullOut)
def change_status_public(
    application_id: int,
    payload: UpdateStatusIn,
    db: Session = Depends(get_db),
):
    return update_status_public(db, application_id, ApplicationStatus(payload.status))


# ── Auth-protected endpoints ───────────────────────────────────

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
