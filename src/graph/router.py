from src.graph.state import LinkedInState


MAX_RETRIES = 3
MIN_QUALITY_SCORE = 0.85


def route_after_validation(
    state: LinkedInState,
) -> str:
    """
    Decide whether the generated post should be
    regenerated or checked for duplicates.
    """

    quality_score = state.get(
        "quality_score",
        0.0,
    )

    is_ai_ml = state.get(
        "is_ai_ml",
        False,
    )

    technically_sound = state.get(
        "technically_sound",
        False,
    )

    professional = state.get(
        "professional",
        False,
    )

    recruiter_relevant = state.get(
        "recruiter_relevant",
        False,
    )

    engineer_relevant = state.get(
        "engineer_relevant",
        False,
    )

    grammar_ok = state.get(
        "grammar_ok",
        False,
    )

    retry_count = state.get(
        "retry_count",
        0,
    )

    validation_passed = (
        is_ai_ml
        and technically_sound
        and professional
        and recruiter_relevant
        and engineer_relevant
        and grammar_ok
        and quality_score >= MIN_QUALITY_SCORE
    )

    if not validation_passed:

        if retry_count >= MAX_RETRIES:
            return "failed"

        return "regenerate"

    return "duplicate_check"


def route_after_duplicate_check(
    state: LinkedInState,
) -> str:
    """
    Decide whether to publish or regenerate
    after duplicate detection.
    """

    is_duplicate = state.get(
        "is_duplicate",
        False,
    )

    retry_count = state.get(
        "retry_count",
        0,
    )

    if is_duplicate:

        if retry_count >= MAX_RETRIES:
            return "failed"

        return "regenerate"

    return "publish"