from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True)

    title = Column(String(80), nullable=False)
    description = Column(String(1000), nullable=False)
    requirements = Column(Text, nullable=False, default="")
    category = Column(String(100), nullable=True)

    value_cop = Column(Integer, nullable=False)
    date_time = Column(DateTime(timezone=False), nullable=False)
    deadline = Column(DateTime(timezone=False), nullable=True)
    duration_hours = Column(Integer, nullable=False)
    is_on_site = Column(Boolean, nullable=False, default=True)
    location = Column(String(200), nullable=False, default="")

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    closed_at = Column(DateTime(timezone=True), nullable=True, default=None)
    closed_early = Column(Boolean, nullable=False, default=False, server_default='false')
