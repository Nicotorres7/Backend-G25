from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class OfferCreateIn(BaseModel):
    title: str
    description: str
    requirements: str = ""
    category: Optional[str] = None
    value_cop: int
    date_time: datetime
    deadline: Optional[datetime] = None
    duration_hours: int
    is_on_site: bool
    location: str = ""


class OfferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    requirements: str
    category: Optional[str]
    value_cop: int
    date_time: datetime
    deadline: Optional[datetime]
    duration_hours: int
    is_on_site: bool
    location: str
    created_at: datetime
