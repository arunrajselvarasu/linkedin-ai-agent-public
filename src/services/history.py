import sqlite3
from pathlib import Path
from typing import Any


DATABASE_FILE = Path("data/linkedin_agent.db")


def get_connection():
    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            topic TEXT,
            subtopic TEXT,
            angle TEXT,
            linkedin_post_id TEXT,
            quality_score REAL,
            duplicate_score REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # --------------------------------------------------------
    # IDEMPOTENCY TABLE
    # --------------------------------------------------------

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS executions (
            execution_key TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()
    connection.close()


# ============================================================
# POST HISTORY
# ============================================================

def load_history() -> list[dict[str, Any]]:
    initialize_database()

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            content,
            topic,
            subtopic,
            angle,
            linkedin_post_id,
            quality_score,
            duplicate_score,
            status,
            created_at
        FROM posts
        ORDER BY id ASC
        """
    ).fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


def save_post(post_data: dict[str, Any]):
    initialize_database()

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO posts (
            content,
            topic,
            subtopic,
            angle,
            linkedin_post_id,
            quality_score,
            duplicate_score,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            post_data.get("content"),
            post_data.get("topic"),
            post_data.get("subtopic"),
            post_data.get("angle"),
            post_data.get("linkedin_post_id"),
            post_data.get("quality_score"),
            post_data.get("duplicate_score"),
            post_data.get("status"),
        ),
    )

    connection.commit()
    connection.close()


# ============================================================
# IDEMPOTENCY
# ============================================================

def claim_execution(execution_key: str) -> bool:
    """
    Atomically claim an execution.

    Returns:
        True  -> this execution is new
        False -> execution already exists
    """

    initialize_database()

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO executions (
                execution_key,
                status
            )
            VALUES (?, ?)
            """,
            (
                execution_key,
                "started",
            ),
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:
        # Same execution_key already exists.
        connection.rollback()

        return False

    finally:
        connection.close()


def update_execution_status(
    execution_key: str,
    status: str,
):
    """
    Update execution status.
    """

    initialize_database()

    connection = get_connection()

    connection.execute(
        """
        UPDATE executions
        SET status = ?
        WHERE execution_key = ?
        """,
        (
            status,
            execution_key,
        ),
    )

    connection.commit()
    connection.close()