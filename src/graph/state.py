from typing import TypedDict


class LinkedInState(TypedDict, total=False):

    execution_key: str
    execution_status: str
    topic: str
    subtopic: str
    angle: str

    research: str
    generated_post: str

    # Validation
    is_ai_ml: bool
    technically_sound: bool
    professional: bool
    recruiter_relevant: bool
    engineer_relevant: bool
    grammar_ok: bool
    quality_score: float
    validation_feedback: str

    # Duplicate detection
    is_duplicate: bool
    duplicate_score: float

    # Retry
    retry_count: int

    # LinkedIn
    linkedin_post_id: str

    status: str

