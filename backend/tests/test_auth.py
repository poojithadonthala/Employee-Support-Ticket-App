from tests.helpers import login, register_employee


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_registration_trims_fields_lowercases_email_and_ignores_role(client):
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "  Anita Rao  ",
            "email": "  ANITA.RAO@Example.COM ",
            "password": "Password123",
            "confirm_password": "Password123",
            "role": "Support Staff",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["full_name"] == "Anita Rao"
    assert body["email"] == "anita.rao@example.com"
    assert body["role"] == "Employee"
    assert "password" not in body
    assert "password_hash" not in body


def test_registration_rejects_invalid_input(client):
    base = {
        "full_name": "Anita Rao",
        "email": "anita@example.com",
        "password": "Password123",
        "confirm_password": "Password123",
    }
    cases = [
        {**base, "full_name": "   "},
        {**base, "email": "not-an-email"},
        {**base, "password": "short"},
        {**base, "confirm_password": "Different123"},
    ]
    for payload in cases:
        response = client.post("/api/auth/register", json=payload)
        assert response.status_code == 400, response.text


def test_duplicate_registration_is_case_insensitive(client):
    register_employee(client, "Same@Example.com")
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Another Person",
            "email": "same@example.com",
            "password": "Password123",
            "confirm_password": "Password123",
        },
    )
    assert response.status_code == 400


def test_login_requires_both_fields_and_rejects_bad_password(client):
    register_employee(client)
    missing = client.post("/api/auth/login", json={"email": "employee@example.com"})
    assert missing.status_code == 400

    wrong = client.post(
        "/api/auth/login",
        json={"email": "employee@example.com", "password": "WrongPassword"},
    )
    assert wrong.status_code == 401


def test_login_accepts_mixed_case_email_and_protects_me_and_logout(client):
    register_employee(client, "Employee@Example.com")
    assert client.get("/api/auth/me").status_code == 401

    body = login(client, "  EMPLOYEE@EXAMPLE.COM  ")
    assert body["role"] == "Employee"

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == "employee@example.com"

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 204
    assert client.get("/api/auth/me").status_code == 401
