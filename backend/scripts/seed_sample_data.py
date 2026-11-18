import getpass
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.core.validation import normalize_email  # noqa: E402
from app.db.session import SessionLocal, create_tables  # noqa: E402
from app.models.ticket import Category, Priority, Status, Ticket  # noqa: E402
from app.models.user import Role, User  # noqa: E402

EMPLOYEE_EMAIL = "ravi@company.com"
SUPPORT_EMAIL = "support@company.com"

SAMPLE_TICKETS = [
    {
        "title": "Laptop not charging",
        "description": "My laptop shows 0% even when plugged in.",
        "category": Category.HARDWARE,
        "priority": Priority.HIGH,
        "status": Status.OPEN,
        "created_at": datetime(2026, 11, 18, 3, 45, 0),
        "updated_at": datetime(2026, 11, 18, 3, 45, 0),
    },
    {
        "title": "Cannot log in to VPN",
        "description": "The VPN client connects and then disconnects before the office network opens.",
        "category": Category.NETWORK,
        "priority": Priority.HIGH,
        "status": Status.IN_PROGRESS,
        "created_at": datetime(2026, 11, 17, 5, 30, 0),
        "updated_at": datetime(2026, 11, 18, 4, 10, 0),
    },
    {
        "title": "Need access to the shared project folder",
        "description": "I need read access to the shared project folder so I can open the onboarding documents.",
        "category": Category.ACCESS,
        "priority": Priority.MEDIUM,
        "status": Status.OPEN,
        "created_at": datetime(2026, 11, 18, 4, 35, 0),
        "updated_at": datetime(2026, 11, 18, 4, 35, 0),
    },
    {
        "title": "Excel keeps crashing on startup",
        "description": "Excel closes immediately after it opens, before any workbook appears.",
        "category": Category.SOFTWARE,
        "priority": Priority.MEDIUM,
        "status": Status.RESOLVED,
        "created_at": datetime(2026, 11, 16, 9, 0, 0),
        "updated_at": datetime(2026, 11, 18, 5, 50, 0),
    },
    {
        "title": "Request a second monitor",
        "description": "I am requesting a second monitor so I can keep a spreadsheet and the ticket page open together.",
        "category": Category.HARDWARE,
        "priority": Priority.LOW,
        "status": Status.CLOSED,
        "created_at": datetime(2026, 11, 15, 3, 30, 0),
        "updated_at": datetime(2026, 11, 17, 11, 15, 0),
    },
]


def password_from_env_or_prompt(env_name: str, label: str) -> str:
    value = os.getenv(env_name) or getpass.getpass(f"{label} password: ")
    if len(value) < 8:
        raise SystemExit(f"{label} password must be at least 8 characters.")
    return value


def get_or_create_user(db, email: str, full_name: str, role: Role, password: str) -> User:
    normalized = normalize_email(email)
    user = db.scalar(select(User).where(User.email == normalized))
    if user:
        return user
    user = User(
        full_name=full_name,
        email=normalized,
        password_hash=hash_password(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def main() -> None:
    create_tables()
    employee_password = password_from_env_or_prompt("SEED_EMPLOYEE_PASSWORD", "Employee (ravi@company.com)")
    support_password = password_from_env_or_prompt("SEED_SUPPORT_PASSWORD", "Support Staff (support@company.com)")

    with SessionLocal() as db:
        ravi = get_or_create_user(db, EMPLOYEE_EMAIL, "Ravi", Role.EMPLOYEE, employee_password)
        get_or_create_user(db, SUPPORT_EMAIL, "Support Admin", Role.SUPPORT_STAFF, support_password)

        inserted = 0
        for item in SAMPLE_TICKETS:
            existing = db.scalar(
                select(Ticket).where(
                    Ticket.title == item["title"],
                    Ticket.creator_id == ravi.id,
                    Ticket.created_at == item["created_at"],
                )
            )
            if existing:
                continue
            db.add(
                Ticket(
                    title=item["title"],
                    description=item["description"],
                    category=item["category"],
                    priority=item["priority"],
                    status=item["status"],
                    creator_id=ravi.id,
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                )
            )
            inserted += 1
        db.commit()
        print(f"Sample data ready. Inserted {inserted} new ticket(s).")


if __name__ == "__main__":
    main()
