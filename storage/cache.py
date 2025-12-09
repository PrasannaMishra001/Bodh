import json
import os
from datetime import date
from config.settings import CACHE_DIR


def _get_cache_file_path(target_date: date) -> str:
    safe_name = target_date.isoformat()
    # Store in storage directory
    base_dir = os.path.join(CACHE_DIR)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, f"quiz_{safe_name}.json")


def load_cached_quiz(target_date: date):
    path = _get_cache_file_path(target_date)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_quiz_to_cache(target_date: date, quiz_data: dict):
    path = _get_cache_file_path(target_date)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}")
