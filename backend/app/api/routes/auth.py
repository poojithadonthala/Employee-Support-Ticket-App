from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, UserOut
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_ttl_hours * 3600,
        httponly=True,
        samesite="lax",
        secure=settings.secure_cookies,
        path="/",
    )


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserOut:
    user = auth_service.register_employee(
        db,
        payload.full_name,
        payload.email,
        payload.password,
        payload.confirm_password,
    )
    return auth_service.to_user_out(user)


@router.post("/login", response_model=UserOut)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> UserOut:
    user = auth_service.authenticate_user(db, payload.email, payload.password)
    token = auth_service.create_session(db, user)
    _set_session_cookie(response, token)
    return auth_service.to_user_out(user)


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)) -> UserOut:
    return auth_service.to_user_out(user)


@router.post("/logout", status_code=204)
def logout(request: Request, response: Response, db: Session = Depends(get_db), user=Depends(get_current_user)) -> None:
    auth_service.revoke_session_token(db, request.cookies.get(settings.session_cookie_name))
    response.delete_cookie(key=settings.session_cookie_name, path="/")
    response.status_code = 204
