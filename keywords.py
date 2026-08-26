WEATHER_KEYWORDS = [
    "rain",
    "rainfall",
    "temperature",
    "humidity",
    "wind",
    "storm",
    "cyclone",
    "flood",
    "heatwave",
    "coldwave",
    "warning",
    "alert",
    "weather",
    "forecast",
    "बारिश",
    "वर्षा",
    "तापमान",
    "नमी",
    "हवा",
    "तूफान",
    "बाढ़",
    "मौसम",
    "चेतावनी",
    "ବର୍ଷା",
    "ତାପମାତ୍ରା",
    "ପବନ",
    "ପାଗ"
]


def extract_keywords(text: str):

    text_lower = text.lower()

    keywords = []

    for word in WEATHER_KEYWORDS:

        if word.lower() in text_lower:
            keywords.append(word)

    return list(dict.fromkeys(keywords))