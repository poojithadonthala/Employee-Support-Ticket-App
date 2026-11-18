from urllib.parse import quote

from tests.helpers import create_ticket, login, make_support_staff, register_employee


def support_client(client):
    register_employee(client, "ravi@example.com", "Ravi")
    login(client, "ravi@example.com")
    tickets = [
        create_ticket(
            client,
            title="Laptop not charging",
            description="Battery will not hold charge.",
            category="Hardware",
            priority="High",
        ),
        create_ticket(
            client,
            title="VPN disconnecting",
            description="The office network drops after login.",
            category="Network",
            priority="Medium",
        ),
    ]
    client.post("/api/auth/logout")
    make_support_staff()
    login(client, "support@example.com")
    return tickets


def test_support_staff_sees_all_tickets_and_dashboard_counts(client):
    tickets = support_client(client)
    response = client.get("/api/support/tickets")
    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {ticket["id"] for ticket in tickets}

    dashboard = client.get("/api/support/dashboard")
    assert dashboard.status_code == 200
    assert dashboard.json() == {
        "total": 2,
        "open": 2,
        "in_progress": 0,
        "resolved": 0,
        "closed": 0,
    }


def test_employee_cannot_use_support_endpoints(client):
    register_employee(client)
    login(client, "employee@example.com")
    assert client.get("/api/support/tickets").status_code == 403
    assert client.get("/api/support/dashboard").status_code == 403


def test_search_and_filters(client):
    support_client(client)
    assert [t["title"] for t in client.get("/api/support/tickets?search=laptop").json()] == [
        "Laptop not charging"
    ]
    assert [t["title"] for t in client.get("/api/support/tickets?search=office network").json()] == [
        "VPN disconnecting"
    ]
    assert [t["title"] for t in client.get("/api/support/tickets?search=Ravi").json()] == [
        "VPN disconnecting",
        "Laptop not charging",
    ]
    assert [t["title"] for t in client.get("/api/support/tickets?category=Network").json()] == [
        "VPN disconnecting"
    ]
    combined = client.get("/api/support/tickets?status=Open&category=Hardware&priority=High").json()
    assert [t["title"] for t in combined] == ["Laptop not charging"]
    assert client.get("/api/support/tickets?status=Unknown").status_code == 400


def test_search_treats_sql_like_wildcards_literally(client):
    support_client(client)
    for term in ["%", "_"]:
        response = client.get(f"/api/support/tickets?search={quote(term)}")
        assert response.status_code == 200, response.text
        assert response.json() == [], f"Search term {term!r} should match no ticket"


def test_status_transitions_only_one_step_forward(client):
    tickets = support_client(client)
    ticket_id = tickets[0]["id"]

    illegal = client.post(f"/api/tickets/{ticket_id}/status", json={"status": "Resolved"})
    assert illegal.status_code == 400
    assert client.get(f"/api/tickets/{ticket_id}").json()["status"] == "Open"

    for target in ["In Progress", "Resolved", "Closed"]:
        response = client.post(f"/api/tickets/{ticket_id}/status", json={"status": target})
        assert response.status_code == 200, response.text
        assert response.json()["status"] == target

    final = client.post(f"/api/tickets/{ticket_id}/status", json={"status": "In Progress"})
    assert final.status_code == 400
    assert client.get(f"/api/tickets/{ticket_id}").json()["status"] == "Closed"


def test_same_status_and_backward_status_are_rejected(client):
    tickets = support_client(client)
    ticket_id = tickets[0]["id"]

    same = client.post(f"/api/tickets/{ticket_id}/status", json={"status": "Open"})
    assert same.status_code == 400

    advanced = client.post(f"/api/tickets/{ticket_id}/status", json={"status": "In Progress"})
    assert advanced.status_code == 200
    backward = client.post(f"/api/tickets/{ticket_id}/status", json={"status": "Open"})
    assert backward.status_code == 400
    assert client.get(f"/api/tickets/{ticket_id}").json()["status"] == "In Progress"


def test_support_staff_cannot_edit_ticket_content(client):
    tickets = support_client(client)
    ticket_id = tickets[0]["id"]
    before = client.get(f"/api/tickets/{ticket_id}").json()

    response = client.patch(
        f"/api/tickets/{ticket_id}",
        json={
            "title": "Changed by support",
            "description": "Changed by support",
            "category": "Other",
            "priority": "Low",
        },
    )
    assert response.status_code == 403
    assert client.get(f"/api/tickets/{ticket_id}").json() == before
