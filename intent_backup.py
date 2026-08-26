def detect_intent(text: str):

    text = text.lower()

    if any(word in text for word in [
        "rain", "rainfall", "बारिश", "वर्षा", "ବର୍ଷା"
    ]):
        return "rain_forecast"

    if any(word in text for word in [
        "temperature", "temp", "तापमान", "ତାପମାତ୍ରା"
    ]):
        return "temperature"

    if any(word in text for word in [
        "humidity", "नमी", "ଆର୍ଦ୍ରତା"
    ]):
        return "humidity"

    if any(word in text for word in [
        "wind", "हवा", "ବାୟୁ", "ପବନ"
    ]):
        return "wind"

    if any(word in text for word in [
        "warning", "alert", "चेतावनी", "ସତର୍କ"
    ]):
        return "weather_warning"

    if any(word in text for word in [
        "weather", "मौसम", "ପାଗ"
    ]):
        return "weather_forecast"

    return "general_weather"