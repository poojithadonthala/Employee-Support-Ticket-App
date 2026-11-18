from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.core.time import utc_now
from app.core.validation import (
    bad_request,
    normalize_email,
    trim,
    validate_confirm_password,
    validate_email_format,
    validate_full_name,
    validate_password,
)
from app.models.session_token import UserSession
from app.models.user import Role, User
from app.schemas.auth import UserOut


def to_user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        full_name=user.full_name,
        email=user.email,
        role=user.role.value,
    )


def register_employee(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
) -> User:
    name = validate_full_name(full_name)
    normalized_email = validate_email_format(email)
    validated_password = validate_password(password)
    validate_confirm_password(validated_password, confirm_password)

    existing = db.scalar(select(User).where(User.email == normalized_email))
    if existing:
        raise bad_request("Email is already registered.")

    user = User(
        full_name=name,
        email=normalized_email,
        password_hash=hash_password(validated_password),
        role=Role.EMPLOYEE,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise bad_request("Email is already registered.")
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User:
    if not trim(email):
        raise bad_request("Email is required.")
    if not isinstance(password, str) or password == "":
        raise bad_request("Password is required.")

    normalized_email = normalize_email(email)
    user = db.scalar(select(User).where(User.email == normalized_email))
    if not user or not verify_password(user.password_hash, password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return user


def create_session(db: Session, user: User) -> str:
    token = create_session_token()
    session = UserSession(
        token_hash=hash_session_token(token),
        user_id=user.id,
        expires_at=utc_now() + timedelta(hours=settings.session_ttl_hours),
    )
    db.add(session)
    db.commit()
    return token


def user_for_session_token(db: Session, token: str) -> User:
    token_hash = hash_session_token(token)
    session = db.scalar(select(UserSession).where(UserSession.token_hash == token_hash))
    if not session:
        raise HTTPException(status_code=401, detail="Authentication required.")
    if session.revoked_at is not None or session.expires_at <= utc_now():
        raise HTTPException(status_code=401, detail="Session expired or revoked.")
    return session.user


def revoke_session_token(db: Session, token: str | None) -> None:
    if not token:
        return
    token_hash = hash_session_token(token)
    session = db.scalar(select(UserSession).where(UserSession.token_hash == token_hash))
    if session and session.revoked_at is None:
        session.revoked_at = utc_now()
        db.commit()
