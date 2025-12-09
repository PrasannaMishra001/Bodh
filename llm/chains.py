from llm.groq_client import get_llm
from llm.prompt_templates import (
    get_history_prompt,
    get_news_prompt,
    get_quiz_prompt
)


def generate_quiz(history_text: str, news_text: str) -> dict:
    llm = get_llm()

    history_prompt = get_history_prompt()
    news_prompt = get_news_prompt()
    quiz_prompt = get_quiz_prompt()

    history_chain = history_prompt | llm
    news_chain = news_prompt | llm
    quiz_chain = quiz_prompt | llm

    history_summary = history_chain.invoke(
        {"history_text": history_text}
    )

    news_summary = news_chain.invoke(
        {"news_text": news_text}
    )

    quiz_output = quiz_chain.invoke(
        {
            "history_summary": history_summary.content,
            "news_summary": news_summary.content
        }
    )

    return {
        "history_summary": history_summary.content,
        "news_summary": news_summary.content,
        "quiz_text": quiz_output.content
    }
