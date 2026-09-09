import json

from src.llm import get_llm
from src.models.schemas import TopicSelection


TOPICS = [
    "Generative AI",
    "Large Language Models",
    "AI Agents",
    "Agentic RAG",
    "LangChain",
    "LangGraph",
    "Model Context Protocol",
    "RAG",
    "Vector Databases",
    "Embeddings",
    "Prompt Engineering",
    "LLM Evaluation",
    "AI Security",
    "MLOps",
    "LLMOps",
    "Multi-Agent Systems",
    "NLP",
    "Machine Learning",
    "Deep Learning",
    "Computer Vision",
]


def select_topic() -> TopicSelection:
    """
    Select an AI/ML topic and a specific content angle
    for the LinkedIn content agent.
    """

    llm = get_llm(json_mode=True)

    prompt = f"""
You are an AI/ML content strategist.

Your job is to select ONE topic for an automated
LinkedIn post.

TARGET AUDIENCE:
- AI Engineers
- ML Engineers
- AI/ML Developers
- Technical Recruiters
- Technical Hiring Managers

ALLOWED TOPICS:

{", ".join(TOPICS)}

REQUIREMENTS:

1. The topic MUST be related to AI or Machine Learning.
2. Select one specific technical subtopic.
3. Select a practical and interesting angle.
4. Avoid generic motivational content.
5. Focus on engineering knowledge.
6. The post should provide real technical value.
7. Prefer architectures, implementation patterns,
   tools, trade-offs, practical use cases,
   and engineering best practices.
8. Do not invent statistics.
9. Avoid obvious beginner-level content.
10. Make the topic suitable for LinkedIn.
11. The angle should give the writer something
    meaningful to explain.
12. Do not generate the LinkedIn post itself.

Return ONLY valid JSON.

The JSON MUST have exactly these fields:

{{
    "topic": "AI/ML topic",
    "subtopic": "specific technical subtopic",
    "angle": "specific content angle"
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
            f"Groq returned invalid JSON:\n{content}"
        ) from exc

    return TopicSelection.model_validate(data)