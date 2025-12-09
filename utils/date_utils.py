from datetime import date, datetime


def to_date(dt) -> date:
    """
    Convert a Streamlit date_input value or string into a datetime.date object.
    """
    if isinstance(dt, date):
        return dt
    if isinstance(dt, datetime):
        return dt.date()
    if isinstance(dt, str):
        return datetime.fromisoformat(dt).date()
    raise ValueError(f"Cannot convert {type(dt)} to date.")
