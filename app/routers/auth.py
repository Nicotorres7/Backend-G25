from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.schemas.auth import LoginIn, LoginOut, RefreshIn, RefreshOut, RegisterIn
from app.services.auth_service import login, refresh_access_token, register

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginOut)
def auth_login(payload: LoginIn, db: Session = Depends(get_db)):
    return login(db, payload.email.lower(), payload.password)


@router.post("/register", response_model=LoginOut)
def auth_register(payload: RegisterIn, db: Session = Depends(get_db)):
    return register(db, payload.name, payload.email.lower(), payload.password, payload.department, payload.role)


@router.post("/refresh", response_model=RefreshOut)
def auth_refresh(payload: RefreshIn):
    access = refresh_access_token(payload.refresh_token)
    return {"access_token": access, "token_type": "bearer"}