import os

# Model and LLM settings
MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0.4

# Quiz settings
NUM_PRELIMS_QUESTIONS = 8
NUM_MAINS_QUESTIONS = 4

# History / news limits
MAX_HISTORY_CHARS = 3000
MAX_NEWS_CHARS = 4000

# Cache settings
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "storage")

# App metadata
APP_TITLE = "Date-based Current Affairs and History Quiz"
APP_DESCRIPTION = (
    "Select a date to generate a style quiz based on historical events and news "
    "around that day. Useful for revision of static + current affairs."
)
