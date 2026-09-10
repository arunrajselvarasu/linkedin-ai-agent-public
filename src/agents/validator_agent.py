import json

from src.llm import get_llm


def validate_post(
    post: str,
    research: str = "",
) -> dict:
    """
    Validate a LinkedIn post against
    AI/ML, technical, professional and
    audience-quality requirements.

    Returns a plain dictionary so that
    LangGraph state can consume it directly.
    """

    llm = get_llm(
        temperature=0.0,
        json_mode=True,
    )

    prompt = f"""
You are a strict LinkedIn AI/ML content validator.

Your job is to determine whether the following
LinkedIn post is safe and suitable for publishing.

The target audience is:

1. Recruiters
2. AI/ML engineers
3. Software engineers
4. Technology professionals

The post must be:

- Clearly related to AI, ML, GenAI, LLMs,
  RAG, agents, automation, MLOps, AI engineering,
  data/ML engineering, or closely related technology.
- Technically reasonable.
- Professional.
- Useful to recruiters.
- Useful to engineers.
- Grammatically acceptable.
- Not misleading.
- Not spammy.
- Not excessively promotional.
- Not generic motivational content.
- Not unrelated to AI/ML.
- Not obviously copied from another post.

Research context:

{research}

Post:

{post}

Evaluate the post.

Return ONLY valid JSON.

Required JSON structure:

{{
    "is_ai_ml": true,
    "technically_sound": true,
    "professional": true,
    "recruiter_relevant": true,
    "engineer_relevant": true,
    "grammar_ok": true,
    "quality_score": 0.92,
    "feedback": "Short explanation of the validation result."
}}

Rules for quality_score:

- 0.90 - 1.00 = excellent
- 0.85 - 0.89 = acceptable
- 0.70 - 0.84 = needs improvement
- below 0.70 = poor

Be strict.

A post should only pass if all required boolean
criteria are true and quality_score >= 0.85.
"""

    response = llm.invoke(prompt)

    raw_content = response.content

    if isinstance(
        raw_content,
        list,
    ):
        raw_content = "".join(
            str(item)
            for item in raw_content
        )

    raw_content = str(
        raw_content
    ).strip()

    try:
        result = json.loads(
            raw_content
        )

    except json.JSONDecodeError:
        print(
            "❌ Validator returned invalid JSON"
        )

        return {
            "is_ai_ml": False,
            "technically_sound": False,
            "professional": False,
            "recruiter_relevant": False,
            "engineer_relevant": False,
            "grammar_ok": False,
            "quality_score": 0.0,
            "feedback":
                "Validator returned invalid JSON.",
        }

    # --------------------------------------------------------
    # Normalize / sanitize values
    # --------------------------------------------------------

    return {
        "is_ai_ml": bool(
            result.get(
                "is_ai_ml",
                False,
            )
        ),

        "technically_sound": bool(
            result.get(
                "technically_sound",
                False,
            )
        ),

        "professional": bool(
            result.get(
                "professional",
                False,
            )
        ),

        "recruiter_relevant": bool(
            result.get(
                "recruiter_relevant",
                False,
            )
        ),

        "engineer_relevant": bool(
            result.get(
                "engineer_relevant",
                False,
            )
        ),

        "grammar_ok": bool(
            result.get(
                "grammar_ok",
                False,
            )
        ),

        "quality_score": float(
            result.get(
                "quality_score",
                0.0,
            )
        ),

        "feedback": str(
            result.get(
                "feedback",
                "",
            )
        ),
    }