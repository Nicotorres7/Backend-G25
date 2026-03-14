import re
from pydantic import BaseModel, EmailStr, field_validator

EMOJI_RE = re.compile(
    "[\U00010000-\U0010ffff"
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\u2600-\u26FF\u2700-\u27BF]+",
    flags=re.UNICODE,
)
NAME_RE = re.compile(r"^[A-Za-zÁÉÍÓÚÜáéíóúüÑñ ]+$")
PASSWORD_RE = re.compile(r"^[^\s\U00010000-\U0010ffff\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\u2600-\u26FF\u2700-\u27BF]+$")


class LoginIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def institutional_email(cls, v: str) -> str:
        if EMOJI_RE.search(v):
            raise ValueError("Email must not contain emojis")
        if not v.lower().endswith("@uniandes.edu.co"):
            raise ValueError("Email must be institutional (@uniandes.edu.co)")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not PASSWORD_RE.match(v):
            raise ValueError("Password must not contain spaces or emojis")
        return v


class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str
    role: str = "student"

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Name must have at least 3 characters")
        if not NAME_RE.match(v):
            raise ValueError("Name must contain only letters and spaces")
        return v

    @field_validator("email")
    @classmethod
    def institutional_email(cls, v: str) -> str:
        if EMOJI_RE.search(v):
            raise ValueError("Email must not contain emojis")
        if not v.lower().endswith("@uniandes.edu.co"):
            raise ValueError("Email must be institutional (@uniandes.edu.co)")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if not PASSWORD_RE.match(v):
            raise ValueError("Password must not contain spaces or emojis")
        return v

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str) -> str:
        if EMOJI_RE.search(v):
            raise ValueError("Department must not contain emojis")
        return v.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ("student", "staff"):
            raise ValueError("Role must be 'student' or 'staff'")
        return v


class RefreshIn(BaseModel):
    refresh_token: str


class TokenUserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    role: str
    language: str
    is_dark_mode: bool


class LoginOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: TokenUserOut


class RefreshOut(BaseModel):
    access_token: str
    token_type: str = "bearer"