from src.graph.router import (
    route_after_validation,
    route_after_duplicate_check,
)


def test_validation_failure_regenerates():
    state = {
        "is_ai_ml": False,
        "technically_sound": True,
        "professional": True,
        "recruiter_relevant": True,
        "engineer_relevant": True,
        "grammar_ok": True,
        "quality_score": 0.50,
        "retry_count": 0,
    }

    result = route_after_validation(state)

    assert result == "regenerate"


def test_validation_failure_after_max_retries_fails():
    state = {
        "is_ai_ml": False,
        "technically_sound": True,
        "professional": True,
        "recruiter_relevant": True,
        "engineer_relevant": True,
        "grammar_ok": True,
        "quality_score": 0.50,
        "retry_count": 3,
    }

    result = route_after_validation(state)

    assert result == "failed"


def test_duplicate_regenerates():
    state = {
        "is_duplicate": True,
        "retry_count": 0,
    }

    result = route_after_duplicate_check(state)

    assert result == "regenerate"


def test_duplicate_after_max_retries_fails():
    state = {
        "is_duplicate": True,
        "retry_count": 3,
    }

    result = route_after_duplicate_check(state)

    assert result == "failed"


def test_valid_post_goes_to_duplicate_check():
    state = {
        "is_ai_ml": True,
        "technically_sound": True,
        "professional": True,
        "recruiter_relevant": True,
        "engineer_relevant": True,
        "grammar_ok": True,
        "quality_score": 0.90,
        "retry_count": 0,
    }

    result = route_after_validation(state)

    assert result == "duplicate_check"


def test_unique_post_goes_to_publish():
    state = {
        "is_duplicate": False,
        "retry_count": 0,
    }

    result = route_after_duplicate_check(state)

    assert result == "publish"
    