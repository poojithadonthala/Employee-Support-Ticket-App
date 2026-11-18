from fastapi import HTTPException

from app.core.time import utc_now
from app.models.ticket import Category, Priority, Status


def bad_request(message: str) -> HTTPException:
    return HTTPException(status_code=400, detail=message)


def trim(value: str | None) -> str:
    return value.strip() if isinstance(value, str) else ""


def normalize_email(value: str | None) -> str:
    return trim(value).lower()


def validate_full_name(value: str | None) -> str:
    name = trim(value)
    if not name:
        raise bad_request("Full name is required.")
    return name


def validate_email_format(value: str | None) -> str:
    email = trim(value)
    if not email:
        raise bad_request("Email is required.")
    if email.count("@") != 1:
        raise bad_request("Enter a valid email address.")

    local, domain = email.split("@")
    if not local or any(char.isspace() for char in local):
        raise bad_request("Enter a valid email address.")
    if not domain or any(char.isspace() for char in domain):
        raise bad_request("Enter a valid email address.")
    if domain.startswith(".") or domain.endswith("."):
        raise bad_request("Enter a valid email address.")

    parts = domain.split(".")
    if len(parts) < 2 or any(not part for part in parts):
        raise bad_request("Enter a valid email address.")
    return normalize_email(email)


def validate_password(value: str | None) -> str:
    if not isinstance(value, str) or len(value) < 8:
        raise bad_request("Password must be at least 8 characters.")
    return value


def validate_confirm_password(password: str, confirm_password: str | None) -> None:
    if not isinstance(confirm_password, str) or confirm_password != password:
        raise bad_request("Passwords do not match.")


def validate_title(value: str | None) -> str:
    title = trim(value)
    if not title:
        raise bad_request("Title is required.")
    if len(title) > 100:
        raise bad_request("Title must be 100 characters or fewer.")
    return title


def validate_description(value: str | None) -> str:
    description = trim(value)
    if not description:
        raise bad_request("Description is required.")
    if len(description) > 2000:
        raise bad_request("Description must be 2,000 characters or fewer.")
    return description


def validate_category(value: str | None) -> str:
    category = trim(value)
    if category not in {item.value for item in Category}:
        raise bad_request("Category must be Hardware, Software, Network, Access, or Other.")
    return category


def validate_priority(value: str | None) -> str:
    priority = trim(value)
    if priority not in {item.value for item in Priority}:
        raise bad_request("Priority must be Low, Medium, or High.")
    return priority


def validate_status(value: str | None) -> str:
    status = trim(value)
    if status not in {item.value for item in Status}:
        raise bad_request("Status must be Open, In Progress, Resolved, or Closed.")
    return status


def validate_ticket_fields(
    title: str | None,
    description: str | None,
    category: str | None,
    priority: str | None,
) -> dict[str, str]:
    return {
        "title": validate_title(title),
        "description": validate_description(description),
        "category": validate_category(category),
        "priority": validate_priority(priority),
    }


def validate_enum_filter(value: str | None, allowed: set[str], label: str) -> str | None:
    cleaned = trim(value)
    if not cleaned:
        return None
    if cleaned not in allowed:
        raise bad_request(f"{label} filter is invalid.")
    return cleaned


def now_for_storage():
    return utc_now()
