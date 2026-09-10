from src.llm import get_llm


def validate_post(post: str, research: str = "") -> dict:
    """
    Validate a LinkedIn post before publishing.

    The validator checks:
    - AI/ML relevance
    - Technical correctness
    - Professional tone
    - Recruiter relevance
    - AI engineer relevance
    - Grammar
    - Unsupported quantitative claims
    - Potential hallucinations
    """

    llm = get_llm(
        temperature=0.0,
        json_mode=True,
    )

    prompt = f"""
You are a strict technical content reviewer
for an AI/ML engineer's LinkedIn account.

The audience is:
1. Recruiters
2. AI/ML engineers
3. Software engineers interested in AI

Your job is to decide whether the post is safe
and technically credible enough to publish.

POST:
----------------
{post}
----------------

RESEARCH / SOURCE CONTEXT:
----------------
{research}
----------------

Evaluate the following:

1. is_ai_ml
   - The post must genuinely relate to AI, ML,
     GenAI, LLMs, RAG, agents, automation,
     NLP, computer vision, MLOps or related topics.

2. technically_sound
   - Technical statements must be accurate.
   - Reject misleading or fundamentally incorrect claims.

3. professional
   - Professional LinkedIn tone.
   - No clickbait, excessive hype or unrealistic claims.

4. recruiter_relevant
   - Demonstrates useful engineering knowledge,
     skills, experience or problem-solving ability.

5. engineer_relevant
   - Provides meaningful technical value to AI/ML
     or software engineers.

6. grammar_ok
   - Clear and grammatically understandable.

7. unsupported_claims
   - Identify claims that cannot reasonably be supported
     by the supplied research.
   - Pay special attention to numbers, percentages,
     benchmarks, performance improvements, rankings,
     adoption statistics and dates.

8. hallucination_risk
   - Identify statements that appear invented,
     exaggerated or presented as facts without evidence.

IMPORTANT RULE:

If the post contains a specific quantitative claim
such as:

"improves performance by 40%"
"reduces latency by 60%"
"used by 80% of companies"

and the supplied research does not support that claim,
consider it unsafe.

Do NOT reject normal technical explanations simply
because they do not have citations.

Return ONLY valid JSON with exactly this structure:

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

Rules for quality_score:

0.90 - 1.00:
Excellent and safe to publish.

0.85 - 0.89:
Good and acceptable.

0.70 - 0.84:
Needs improvement.

Below 0.70:
Unsafe or poor quality.

If unsupported quantitative claims or significant
hallucination risk exists, quality_score must be
below 0.85.

Return JSON only.
"""

    response = llm.invoke(prompt)

    return response.content