import streamlit as st
from datetime import date

from config.settings import APP_TITLE, APP_DESCRIPTION
from data_sources import fetch_history_for_date, fetch_news_for_date
from llm import generate_quiz
from quizzes import format_quiz_markdown
from storage import load_cached_quiz, save_quiz_to_cache
from utils import to_date, is_non_empty


def main():
    st.set_page_config(
        page_title="Daily Quiz Generator",
        layout="wide",
    )

    # Optional logo
    try:
        st.sidebar.image("assets/app_logo.png", width=80)
    except Exception:
        pass

    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)

    # Date selector
    st.subheader("Select a date")
    selected_date = st.date_input(
        "Choose a date for which you want history and current affairs based quiz",
        value=date.today(),
    )

    if st.button("Generate Quiz"):
        target_date = to_date(selected_date)

        # Try cache first
        cached = load_cached_quiz(target_date)
        if cached:
            st.info("Loaded quiz from cache.")
            history_points = cached.get("history_points", "")
            news_points = cached.get("news_points", "")
            quiz_text = cached.get("quiz_text", "")
        else:
            with st.spinner("Fetching history data..."):
                history_raw = fetch_history_for_date(target_date)

            with st.spinner("Fetching news data..."):
                news_raw = fetch_news_for_date(target_date)

            if not is_non_empty(history_raw) and not is_non_empty(news_raw):
                st.error("Could not fetch enough history or news data for this date.")
                return

            with st.spinner("Generating style quiz with LLM..."):
                result = generate_quiz(history_text=history_raw, news_text=news_raw)

            history_points = result.get("history_points", "")
            news_points = result.get("news_points", "")
            quiz_text = result.get("quiz_text", "")

            save_quiz_to_cache(
                target_date,
                {
                    "history_points": history_points,
                    "news_points": news_points,
                    "quiz_text": quiz_text,
                },
            )

        # Display sections
        st.success(f"Quiz generated for {target_date.isoformat()}")

        with st.expander("Relevant history points", expanded=False):
            st.markdown(history_points or "No history points available.")

        with st.expander("Relevant current affairs points", expanded=False):
            st.markdown(news_points or "No news points available.")

        st.subheader("Prelims and Mains Quiz")
        st.markdown(format_quiz_markdown(quiz_text), unsafe_allow_html=False)


if __name__ == "__main__":
    main()
