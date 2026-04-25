import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, field_validator

EMOJI_RE = re.compile(
    "[\U00010000-\U0010ffff"
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF\u2700-\u27BF]+",
    flags=re.UNICODE,
)


def _normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _validate_title_value(value: str) -> str:
    normalized = _normalize_title(value)
    if not normalized:
        raise ValueError("Title must not be empty")
    if EMOJI_RE.search(normalized):
        raise ValueError("Title must not contain emojis")
    if len(normalized) < 3:
        raise ValueError("Title must have at least 3 characters")
    return normalized


def _validate_schedule_value(value: datetime) -> datetime:
    now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
    if value < now:
        raise ValueError("date_time must not be in the past")
    return value


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

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _validate_title_value(value)

    @field_validator("date_time")
    @classmethod
    def validate_date_time(cls, value: datetime) -> datetime:
        return _validate_schedule_value(value)


class OfferUpdateIn(BaseModel):
    """Partial update – only provided fields are changed."""

    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    category: Optional[str] = None
    value_cop: Optional[int] = None
    date_time: Optional[datetime] = None
    deadline: Optional[datetime] = None
    duration_hours: Optional[int] = None
    is_on_site: Optional[bool] = None
    location: Optional[str] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return _validate_title_value(value)

    @field_validator("date_time")
    @classmethod
    def validate_date_time(cls, value: Optional[datetime]) -> Optional[datetime]:
        if value is None:
            return None
        return _validate_schedule_value(value)


OfferState = Literal["upcoming", "active", "closed"]


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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    closed_at: Optional[datetime]
    closed_early: bool
    state: OfferState
    created_at: datetime