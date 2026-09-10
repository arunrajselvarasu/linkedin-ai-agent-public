import json

from src.llm import get_llm


def validate_post(
    post: str,
    research: str = "",
) -> dict:
    """
    Validate a LinkedIn post and return structured
    validation results for LangGraph state.
    """

    llm = get_llm(
        temperature=0.0,
        json_mode=True,
    )

    prompt = f"""
You are a strict technical content reviewer
for an AI/ML engineer's LinkedIn account.

Audience:
- Recruiters
- AI/ML engineers
- Software engineers

POST:
----------------
{post}
----------------

RESEARCH:
----------------
{research}
----------------

Evaluate:

1. is_ai_ml
   Must genuinely relate to AI, ML, GenAI, LLMs,
   RAG, agents, NLP, computer vision, MLOps,
   AI automation or related engineering topics.

2. technically_sound
   Technical statements must be accurate.

3. professional
   Professional LinkedIn tone.
   No clickbait or unrealistic hype.

4. recruiter_relevant
   Demonstrates useful engineering knowledge,
   skills, experience or problem solving.

5. engineer_relevant
   Provides meaningful technical value.

6. grammar_ok
   Clear and understandable.

7. unsupported_claims
   Identify unsupported numbers, percentages,
   benchmarks, performance improvements,
   rankings, adoption statistics or dates.

8. hallucination_risk
   Identify invented or questionable factual claims.

IMPORTANT:

If a quantitative claim is not supported by the
research, treat it as an unsupported claim.

Return ONLY JSON:

{{
    "is_ai_ml": true,
    "technically_sound": true,
    "professional": true,
    "recruiter_relevant": true,
    "engineer_relevant": true,
    "grammar_ok": true,
    "unsupported_claims": [],
    "hallucination_risk": false,
    "quality_score": 0.95,
    "feedback": "Short explanation"
}}

Quality score:
0.90-1.00 = excellent
0.85-0.89 = acceptable
0.70-0.84 = needs improvement
below 0.70 = poor

If unsupported claims or significant hallucination
risk exists, quality_score must be below 0.85.

Return JSON only.
"""

    response = llm.invoke(prompt)

    try:
        result = json.loads(
            response.content
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Validator returned invalid JSON."
        ) from exc

    required_fields = [
        "is_ai_ml",
        "technically_sound",
        "professional",
        "recruiter_relevant",
        "engineer_relevant",
        "grammar_ok",
        "quality_score",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Validator response missing field: {field}"
            )

    return {
        "is_ai_ml": bool(
            result["is_ai_ml"]
        ),
        "technically_sound": bool(
            result["technically_sound"]
        ),
        "professional": bool(
            result["professional"]
        ),
        "recruiter_relevant": bool(
            result["recruiter_relevant"]
        ),
        "engineer_relevant": bool(
            result["engineer_relevant"]
        ),
        "grammar_ok": bool(
            result["grammar_ok"]
        ),
        "quality_score": float(
            result["quality_score"]
        ),
        "validation_feedback": result.get(
            "feedback",
            "",
        ),
    }