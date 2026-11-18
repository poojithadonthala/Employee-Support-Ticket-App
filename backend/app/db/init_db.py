from app.db.session import create_tables


def main() -> None:
    create_tables()
    print("Database tables are ready.")


if __name__ == "__main__":
    main()
