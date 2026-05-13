from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base, SessionLocal
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.offers import router as offers_router
from app.routers.applications import router as applications_router
from app.routers.analytics import router as analytics_router
from app.services.seed_service import seed_if_empty

# Import all models so create_all picks them up
import app.models.user  # noqa: F401
import app.models.offer  # noqa: F401
import app.models.application  # noqa: F401

app = FastAPI(title="Goatly Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(offers_router)
app.include_router(applications_router)
app.include_router(analytics_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)