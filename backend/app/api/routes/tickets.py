from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.body import json_object_body
from app.api.deps import get_current_user, require_employee, require_support
from app.db.session import get_db
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketOut
from app.services import ticket_service

router = APIRouter(prefix="/api", tags=["tickets"])


@router.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(
    payload: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_employee),
) -> TicketOut:
    return ticket_service.create_ticket(
        db,
        user,
        payload.title,
        payload.description,
        payload.category,
        payload.priority,
    )


@router.get("/employee/tickets", response_model=list[TicketOut])
def employee_tickets(
    db: Session = Depends(get_db),
    user: User = Depends(require_employee),
) -> list[TicketOut]:
    return ticket_service.list_employee_tickets(db, user)


@router.get("/support/tickets", response_model=list[TicketOut])
def support_tickets(
    search: str | None = None,
    status: str | None = None,
    category: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_support),
) -> list[TicketOut]:
    return ticket_service.list_support_tickets(db, search, status, category, priority)


@router.get("/tickets/{ticket_id}", response_model=TicketOut)
def ticket_detail(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TicketOut:
    return ticket_service.ticket_to_out(ticket_service.require_visible_ticket(db, user, ticket_id))


@router.patch("/tickets/{ticket_id}", response_model=TicketOut)
async def update_ticket(
    ticket_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TicketOut:
    payload = await json_object_body(request)
    return ticket_service.update_ticket_content(db, user, ticket_id, payload)


@router.post("/tickets/{ticket_id}/status", response_model=TicketOut)
async def update_status(
    ticket_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> TicketOut:
    payload = await json_object_body(request)
    return ticket_service.update_ticket_status(db, user, ticket_id, payload)
