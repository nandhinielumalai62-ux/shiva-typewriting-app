"""Initialize MySQL database, create tables from sql/schema.sql, and load seed data."""
from config import Config
from db import init_db_schema
from seed_data import seed_initial_data


def main():
    print(f"Initializing database ({Config.DB_BACKEND})...")
    init_db_schema()
    seed_initial_data()
    print("Database schema and initial Practice 1..N passages & Admin account are ready!")
    print("Default Admin Login -> ID: admin | Password: admin123")


if __name__ == "__main__":
    main()
