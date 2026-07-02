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
def get_recent_logs(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    logs = cursor.execute("""
        SELECT timestamp, severity, source, raw_log
        FROM logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return logs

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    total_logs = cursor.execute(
        "SELECT COUNT(*) FROM logs"
    ).fetchone()[0]

    warnings = cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE severity='Warning'"
    ).fetchone()[0]

    errors = cursor.execute(
        "SELECT COUNT(*) FROM logs WHERE severity='Error'"
    ).fetchone()[0]

    conn.close()

    return {
        "total_logs": total_logs,
        "warnings": warnings,
        "errors": errors
    }


def save_log(log_entry):
    conn = get_connection()
    cursor = conn.cursor()

    # Detect severity from the log entry
    if "ERROR" in log_entry:
        severity = "Error"
    elif "WARNING" in log_entry:
        severity = "Warning"
    else:
        severity = "Info"

    cursor.execute("""
        INSERT INTO logs (
            timestamp,
            source,
            event_type,
            severity,
            raw_log
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        "Unknown",
        "Uploaded File",
        "Log Entry",
        severity,
        log_entry
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
