from pydantic import BaseModel, EmailStr, field_validator


class LoginIn(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def institutional_email(cls, v: str) -> str:
        if not v.lower().endswith("@uniandes.edu.co"):
            raise ValueError("Email must be institutional (@uniandes.edu.co)")
        return v


class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    department: str

    @field_validator("email")
    @classmethod
    def institutional_email(cls, v: str) -> str:
        if not v.lower().endswith("@uniandes.edu.co"):
            raise ValueError("Email must be institutional (@uniandes.edu.co)")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Name must have at least 3 characters")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class RefreshIn(BaseModel):
    refresh_token: str


class TokenUserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
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