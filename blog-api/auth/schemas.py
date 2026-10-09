from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

FORBIDDEN_WORDS = {"admin", "root", "superuser", "test"}

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator('username')
    @classmethod
    def username_no_forbidden_words(cls, value: str) -> str:
        if value.lower() in FORBIDDEN_WORDS:
            raise ValueError("Это имя зарезервировано")
        return value

class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=3)
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    created_at: datetime