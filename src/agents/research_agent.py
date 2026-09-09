import os

from dotenv import load_dotenv
from tavily import TavilyClient

from src.llm import get_llm


load_dotenv()


def get_tavily_client() -> TavilyClient:
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is not set. "
            "Please add it to your .env file."
        )

    return TavilyClient(api_key=api_key)


def research_topic(
    topic: str,
    subtopic: str,
    angle: str,
) -> str:
    """
    Search for reliable technical information.
    """

    client = get_tavily_client()

    query = f"""
AI engineering research:

Topic: {topic}
Subtopic: {subtopic}
Content angle: {angle}

Find reliable technical information from
official documentation, reputable engineering
sources, and technical articles.
"""

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    results = response.get("results", [])

    if not results:
        raise ValueError(
            "Research Agent did not find useful results."
        )

    research_parts = []

    for index, result in enumerate(results, start=1):
        research_parts.append(
            f"""
SOURCE {index}

Title:
{result.get("title", "")}

URL:
{result.get("url", "")}

Information:
{result.get("content", "")}
"""
        )

    return "\n".join(research_parts)


def synthesize_research(
    topic: str,
    subtopic: str,
    angle: str,
    raw_research: str,
) -> str:
    """
    Convert raw search results into concise,
    technically useful research for the writer.
    """

    llm = get_llm()

    prompt = f"""
You are a senior AI engineer performing research
for a professional LinkedIn post.

TOPIC:
{topic}

SUBTOPIC:
{subtopic}

ANGLE:
{angle}

RAW RESEARCH:
{raw_research}

Analyze the research and create a concise technical
brief for another AI writing agent.

Include:

1. Core technical concept
2. How it works
3. Important implementation details
4. Practical engineering use cases
5. Advantages
6. Limitations or trade-offs
7. Important terminology
8. One concrete example if supported by the sources

Rules:

- Use only information supported by the research.
- Do not invent statistics.
- Do not make unsupported claims.
- Do not write the LinkedIn post.
- Prefer technically accurate explanations.
- Clearly distinguish facts from interpretations.
"""

    response = llm.invoke(prompt)

    return response.content