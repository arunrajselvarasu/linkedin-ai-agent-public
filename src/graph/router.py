MAX_RETRIES = 3
MIN_QUALITY_SCORE = 0.85


def route_after_validation(state):
    """
    Decide what happens after validation.

    Valid post:
        → duplicate_check

    Invalid post:
        → regenerate

    Maximum retries:
        → failed
    """

    quality_score = state.get(
        "quality_score",
        0.0,
    )

    validation_passed = (
        state.get("is_ai_ml", False)
        and state.get("technically_sound", False)
        and state.get("professional", False)
        and state.get("recruiter_relevant", False)
        and state.get("engineer_relevant", False)
        and state.get("grammar_ok", False)
        and quality_score >= MIN_QUALITY_SCORE
    )

    # --------------------------------------------------------
    # VALIDATION PASSED
    # --------------------------------------------------------

    if validation_passed:
        print(
            "✅ Validation passed"
        )

        return "duplicate_check"

    # --------------------------------------------------------
    # VALIDATION FAILED
    # --------------------------------------------------------

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count < MAX_RETRIES:
        print(
            f"🔄 Validation failed. "
            f"Regeneration required: "
            f"{retry_count + 1}/{MAX_RETRIES}"
        )

        return "regenerate"

    # --------------------------------------------------------
    # MAX RETRIES
    # --------------------------------------------------------

    print(
        "❌ Maximum validation retries reached."
    )

    return "failed"


def route_after_duplicate_check(state):
    """
    Decide what happens after duplicate detection.

    Unique:
        → publish

    Duplicate:
        → regenerate

    Maximum retries:
        → failed
    """

    is_duplicate = state.get(
        "is_duplicate",
        False,
    )

    # --------------------------------------------------------
    # UNIQUE POST
    # --------------------------------------------------------

    if not is_duplicate:
        print(
            "✅ Duplicate check passed"
        )

        return "publish"

    # --------------------------------------------------------
    # DUPLICATE DETECTED
    # --------------------------------------------------------

    retry_count = state.get(
        "retry_count",
        0,
    )

    if retry_count < MAX_RETRIES:
        print(
            f"🔄 Duplicate detected. "
            f"Regeneration required: "
            f"{retry_count + 1}/{MAX_RETRIES}"
        )

        return "regenerate"

    # --------------------------------------------------------
    # MAX RETRIES
    # --------------------------------------------------------

    print(
        "❌ Maximum duplicate retries reached."
    )

    return "failed"