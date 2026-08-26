import dateparser
from dateparser.search import search_dates
from datetime import datetime


def extract_datetime(text: str):

    now = datetime.now()

    result = search_dates(
        text,
        languages=["en", "hi"],
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": now
        }
    )

    if not result:
        return {
            "date": None,
            "time": None,
            "relative_expression": None
        }

    # Take the first detected date/time
    expression, detected_datetime = result[0]

    return {
        "date": detected_datetime.strftime("%Y-%m-%d"),
        "time": detected_datetime.strftime("%H:%M"),
        "relative_expression": expression
    }