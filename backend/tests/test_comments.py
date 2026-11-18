from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.comment import Comment
from tests.helpers import create_ticket, login, make_support_staff, register_employee


def advance_to_closed(client, ticket_id):
    for target in ["In Progress", "Resolved", "Closed"]:
        response = client.post(f"/api/tickets/{ticket_id}/status", json={"status": target})
        assert response.status_code == 200, response.text
    return client.get(f"/api/tickets/{ticket_id}").json()


def test_employee_can_add_and_view_own_ticket_comments(client):
    employee = register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(client)
    ticket_id = ticket["id"]
    before = client.get(f"/api/tickets/{ticket_id}").json()

    response = client.post(
        f"/api/tickets/{ticket_id}/comments",
        json={"content": "  Please check the power cable.  "},
    )
    assert response.status_code == 201, response.text
    created = response.json()
    assert created["ticket_id"] == ticket_id
    assert created["author_id"] == employee["id"]
    assert created["author"] == "Test Employee"
    assert created["author_role"] == "Employee"
    assert created["content"] == "Please check the power cable."
    assert isinstance(created["id"], int) and created["id"] > 0
    assert ", " in created["created_at"]

    with SessionLocal() as db:
        stored = db.scalar(select(Comment).where(Comment.id == created["id"]))
        assert stored is not None
        assert stored.ticket_id == ticket_id
        assert stored.author_id == employee["id"]
        assert stored.content == "Please check the power cable."
        assert stored.created_at is not None

    listing = client.get(f"/api/tickets/{ticket_id}/comments")
    assert listing.status_code == 200
    assert [item["id"] for item in listing.json()] == [created["id"]]

    after = client.get(f"/api/tickets/{ticket_id}").json()
    assert after["status"] == before["status"] == "Open"
    assert after["updated_at"] == before["updated_at"]


def test_support_can_comment_on_closed_ticket_and_both_roles_view_comments(client):
    register_employee(client, "ravi@example.com", "Ravi")
    login(client, "ravi@example.com")
    ticket = create_ticket(client)
    ticket_id = ticket["id"]

    employee_comment = client.post(
        f"/api/tickets/{ticket_id}/comments", json={"content": "I have tried restarting it."}
    )
    assert employee_comment.status_code == 201, employee_comment.text

    make_support_staff()
    client.post("/api/auth/logout")
    login(client, "support@example.com")
    closed = advance_to_closed(client, ticket_id)
    assert closed["status"] == "Closed"

    support_comment = client.post(
        f"/api/tickets/{ticket_id}/comments", json={"content": "  Closed after confirmation.  "}
    )
    assert support_comment.status_code == 201, support_comment.text
    created = support_comment.json()
    assert created["author"] == "Test Support"
    assert created["author_role"] == "Support Staff"
    assert created["content"] == "Closed after confirmation."

    support_view = client.get(f"/api/tickets/{ticket_id}/comments")
    assert support_view.status_code == 200
    assert [item["content"] for item in support_view.json()] == [
        "I have tried restarting it.",
        "Closed after confirmation.",
    ]

    after = client.get(f"/api/tickets/{ticket_id}").json()
    assert after["status"] == "Closed"
    assert after["updated_at"] == closed["updated_at"]

    client.post("/api/auth/logout")
    login(client, "ravi@example.com")
    employee_view = client.get(f"/api/tickets/{ticket_id}/comments")
    assert employee_view.status_code == 200
    assert [item["content"] for item in employee_view.json()] == [
        "I have tried restarting it.",
        "Closed after confirmation.",
    ]


def test_employee_cannot_access_another_employees_comments(client):
    register_employee(client, "owner@example.com", "Owner")
    login(client, "owner@example.com")
    ticket = create_ticket(client)
    ticket_id = ticket["id"]
    posted = client.post(
        f"/api/tickets/{ticket_id}/comments", json={"content": "Private owner note"}
    )
    assert posted.status_code == 201, posted.text

    client.post("/api/auth/logout")
    register_employee(client, "other@example.com", "Other")
    login(client, "other@example.com")

    listing = client.get(f"/api/tickets/{ticket_id}/comments")
    assert listing.status_code == 403
    assert "Private owner note" not in listing.text

    add = client.post(f"/api/tickets/{ticket_id}/comments", json={"content": "Intrusion"})
    assert add.status_code == 403
    assert "Intrusion" not in add.text


def test_comment_validation_rejects_empty_or_invalid_content(client):
    register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(client)
    ticket_id = ticket["id"]
    before = client.get(f"/api/tickets/{ticket_id}").json()

    invalid_payloads = [
        {"content": ""},
        {"content": "   \n\t  "},
        {},
        {"content": None},
        {"content": 123},
        ["not", "an", "object"],
    ]
    for payload in invalid_payloads:
        response = client.post(f"/api/tickets/{ticket_id}/comments", json=payload)
        assert response.status_code == 400, (payload, response.text)

    assert client.get(f"/api/tickets/{ticket_id}/comments").json() == []
    assert client.get(f"/api/tickets/{ticket_id}").json() == before

    client.post("/api/auth/logout")
    assert client.get(f"/api/tickets/{ticket_id}/comments").status_code == 401
    assert (
        client.post(f"/api/tickets/{ticket_id}/comments", json={"content": "Anonymous"}).status_code
        == 401
    )


def test_comments_are_returned_in_chronological_order(client):
    register_employee(client)
    login(client, "employee@example.com")
    ticket = create_ticket(client)
    ticket_id = ticket["id"]

    ids = []
    for index in range(3):
        response = client.post(
            f"/api/tickets/{ticket_id}/comments", json={"content": f"Comment {index}"}
        )
        assert response.status_code == 201, response.text
        ids.append(response.json()["id"])

    listing = client.get(f"/api/tickets/{ticket_id}/comments")
    assert listing.status_code == 200
    comments = listing.json()
    assert [item["content"] for item in comments] == ["Comment 0", "Comment 1", "Comment 2"]
    assert [item["id"] for item in comments] == ids


def test_missing_ticket_returns_404_before_comment_validation(client):
    register_employee(client)
    login(client, "employee@example.com")

    listing = client.get("/api/tickets/99999/comments")
    assert listing.status_code == 404

    add = client.post("/api/tickets/99999/comments", json={"content": "   "})
    assert add.status_code == 404
