from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.body import json_object_body
from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.comment import CommentOut
from app.services import comment_service, ticket_service

router = APIRouter(prefix="/api", tags=["comments"])


@router.get("/tickets/{ticket_id}/comments", response_model=list[CommentOut])
def list_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[CommentOut]:
    return comment_service.list_comments(db, user, ticket_id)


@router.post("/tickets/{ticket_id}/comments", response_model=CommentOut, status_code=201)
async def add_comment(
    ticket_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CommentOut:
    ticket = ticket_service.require_visible_ticket(db, user, ticket_id)
    payload = await json_object_body(request)
    return comment_service.add_comment(db, user, ticket, payload)
