import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def get_llm(
    temperature: float = 0.7,
    json_mode: bool = False,
):
    """
    Create and return the Groq LLM.

    Args:
        temperature: Controls response creativity.
        json_mode: Enables Groq JSON response mode when required.
    """

    api_key = os.getenv("GROQ_API_KEY")

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. "
            "Please add it to your .env file."
        )

    kwargs = {
        "model": model,
        "api_key": api_key,
        "temperature": temperature,
    }

    if json_mode:
        kwargs["model_kwargs"] = {
            "response_format": {
                "type": "json_object"
            }
        }

    return ChatGroq(**kwargs)