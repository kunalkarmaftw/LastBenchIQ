"""Shared FastAPI dependencies."""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services import auth_service

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    """Resolve the signed-in student, or 401.

    Every protected route depends on this. Routes must take the user from here
    rather than from a path or query parameter, or one student could read
    another's data by changing an id in the URL.
    """
    unauthorised = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not signed in.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorised

    subject = decode_access_token(credentials.credentials)
    if subject is None:
        raise unauthorised

    try:
        user_id = uuid.UUID(subject)
    except ValueError:
        raise unauthorised from None

    user = auth_service.get_by_id(db, user_id)
    if user is None:
        # A valid token for a deleted account.
        raise unauthorised
    return user
