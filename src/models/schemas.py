from pydantic import BaseModel, Field


class TopicSelection(BaseModel):
    topic: str
    subtopic: str
    angle: str


class ContentValidation(BaseModel):
    is_ai_ml: bool
    technically_sound: bool
    professional: bool
    recruiter_relevant: bool
    engineer_relevant: bool
    grammar_ok: bool
    quality_score: float = Field(
        ge=0.0,
        le=1.0,
    )
    feedback: str