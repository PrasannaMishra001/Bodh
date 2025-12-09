from langchain.prompts import PromptTemplate
from Bodh.config.settings import (
    NUM_PRELIMS_QUESTIONS,
    NUM_MAINS_QUESTIONS,
)


def get_history_prompt() -> PromptTemplate:
    """
    Summarize 'On this day in history' text into relevant points.
    """
    template = (
        "You are helping a aspirant.\n\n"
        "Given the following raw historical events information for a specific date:\n\n"
        "{history_text}\n\n"
        "Summarize it into concise bullet points that are relevant for  focusing on:\n"
        "- Important personalities\n"
        "- Major events\n"
        "- Treaties, wars, constitutional events, national movements\n\n"
        "Return the result as bullet points only. No introduction, no conclusion."
    )
    return PromptTemplate(
        input_variables=["history_text"],
        template=template,
    )


def get_news_prompt() -> PromptTemplate:
    """
    Summarize current affairs news text into relevant themes.
    """
    template = (
        "You are helping a aspirant revise current affairs.\n\n"
        "Here is news content collected around a given date:\n\n"
        "{news_text}\n\n"
        "Summarize this into concise bullet points focusing on:\n"
        "- Government schemes and policies\n"
        "- International relations and diplomacy\n"
        "- Economy, environment, science and tech\n"
        "- Important reports, indices, committees\n\n"
        "Return bullet points only, no paragraphs, no introduction."
    )
    return PromptTemplate(
        input_variables=["news_text"],
        template=template,
    )


def get_quiz_prompt() -> PromptTemplate:
    """
    Generate style prelims and mains questions.
    """
    template = (
        "You are a question setter.\n\n"
        "You are given two sets of bullet points:\n\n"
        "Static and historical points:\n"
        "{history_points}\n\n"
        "Current affairs points:\n"
        "{news_points}\n\n"
        "Using this, generate:\n"
        f"1) Exactly {NUM_PRELIMS_QUESTIONS} Prelims-style MCQs.\n"
        "   - Each question should have 4 options (A, B, C, D).\n"
        "   - Mark the correct option clearly using 'Answer: X'.\n"
        "   - Do not add extra commentary.\n\n"
        f"2) Exactly {NUM_MAINS_QUESTIONS} Mains-style questions.\n"
        "   - These should be analytical and link static and current aspects.\n\n"
        "Return the output in the following structure strictly:\n\n"
        "PRELIMS:\n"
        "Q1. ...\n"
        "A) ...\n"
        "B) ...\n"
        "C) ...\n"
        "D) ...\n"
        "Answer: X\n"
        "Q2. ...\n"
        "...\n\n"
        "MAINS:\n"
        "Q1. ...\n"
        "Q2. ...\n"
        "...\n"
    )
    return PromptTemplate(
        input_variables=["history_points", "news_points"],
        template=template,
    )
