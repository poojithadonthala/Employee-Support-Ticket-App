from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.ticket import Ticket
from app.models.user import Role, User
from app.services.ticket_service import ticket_to_out
from scripts import seed_sample_data


def test_seed_is_idempotent_and_matches_specification(monkeypatch):
    monkeypatch.setenv("SEED_EMPLOYEE_PASSWORD", "EmployeeSeed123")
    monkeypatch.setenv("SEED_SUPPORT_PASSWORD", "SupportSeed123")

    seed_sample_data.main()
    seed_sample_data.main()

    with SessionLocal() as db:
        assert db.scalar(select(func.count(Ticket.id))) == 5
        users = db.scalars(select(User).order_by(User.id)).all()
        assert {user.email: user.role for user in users} == {
            "ravi@company.com": Role.EMPLOYEE,
            "support@company.com": Role.SUPPORT_STAFF,
        }
        tickets = db.scalars(select(Ticket).order_by(Ticket.id)).all()
        outputs = [ticket_to_out(ticket).model_dump() for ticket in tickets]

    assert [item["title"] for item in outputs] == [
        "Laptop not charging",
        "Cannot log in to VPN",
        "Need access to the shared project folder",
        "Excel keeps crashing on startup",
        "Request a second monitor",
    ]
    assert [item["status"] for item in outputs] == [
        "Open",
        "In Progress",
        "Open",
        "Resolved",
        "Closed",
    ]
    assert outputs[0]["created_at"] == "18 Nov 2026, 09:15 AM"
    assert outputs[0]["updated_at"] == "18 Nov 2026, 09:15 AM"
    assert outputs[4]["created_at"] == "15 Nov 2026, 09:00 AM"
    assert outputs[4]["updated_at"] == "17 Nov 2026, 04:45 PM"
    assert all(item["created_by"] == "Ravi" for item in outputs)
