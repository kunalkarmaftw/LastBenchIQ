"""Request and response shapes for registration and sign-in."""

import re
import uuid
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.security import MAX_PASSWORD_BYTES, MIN_PASSWORD_LENGTH
from app.models.user import CareerGoal

# Enrollment numbers at this university are digits only. Length is bounded
# rather than fixed: formats differ between colleges and change between
# batches, and rejecting a valid student's number is worse than accepting an
# unusual one. Digits-only is the part that holds across every sample.
ENROLLMENT_PATTERN = re.compile(r"^\d{8,15}$")

EnrollmentNumber = Annotated[str, Field(min_length=8, max_length=15)]
Password = Annotated[str, Field(min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_BYTES)]


def _clean_enrollment(value: str) -> str:
    """Strip the spaces and dashes students type when copying from an ID card."""
    cleaned = re.sub(r"[\s-]", "", value)
    if not ENROLLMENT_PATTERN.match(cleaned):
        raise ValueError("Enrollment number must be 8 to 15 digits")
    return cleaned


class RegisterRequest(BaseModel):
    enrollment_number: EnrollmentNumber
    email: EmailStr
    password: Password
    name: Annotated[str, Field(min_length=2, max_length=120)]
    college: str | None = Field(default=None, max_length=200)
    branch: str | None = Field(default=None, max_length=80)
    graduation_year: int | None = Field(default=None, ge=2000, le=2100)

    @field_validator("enrollment_number")
    @classmethod
    def validate_enrollment(cls, v: str) -> str:
        return _clean_enrollment(v)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class LoginRequest(BaseModel):
    """Sign in with the enrollment number, not the email."""

    enrollment_number: EnrollmentNumber
    password: str

    @field_validator("enrollment_number")
    @classmethod
    def validate_enrollment(cls, v: str) -> str:
        return _clean_enrollment(v)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    enrollment_number: str
    email: str
    name: str
    college: str | None
    branch: str | None
    graduation_year: int | None
    career_goal: CareerGoal
    target_role: str | None


class AuthResponse(BaseModel):
    access_token: str
    # S105: the OAuth 2.0 token *type*, a fixed protocol literal, not a secret.
    token_type: str = "bearer"  # noqa: S105
    user: UserOut
