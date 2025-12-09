import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from Bodh.config.settings import MODEL_NAME, TEMPERATURE

# Load environment variables from .env if present
load_dotenv()


def get_llm() -> ChatGroq:
    """
    Create and return a configured Groq ChatGroq LLM instance.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Set it in your environment or .env file."
        )

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=MODEL_NAME,
        temperature=TEMPERATURE,
    )
    return llm
