from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import Role, User


def register_employee(
    client: TestClient,
    email: str = "employee@example.com",
    full_name: str = "Test Employee",
) -> dict:
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": "Password123",
            "confirm_password": "Password123",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def login(client: TestClient, email: str, password: str = "Password123") -> dict:
    response = client.post("/api/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def make_support_staff(email: str = "support@example.com") -> User:
    user = User(
        full_name="Test Support",
        email=email,
        password_hash=hash_password("Password123"),
        role=Role.SUPPORT_STAFF,
    )
    with SessionLocal() as db:
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def create_ticket(client: TestClient, **overrides) -> dict:
    payload = {
        "title": "Laptop issue",
        "description": "The laptop will not start.",
        "category": "Hardware",
        "priority": "High",
    }
    payload.update(overrides)
    response = client.post("/api/tickets", json=payload)
    assert response.status_code == 201, response.text
    return response.json()
