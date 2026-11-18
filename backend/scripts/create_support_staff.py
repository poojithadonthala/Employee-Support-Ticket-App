import getpass
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select  # noqa: E402

from app.core.security import hash_password  # noqa: E402
from app.core.time import utc_now  # noqa: E402
from app.core.validation import normalize_email, validate_email_format, validate_full_name  # noqa: E402
from app.db.session import SessionLocal, create_tables  # noqa: E402
from app.models.user import Role, User  # noqa: E402


def main() -> None:
    create_tables()
    name = os.getenv("SUPPORT_STAFF_NAME") or input("Support staff full name: ")
    email = validate_email_format(os.getenv("SUPPORT_STAFF_EMAIL") or input("Support staff email: "))
    password = os.getenv("SUPPORT_STAFF_PASSWORD") or getpass.getpass("Support staff password: ")
    name = validate_full_name(name)
    if len(password) < 8:
        raise SystemExit("Support staff password must be at least 8 characters.")

    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.email == email))
        if existing:
            print(f"Support staff account already exists for {email}. No changes made.")
            return
        user = User(
            full_name=name,
            email=normalize_email(email),
            password_hash=hash_password(password),
            role=Role.SUPPORT_STAFF,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        db.add(user)
        db.commit()
        print(f"Support staff account created for {user.email}.")


if __name__ == "__main__":
    main()
