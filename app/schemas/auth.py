"""Pydantic schemas for admin auth endpoints."""

from pydantic import BaseModel, EmailStr


class AdminLoginRequest(BaseModel):
    """Request payload for admin login."""

    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    """Response returned after successful admin login."""

    access_token: str
    token_type: str = "bearer"  # noqa: S105
