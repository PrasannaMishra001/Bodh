from langchain_core.prompts import PromptTemplate
from config.settings import NUM_PRELIMS_QUESTIONS, NUM_MAINS_QUESTIONS


def get_history_prompt():
    return PromptTemplate(
        input_variables=["history_text"],
        template="""
You are a UPSC expert.
Summarize the following historical events into 5–8 crisp bullet points suitable for UPSC revision.

History:
{history_text}

Summary:
"""
    )


def get_news_prompt():
    return PromptTemplate(
        input_variables=["news_text"],
        template="""
You are a UPSC current affairs analyst.
Summarize the following news into 5–8 key bullet points.

News:
{news_text}

Summary:
"""
    )


def get_quiz_prompt():
    return PromptTemplate(
        input_variables=["history_summary", "news_summary"],
        template=f"""
Create a UPSC-style quiz with:

Prelims:
Exactly {NUM_PRELIMS_QUESTIONS} multiple-choice questions.
Each question must have 4 options and 1 correct answer.

Mains:
Exactly {NUM_MAINS_QUESTIONS} descriptive questions.

Use only this content:

History Summary:
{{history_summary}}

News Summary:
{{news_summary}}

Format exactly like:

PRELIMS:
Q1.
A)
B)
C)
D)
Answer:

MAINS:
Q1.
"""
    )
