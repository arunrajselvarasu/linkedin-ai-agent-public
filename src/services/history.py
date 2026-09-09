import json
from pathlib import Path
from typing import Any


HISTORY_FILE = Path("data/posts.json")


def _load_data() -> dict[str, Any]:
    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not HISTORY_FILE.exists():
        data = {
            "posts": [],
            "executions": {},
        }

        HISTORY_FILE.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

        return data

    try:
        return json.loads(
            HISTORY_FILE.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError:
        return {
            "posts": [],
            "executions": {},
        }


def _save_data(data: dict[str, Any]):
    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    HISTORY_FILE.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


# ============================================================
# POST HISTORY
# ============================================================

def load_history() -> list[dict[str, Any]]:
    data = _load_data()

    return data.get(
        "posts",
        [],
    )


def save_post(post_data: dict[str, Any]):
    data = _load_data()

    post = {
        "content": post_data.get("content"),
        "topic": post_data.get("topic"),
        "subtopic": post_data.get("subtopic"),
        "angle": post_data.get("angle"),
        "linkedin_post_id": post_data.get("linkedin_post_id"),
        "quality_score": post_data.get("quality_score"),
        "duplicate_score": post_data.get("duplicate_score"),
        "status": post_data.get("status"),
    }

    data.setdefault(
        "posts",
        [],
    ).append(post)

    _save_data(data)


# ============================================================
# IDEMPOTENCY
# ============================================================

def claim_execution(execution_key: str) -> bool:
    """
    Claim an execution key.

    Returns:
        True  -> execution is new
        False -> execution already exists
    """

    data = _load_data()

    executions = data.setdefault(
        "executions",
        {},
    )

    if execution_key in executions:
        return False

    executions[execution_key] = {
        "status": "started",
    }

    _save_data(data)

    return True


def update_execution_status(
    execution_key: str,
    status: str,
):
    """
    Update the execution status.
    """

    data = _load_data()

    executions = data.setdefault(
        "executions",
        {},
    )

    if execution_key in executions:
        executions[execution_key]["status"] = status

    _save_data(data)