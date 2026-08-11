import sqlite3
import json
from pathlib import Path


DATABASE_FILE = Path(__file__).parent / "phishshield.db"


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            status TEXT NOT NULL,
            reasons TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_scan(
    url: str,
    risk_score: int,
    status: str,
    reasons: list
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO scan_history
        (url, risk_score, status, reasons)
        VALUES (?, ?, ?, ?)
        """,
        (
            url,
            risk_score,
            status,
            json.dumps(reasons)
        )
    )

    connection.commit()

    scan_id = cursor.lastrowid

    connection.close()

    return scan_id


def get_scan_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            url,
            risk_score,
            status,
            reasons,
            created_at
        FROM scan_history
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:
        history.append({
            "id": row[0],
            "url": row[1],
            "risk_score": row[2],
            "status": row[3],
            "reasons": json.loads(row[4]) if row[4] else [],
            "created_at": row[5]
        })

    return history


def delete_scan(scan_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM scan_history
        WHERE id = ?
        """,
        (scan_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted > 0


def clear_scan_history():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM scan_history")

    connection.commit()

    deleted_count = cursor.rowcount

    connection.close()

    return deleted_count

