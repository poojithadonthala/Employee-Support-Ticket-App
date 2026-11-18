from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import Role, User
from app.services.auth_service import user_for_session_token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return user_for_session_token(db, token)


def require_employee(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Employee access required.")
    return user


def require_support(user: User = Depends(get_current_user)) -> User:
    if user.role != Role.SUPPORT_STAFF:
        raise HTTPException(status_code=403, detail="Support Staff access required.")
    return user
