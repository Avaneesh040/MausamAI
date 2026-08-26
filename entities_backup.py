def extract_weather_entities(text: str):

    text_lower = text.lower()

    entities = {}

    # Rain
    if any(word in text_lower for word in [
        "rain",
        "rainfall",
        "बारिश",
        "वर्षा",
        "ବର୍ଷା"
    ]):
        entities["weather_condition"] = "rain"

    # Wind
    if any(word in text_lower for word in [
        "wind",
        "हवा",
        "पवन",
        "ବାୟୁ",
        "ପବନ"
    ]):
        entities["wind"] = True

    # Heavy rain
    if any(word in text_lower for word in [
        "heavy rain",
        "भारी बारिश",
        "तेज बारिश",
        "ଭୀଷଣ ବର୍ଷା"
    ]):
        entities["rain_intensity"] = "heavy"

    # Light rain
    elif any(word in text_lower for word in [
        "light rain",
        "हल्की बारिश",
        "हल्की वर्षा",
        "ହାଲୁକା ବର୍ଷା"
    ]):
        entities["rain_intensity"] = "light"

    # Strong wind
    if any(word in text_lower for word in [
        "strong wind",
        " तेज हवा",
        "तेज हवाएं",
        "ପ୍ରବଳ ପବନ"
    ]):
        entities["wind_intensity"] = "strong"

    # Cyclone
    if any(word in text_lower for word in [
        "cyclone",
        "चक्रवात",
        "ବାତ୍ୟା"
    ]):
        entities["disaster"] = "cyclone"

    # Flood
    if any(word in text_lower for word in [
        "flood",
        "flooding",
        "बाढ़",
        "ବନ୍ୟା"
    ]):
        entities["disaster"] = "flood"

    # Heatwave
    if any(word in text_lower for word in [
        "heatwave",
        "heat wave",
        "लू",
        "हीटवेव"
    ]):
        entities["disaster"] = "heatwave"

    return entities