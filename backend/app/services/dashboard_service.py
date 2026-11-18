from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ticket import Status, Ticket
from app.models.user import User
from app.schemas.dashboard import EmployeeDashboardOut, StatsOut, SupportDashboardOut
from app.services.ticket_service import ticket_to_out


def _empty_counts() -> dict[str, int]:
    return {
        "total": 0,
        "open": 0,
        "in_progress": 0,
        "resolved": 0,
        "closed": 0,
    }


def _counts_from_rows(rows: list[tuple[Status, int]]) -> StatsOut:
    counts = _empty_counts()
    key_by_status = {
        Status.OPEN: "open",
        Status.IN_PROGRESS: "in_progress",
        Status.RESOLVED: "resolved",
        Status.CLOSED: "closed",
    }
    for status, count in rows:
        counts[key_by_status[status]] = count
    counts["total"] = sum(counts[key] for key in key_by_status.values())
    return StatsOut(**counts)


def employee_dashboard(db: Session, user: User) -> EmployeeDashboardOut:
    rows = db.execute(
        select(Ticket.status, func.count(Ticket.id))
        .where(Ticket.creator_id == user.id)
        .group_by(Ticket.status)
    ).all()
    stats = _counts_from_rows(rows)
    recent = db.scalars(
        select(Ticket)
        .where(Ticket.creator_id == user.id)
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
        .limit(5)
    ).all()
    return EmployeeDashboardOut(
        **stats.model_dump(),
        recent_tickets=[ticket_to_out(ticket) for ticket in recent],
    )


def support_dashboard(db: Session) -> SupportDashboardOut:
    rows = db.execute(select(Ticket.status, func.count(Ticket.id)).group_by(Ticket.status)).all()
    return SupportDashboardOut(**_counts_from_rows(rows).model_dump())
