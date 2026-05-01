from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str
    country_code: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("phone")
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        if not v.replace(" ", "").isdigit():
            raise ValueError("Phone must contain digits only")
        return v.replace(" ", "")


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    firstName: str
    lastName: str
    phone: str
    countryCode: str
    avatar: str | None
    role: str
    createdAt: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_model(cls, user) -> "UserOut":
        return cls(
            id=user.id,
            email=user.email,
            firstName=user.first_name,
            lastName=user.last_name,
            phone=user.phone,
            countryCode=user.country_code,
            avatar=user.avatar,
            role=user.role,
            createdAt=user.created_at,
        )


class AdminOut(BaseModel):
    id: str
    email: str
    name: str
    role: str
    createdAt: datetime

    @classmethod
    def from_orm_model(cls, admin) -> "AdminOut":
        return cls(
            id=admin.id,
            email=admin.email,
            name=admin.name,
            role=admin.role,
            createdAt=admin.created_at,
        )


class LoginResponse(BaseModel):
    token: str
    user: UserOut


class AdminLoginResponse(BaseModel):
    token: str
    admin: AdminOut


class MeResponse(BaseModel):
    user: UserOut
