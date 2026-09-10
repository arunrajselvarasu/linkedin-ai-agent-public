import json

from src.services import history


def test_claim_execution_only_once(tmp_path, monkeypatch):
    history_file = tmp_path / "posts.json"

    monkeypatch.setattr(history, "HISTORY_FILE", history_file)

    assert history.claim_execution("test-morning") is True
    assert history.claim_execution("test-morning") is False


def test_execution_status_update(tmp_path, monkeypatch):
    history_file = tmp_path / "posts.json"

    monkeypatch.setattr(history, "HISTORY_FILE", history_file)

    history.claim_execution("test-evening")
    history.update_execution_status("test-evening", "completed")

    data = json.loads(history_file.read_text())

    assert data["executions"]["test-evening"]["status"] == "completed"


def test_save_post(tmp_path, monkeypatch):
    history_file = tmp_path / "posts.json"

    monkeypatch.setattr(history, "HISTORY_FILE", history_file)

    history.save_post(
        {
            "content": "Test AI engineering post",
            "topic": "RAG",
            "subtopic": "Hybrid Retrieval",
            "angle": "Practical engineering",
            "quality_score": 0.92,
            "duplicate_score": 0.10,
            "status": "dry_run",
        }
    )

    posts = history.load_history()

    assert len(posts) == 1
    assert posts[0]["content"] == "Test AI engineering post"
    assert posts[0]["status"] == "dry_run"