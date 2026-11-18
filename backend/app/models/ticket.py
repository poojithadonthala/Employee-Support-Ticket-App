from datetime import datetime
from enum import Enum

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.time import utc_now
from app.db.base import Base


class Category(str, Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    NETWORK = "Network"
    ACCESS = "Access"
    OTHER = "Other"


class Priority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Status(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


NEXT_STATUS = {
    Status.OPEN: Status.IN_PROGRESS,
    Status.IN_PROGRESS: Status.RESOLVED,
    Status.RESOLVED: Status.CLOSED,
    Status.CLOSED: None,
}


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        CheckConstraint("length(title) > 0", name="title_not_empty"),
        CheckConstraint("length(description) > 0", name="description_not_empty"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Category] = mapped_column(
        SAEnum(Category, name="ticket_category", create_constraint=True, native_enum=False),
        nullable=False,
    )
    priority: Mapped[Priority] = mapped_column(
        SAEnum(Priority, name="ticket_priority", create_constraint=True, native_enum=False),
        nullable=False,
    )
    status: Mapped[Status] = mapped_column(
        SAEnum(Status, name="ticket_status", create_constraint=True, native_enum=False),
        nullable=False,
    )
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    creator: Mapped["User"] = relationship(back_populates="tickets", lazy="selectin")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Ticket id={self.id} title={self.title!r} status={self.status.value}>"
