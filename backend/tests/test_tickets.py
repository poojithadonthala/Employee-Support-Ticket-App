from tests.helpers import create_ticket, login, make_support_staff, register_employee


def test_employee_can_create_and_read_own_tickets(client):
    register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(
        client,
        title="  Printer jammed  ",
        description="  The printer shows a paper jam error.  ",
        category="Hardware",
        priority="Medium",
    )
    assert ticket["status"] == "Open"
    assert ticket["title"] == "Printer jammed"
    assert ticket["description"] == "The printer shows a paper jam error."
    assert ticket["created_by"] == "Test Employee"
    assert ", " in ticket["created_at"] and "AM" in ticket["created_at"] or "PM" in ticket["created_at"]

    detail = client.get(f"/api/tickets/{ticket['id']}")
    assert detail.status_code == 200
    assert detail.json() == ticket

    listing = client.get("/api/employee/tickets")
    assert listing.status_code == 200
    assert [item["id"] for item in listing.json()] == [ticket["id"]]


def test_ticket_creation_validation(client):
    register_employee(client)
    login(client, "employee@example.com")
    valid = {
        "title": "Valid title",
        "description": "Valid description",
        "category": "Software",
        "priority": "Low",
    }
    cases = [
        {**valid, "title": ""},
        {**valid, "title": "x" * 101},
        {**valid, "description": ""},
        {**valid, "description": "x" * 2001},
        {**valid, "category": "Unknown"},
        {**valid, "priority": "Urgent"},
    ]
    for payload in cases:
        response = client.post("/api/tickets", json=payload)
        assert response.status_code == 400, response.text
    assert client.get("/api/employee/tickets").json() == []


def test_employee_cannot_see_or_edit_another_employees_ticket(client):
    register_employee(client, "one@example.com")
    login(client, "one@example.com")
    own = create_ticket(client)
    client.post("/api/auth/logout")

    register_employee(client, "two@example.com")
    login(client, "two@example.com")
    other_id = own["id"]

    detail = client.get(f"/api/tickets/{other_id}")
    assert detail.status_code == 403
    assert "Laptop issue" not in detail.text

    edit = client.patch(
        f"/api/tickets/{other_id}",
        json={
            "title": "Hacked",
            "description": "Hacked",
            "category": "Other",
            "priority": "Low",
        },
    )
    assert edit.status_code == 403

    own_list = client.get("/api/employee/tickets")
    assert own_list.json() == []


def test_missing_ticket_returns_404_before_authorization(client):
    register_employee(client)
    login(client, "employee@example.com")
    assert client.get("/api/tickets/999").status_code == 404

    edit = client.patch(
        "/api/tickets/999",
        json={
            "title": "x",
            "description": "x",
            "category": "Other",
            "priority": "Low",
        },
    )
    assert edit.status_code == 404

    status = client.post("/api/tickets/999/status", json={"status": "In Progress"})
    assert status.status_code == 404


def test_employee_can_edit_permitted_fields_and_cannot_change_status(client):
    register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(client)

    edit = client.patch(
        f"/api/tickets/{ticket['id']}",
        json={
            "title": "  Updated title  ",
            "description": "  Updated description  ",
            "category": "Network",
            "priority": "Low",
            "status": "Closed",
            "creator_id": 999,
        },
    )
    assert edit.status_code == 200
    updated = edit.json()
    assert updated["title"] == "Updated title"
    assert updated["description"] == "Updated description"
    assert updated["category"] == "Network"
    assert updated["priority"] == "Low"
    assert updated["status"] == "Open"

    status = client.post(f"/api/tickets/{ticket['id']}/status", json={"status": "In Progress"})
    assert status.status_code == 403
    assert client.get(f"/api/tickets/{ticket['id']}").json()["status"] == "Open"


def test_closed_ticket_cannot_be_edited(client):
    register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(client)
    make_support_staff()
    client.post("/api/auth/logout")
    login(client, "support@example.com")

    for target in ["In Progress", "Resolved", "Closed"]:
        response = client.post(f"/api/tickets/{ticket['id']}/status", json={"status": target})
        assert response.status_code == 200, response.text

    client.post("/api/auth/logout")
    login(client, "employee@example.com")
    before = client.get(f"/api/tickets/{ticket['id']}").json()
    edit = client.patch(
        f"/api/tickets/{ticket['id']}",
        json={
            "title": "Cannot edit",
            "description": "Cannot edit",
            "category": "Other",
            "priority": "Low",
        },
    )
    assert edit.status_code == 403
    assert client.get(f"/api/tickets/{ticket['id']}").json() == before
