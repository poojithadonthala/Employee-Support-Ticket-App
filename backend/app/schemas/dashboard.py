from pydantic import BaseModel

from app.schemas.ticket import TicketOut


class StatsOut(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    closed: int


class EmployeeDashboardOut(StatsOut):
    recent_tickets: list[TicketOut]


class SupportDashboardOut(StatsOut):
    pass
