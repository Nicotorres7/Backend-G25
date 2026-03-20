"""
Router: /users
Consumed by: StudentProfileScreen (View 1 — Sprint 2, branch Nicotorres7)

Endpoints:
  GET  /users/me              → loads authenticated user data into StudentProfileScreen
  PUT  /users/change-password → changes password from ChangePasswordScreen (via SettingsScreen)
  PUT  /users/me              → updates profile from EditProfileScreen and preferences from SettingsScreen

Feature classification (rubric):
  - GET  /users/me              → f (external service) + e (authentication)
  - PUT  /users/change-password → f (external service) + e (authentication)
  - PUT  /users/me              → f (external service)

Note: PUT /users/me requires ALL fields (name, department, language, is_dark_mode).
The frontend must always send the full object even when updating a single field.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserOut, UserUpdateIn, ChangePasswordIn
from app.services.user_service import update_me, change_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user",
    description=(
        "Returns the profile of the authenticated user. "
        "Used by StudentProfileScreen to display name, department and application stats. "
        "Requires a valid Bearer token in the Authorization header."
    ),
)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put(
    "/change-password",
    summary="Change password",
    description=(
        "Changes the password of the authenticated user. "
        "Used by ChangePasswordScreen (accessed from SettingsScreen). "
        "Validates current_password against the stored hash before updating. "
        "confirm_password is validated at schema level."
    ),
)
def change_password_route(
    payload: ChangePasswordIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    change_password(db, current_user, payload.current_password, payload.new_password)
    return {"detail": "Password updated successfully"}


@router.put(
    "/me",
    response_model=UserOut,
    summary="Update profile",
    description=(
        "Updates the authenticated user's profile. Used by: "
        "EditProfileScreen (name, department, language) and "
        "SettingsScreen (is_dark_mode, language toggles in real time). "
        "All fields are required — send current values for fields that are not being changed."
    ),
)
def update_profile(
    payload: UserUpdateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = update_me(db, current_user, payload.name, payload.department, payload.language, payload.is_dark_mode)
    return updated_user
