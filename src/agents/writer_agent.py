from src.llm import get_llm
from src.services.history import load_history


def generate_post(
    topic: str,
    subtopic: str,
    angle: str,
    research: str,
    validation_feedback: str = "",
    duplicate_score: float = 0.0,
    retry_count: int = 0,
) -> str:

    llm = get_llm()

    history = load_history()

    previous_posts = "\n\n".join(
        item["content"]
        for item in history[-10:]
        if item.get("content")
    )

    retry_instructions = ""

    if retry_count > 0:
        retry_instructions = f"""
This is regeneration attempt #{retry_count}.

Previous validation feedback:
{validation_feedback}

Previous duplicate similarity score:
{duplicate_score}

You MUST substantially improve the previous attempt.

Do NOT simply rewrite the same post.

If the previous post was too similar to existing content:
- change the technical angle
- use a different example
- explain a different engineering trade-off
- change the structure

If the validator identified a technical or quality problem:
- fix that specific problem
"""

    prompt = f"""
You are an expert AI/ML technical content writer.

Create ONE original LinkedIn post.

AUDIENCE:
AI Engineers, ML Engineers, AI/ML Developers,
Technical Recruiters, Technical Hiring Managers

TOPIC:
{topic}

SUBTOPIC:
{subtopic}

ANGLE:
{angle}

TECHNICAL RESEARCH:
{research}

PREVIOUSLY PUBLISHED POSTS:
{previous_posts}

{retry_instructions}

REQUIREMENTS:

- AI/ML topics only
- genuine technical value
- natural professional language
- strong technical hook
- clear technical context
- practical engineering insight
- include an example when useful
- explain at least one trade-off or limitation
- end with a thoughtful question or takeaway
- 3-5 relevant hashtags
- no excessive emojis
- no generic motivation
- no invented statistics
- no unsupported claims
- no false personal experience
- no copying previous posts
- substantially different perspective when regenerating
- 150-250 words

PREFERRED STRUCTURE:

Hook
Problem / Context
Technical Explanation
Practical Engineering Insight
Trade-off / Limitation
Takeaway
Question
Hashtags

Return ONLY the LinkedIn post.
"""

    response = llm.invoke(prompt)

    return response.content.strip()