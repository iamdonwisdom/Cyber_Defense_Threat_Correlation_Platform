import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "database" / "database.db"
SCHEMA = BASE_DIR / "database" / "schema.sql"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    with open(SCHEMA, "r") as schema_file:
        conn.executescript(schema_file.read())

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
