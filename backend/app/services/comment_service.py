from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import format_display, utc_now
from app.core.validation import validate_comment_content
from app.models.comment import Comment
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.comment import CommentOut
from app.services.ticket_service import require_visible_ticket


def comment_to_out(comment: Comment) -> CommentOut:
    return CommentOut(
        id=comment.id,
        ticket_id=comment.ticket_id,
        author_id=comment.author_id,
        author=comment.author.full_name,
        author_role=comment.author.role.value,
        content=comment.content,
        created_at=format_display(comment.created_at),
    )


def list_comments(db: Session, user: User, ticket_id: int) -> list[CommentOut]:
    ticket = require_visible_ticket(db, user, ticket_id)
    comments = db.scalars(
        select(Comment)
        .where(Comment.ticket_id == ticket.id)
        .order_by(Comment.created_at.asc(), Comment.id.asc())
    ).all()
    return [comment_to_out(comment) for comment in comments]


def add_comment(db: Session, user: User, ticket: Ticket, payload: dict) -> CommentOut:
    content = validate_comment_content(payload.get("content"))
    comment = Comment(
        ticket_id=ticket.id,
        author_id=user.id,
        content=content,
        created_at=utc_now(),
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment_to_out(comment)
