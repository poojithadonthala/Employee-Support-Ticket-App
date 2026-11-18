from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

try:
    IST = ZoneInfo("Asia/Kolkata")
except ZoneInfoNotFoundError:  # pragma: no cover - fallback for stripped-down systems
    IST = timezone(timedelta(hours=5, minutes=30), name="Asia/Kolkata")


def utc_now() -> datetime:
    """Return a naive UTC timestamp for consistent cross-database storage."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def format_display(value: datetime) -> str:
    """Format a stored UTC timestamp in Asia/Kolkata as 18 Nov 2026, 09:15 AM."""
    return as_utc(value).astimezone(IST).strftime("%d %b %Y, %I:%M %p")
