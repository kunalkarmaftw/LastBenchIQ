"""Registration and sign-in. All the logic lives here, not in the router."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import RegisterRequest


class AuthError(Exception):
    """Raised for any registration or sign-in failure the user should see."""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


def get_by_enrollment(db: Session, enrollment_number: str) -> User | None:
    return db.scalar(select(User).where(User.enrollment_number == enrollment_number))


def get_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def get_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def register(db: Session, payload: RegisterRequest) -> User:
    # Checked before inserting so the student gets a useful message naming the
    # field, rather than a database constraint error.
    if get_by_enrollment(db, payload.enrollment_number):
        raise AuthError(
            "An account already exists for this enrollment number.",
            "enrollment_taken",
        )
    if get_by_email(db, payload.email):
        raise AuthError("An account already exists for this email.", "email_taken")

    user = User(
        enrollment_number=payload.enrollment_number,
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        name=payload.name,
        college=payload.college,
        branch=payload.branch,
        graduation_year=payload.graduation_year,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, enrollment_number: str, password: str) -> User:
    user = get_by_enrollment(db, enrollment_number)

    # One message for both "no such account" and "wrong password". Telling the
    # difference lets anyone check which enrollment numbers are registered.
    invalid = AuthError("Enrollment number or password is incorrect.", "invalid_credentials")
    if user is None or not verify_password(password, user.password_hash):
        raise invalid
    return user


def issue_token(user: User) -> str:
    return create_access_token(subject=str(user.id))
