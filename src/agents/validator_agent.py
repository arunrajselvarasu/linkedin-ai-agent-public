import json

from src.llm import get_llm
from src.models.schemas import ContentValidation


def validate_post(
    topic: str,
    subtopic: str,
    angle: str,
    post: str,
) -> ContentValidation:
    """
    Validate a generated LinkedIn post for quality,
    technical relevance, and audience suitability.
    """

    llm = get_llm(json_mode=True)

    prompt = f"""
You are a strict AI/ML content quality reviewer.

Evaluate the following LinkedIn post.

TOPIC:
{topic}

SUBTOPIC:
{subtopic}

ANGLE:
{angle}

POST:
{post}

Evaluate the post using these criteria:

1. is_ai_ml
   - Is the content genuinely related to AI or Machine Learning?

2. technically_sound
   - Are the technical statements accurate?
   - Are there misleading or unsupported claims?

3. professional
   - Is the writing suitable for LinkedIn professionals?

4. recruiter_relevant
   - Would the content demonstrate useful AI/ML knowledge
     to a technical recruiter or hiring manager?

5. engineer_relevant
   - Would an AI/ML engineer find the technical content useful?

6. grammar_ok
   - Is the grammar and readability acceptable?

7. quality_score
   - Overall quality from 0.0 to 1.0.

SCORING GUIDELINES:

0.90 - 1.00 = Excellent
0.80 - 0.89 = Good
0.70 - 0.79 = Acceptable but needs improvement
Below 0.70 = Poor

A post should only be accepted when:

- is_ai_ml = true
- technically_sound = true
- professional = true
- recruiter_relevant = true
- engineer_relevant = true
- grammar_ok = true
- quality_score >= 0.85

IMPORTANT:

Do not be overly generous.

Reject content that:
- is generic motivational content
- contains obvious technical inaccuracies
- contains unsupported statistics
- is unrelated to AI/ML
- is too shallow
- is poorly written
- contains excessive emojis
- sounds like spam
- is repetitive

Return ONLY valid JSON.

The JSON MUST contain exactly these fields:

{{
    "is_ai_ml": true,
    "technically_sound": true,
    "professional": true,
    "recruiter_relevant": true,
    "engineer_relevant": true,
    "grammar_ok": true,
    "quality_score": 0.90,
    "feedback": "Short explanation of the evaluation"
}}
"""

    response = llm.invoke(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict)
        )

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Validator returned invalid JSON:\n{content}"
        ) from exc

    return ContentValidation.model_validate(data)