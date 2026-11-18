from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.time import format_display, utc_now
from app.core.validation import (
    bad_request,
    validate_category,
    validate_enum_filter,
    validate_priority,
    validate_status,
    validate_ticket_fields,
)
from app.models.ticket import Category, NEXT_STATUS, Priority, Status, Ticket
from app.models.user import Role, User
from app.schemas.ticket import TicketOut


def ticket_to_out(ticket: Ticket) -> TicketOut:
    return TicketOut(
        id=ticket.id,
        title=ticket.title,
        description=ticket.description,
        category=ticket.category.value,
        priority=ticket.priority.value,
        status=ticket.status.value,
        created_by=ticket.creator.full_name,
        creator_id=ticket.creator_id,
        created_at=format_display(ticket.created_at),
        updated_at=format_display(ticket.updated_at),
    )


def create_ticket(
    db: Session,
    user: User,
    title: str,
    description: str,
    category: str,
    priority: str,
) -> TicketOut:
    values = validate_ticket_fields(title, description, category, priority)
    ticket = Ticket(
        title=values["title"],
        description=values["description"],
        category=Category(values["category"]),
        priority=Priority(values["priority"]),
        status=Status.OPEN,
        creator_id=user.id,
        creator=user,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket_to_out(ticket)


def get_ticket(db: Session, ticket_id: int) -> Ticket:
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket


def require_visible_ticket(db: Session, user: User, ticket_id: int) -> Ticket:
    ticket = get_ticket(db, ticket_id)
    if user.role == Role.EMPLOYEE and ticket.creator_id != user.id:
        raise HTTPException(status_code=403, detail="You can only access your own tickets.")
    return ticket


def list_employee_tickets(db: Session, user: User) -> list[TicketOut]:
    tickets = db.scalars(
        select(Ticket)
        .where(Ticket.creator_id == user.id)
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
    ).all()
    return [ticket_to_out(ticket) for ticket in tickets]


def list_support_tickets(
    db: Session,
    search: str | None,
    status: str | None,
    category: str | None,
    priority: str | None,
) -> list[TicketOut]:
    status_filter = validate_enum_filter(status, {item.value for item in Status}, "Status")
    category_filter = validate_enum_filter(category, {item.value for item in Category}, "Category")
    priority_filter = validate_enum_filter(priority, {item.value for item in Priority}, "Priority")
    search_text = (search or "").strip().lower()

    query = select(Ticket).join(User, Ticket.creator_id == User.id)
    if status_filter:
        query = query.where(Ticket.status == Status(status_filter))
    if category_filter:
        query = query.where(Ticket.category == Category(category_filter))
    if priority_filter:
        query = query.where(Ticket.priority == Priority(priority_filter))
    if search_text:
        pattern = f"%{search_text}%"
        query = query.where(
            Ticket.title.ilike(pattern)
            | Ticket.description.ilike(pattern)
            | User.full_name.ilike(pattern)
        )

    query = query.order_by(Ticket.created_at.desc(), Ticket.id.desc())
    return [ticket_to_out(ticket) for ticket in db.scalars(query).all()]


def update_ticket_content(
    db: Session,
    user: User,
    ticket_id: int,
    payload: dict,
) -> TicketOut:
    # Required check order: authentication -> existence -> authorization -> input.
    ticket = get_ticket(db, ticket_id)
    if user.role != Role.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Only the ticket owner can edit ticket content.")
    if ticket.creator_id != user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own tickets.")
    if ticket.status == Status.CLOSED:
        raise HTTPException(status_code=403, detail="A Closed ticket cannot be edited.")

    values = validate_ticket_fields(
        payload.get("title"),
        payload.get("description"),
        payload.get("category"),
        payload.get("priority"),
    )
    ticket.title = values["title"]
    ticket.description = values["description"]
    ticket.category = Category(values["category"])
    ticket.priority = Priority(values["priority"])
    ticket.updated_at = utc_now()
    db.commit()
    db.refresh(ticket)
    return ticket_to_out(ticket)


def update_ticket_status(db: Session, user: User, ticket_id: int, payload: dict) -> TicketOut:
    # Required check order: authentication -> existence -> authorization -> input.
    ticket = get_ticket(db, ticket_id)
    if user.role != Role.SUPPORT_STAFF:
        raise HTTPException(status_code=403, detail="Support Staff access required.")

    status_value = validate_status(payload.get("status"))
    target = Status(status_value)
    allowed = NEXT_STATUS[ticket.status]
    if allowed is None or target != allowed:
        raise bad_request("Only the next status step is allowed.")

    ticket.status = target
    ticket.updated_at = utc_now()
    db.commit()
    db.refresh(ticket)
    return ticket_to_out(ticket)
