from langchain.chains import LLMChain, SequentialChain
from llm.groq_client import get_llm
from llm.prompt_templates import (
    get_history_prompt,
    get_news_prompt,
    get_quiz_prompt,
)


def build_history_chain():
    llm = get_llm()
    prompt = get_history_prompt()
    return LLMChain(llm=llm, prompt=prompt, output_key="history_points")


def build_news_chain():
    llm = get_llm()
    prompt = get_news_prompt()
    return LLMChain(llm=llm, prompt=prompt, output_key="news_points")


def build_quiz_chain():
    llm = get_llm()
    prompt = get_quiz_prompt()
    return LLMChain(llm=llm, prompt=prompt, output_key="quiz_text")


def build_full_quiz_pipeline():
    """
    Sequential pipeline:
    raw_history -> history_points
    raw_news -> news_points
    history_points + news_points -> quiz_text
    """
    history_chain = build_history_chain()
    news_chain = build_news_chain()
    quiz_chain = build_quiz_chain()

    # SequentialChain accepts named inputs and outputs
    full_chain = SequentialChain(
        chains=[history_chain, news_chain, quiz_chain],
        input_variables=["history_text", "news_text"],
        output_variables=["history_points", "news_points", "quiz_text"],
        verbose=False,
    )
    return full_chain


def generate_quiz(history_text: str, news_text: str) -> dict:
    """
    High-level helper. Takes raw history and news text, returns:
    {
        "history_points": "...",
        "news_points": "...",
        "quiz_text": "..."
    }
    """
    chain = build_full_quiz_pipeline()
    result = chain.invoke(
        {
            "history_text": history_text,
            "news_text": news_text,
        }
    )
    return result
