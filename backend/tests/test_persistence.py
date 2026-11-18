from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.db.session import create_tables
from app.models.ticket import Ticket
from app.models.user import Role, User
from tests.helpers import create_ticket, login, register_employee


def test_records_survive_a_new_database_connection(client):
    register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(client, title="Persistent ticket")

    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    )
    with Session(engine) as db:
        stored = db.scalar(select(User).where(User.email == "employee@example.com"))
        assert stored is not None
        assert stored.role == Role.EMPLOYEE
        assert verify_password(stored.password_hash, "Password123")
        stored_ticket = db.get(Ticket, ticket["id"])
        assert stored_ticket is not None
        assert stored_ticket.title == "Persistent ticket"
    engine.dispose()


def test_database_tables_include_required_constraints():
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    )
    create_tables()
    with engine.connect() as connection:
        if settings.database_url.startswith("sqlite"):
            ticket_sql = connection.exec_driver_sql(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='tickets'"
            ).scalar_one()
            assert "NOT NULL" in ticket_sql
            assert "FOREIGN KEY(creator_id)" in ticket_sql
            assert "CHECK" in ticket_sql
            email_index_sql = connection.exec_driver_sql(
                "SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='users' AND name LIKE '%email%'"
            ).scalar_one()
            assert "UNIQUE" in email_index_sql
    engine.dispose()
