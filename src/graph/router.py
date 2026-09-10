MAX_RETRIES = 3
MIN_QUALITY_SCORE = 0.85


def route_after_validation(state):
    """
    Decide whether the generated post is good enough
    or needs to be regenerated.
    """

    quality_score = state.get(
        "quality_score",
        0.0,
    )

    is_valid = (
        state.get("is_ai_ml", False)
        and state.get("technically_sound", False)
        and state.get("professional", False)
        and state.get("recruiter_relevant", False)
        and state.get("engineer_relevant", False)
        and state.get("grammar_ok", False)
        and quality_score >= MIN_QUALITY_SCORE
    )

    if is_valid:
        return "duplicate_check"

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count < MAX_RETRIES:
        return "writer"

    return "failed"


def route_after_duplicate_check(state):
    """
    Reject duplicate content and regenerate it.
    """

    if not state.get(
        "is_duplicate",
        False,
    ):
        return "publish"

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count < MAX_RETRIES:
        return "writer"

    return "failed"