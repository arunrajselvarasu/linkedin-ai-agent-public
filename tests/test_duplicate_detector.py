from unittest.mock import patch

from src.services.duplicate_detector import (
    DUPLICATE_THRESHOLD,
    calculate_similarity,
    check_duplicate,
)


def test_no_previous_posts():
    result = calculate_similarity(
        "A new AI engineering post",
        [],
    )

    assert result == 0.0


def test_similar_posts_have_high_similarity():
    previous_posts = [
        "RAG systems improve retrieval using vector databases and embeddings."
    ]

    score = calculate_similarity(
        "RAG systems improve retrieval with vector databases and embeddings.",
        previous_posts,
    )

    assert score >= 0.70


def test_different_posts_have_low_similarity():
    previous_posts = [
        "RAG systems improve retrieval using vector databases and embeddings."
    ]

    score = calculate_similarity(
        "Python automation can simplify repetitive infrastructure operations.",
        previous_posts,
    )

    assert score < DUPLICATE_THRESHOLD


@patch("src.services.duplicate_detector.load_history")
def test_check_duplicate_detects_duplicate(mock_load_history):
    mock_load_history.return_value = [
        {
            "content": (
                "RAG systems improve retrieval using vector databases "
                "and embeddings."
            ),
            "status": "dry_run",
        }
    ]

    is_duplicate, score = check_duplicate(
        "RAG systems improve retrieval using vector databases and embeddings."
    )

    assert is_duplicate is True
    assert score >= DUPLICATE_THRESHOLD


@patch("src.services.duplicate_detector.load_history")
def test_check_duplicate_accepts_new_content(mock_load_history):
    mock_load_history.return_value = [
        {
            "content": (
                "RAG systems improve retrieval using vector databases "
                "and embeddings."
            ),
            "status": "dry_run",
        }
    ]

    is_duplicate, score = check_duplicate(
        "Python automation can simplify repetitive infrastructure operations."
    )

    assert is_duplicate is False
    assert score < DUPLICATE_THRESHOLD
    