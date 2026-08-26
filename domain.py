def identify_domain_task(text: str):

    text_lower = text.lower()

    # Disaster
    if any(word in text_lower for word in [
        "cyclone",
        "flood",
        "heatwave",
        "storm",
        "चक्रवात",
        "बाढ़",
        "तूफान",
        "बवंडर",
        "ବାତ୍ୟା",
        "ବନ୍ୟା"
    ]):
        return {
            "domain": "disaster",
            "task": "warning"
        }

    # Weather
    if any(word in text_lower for word in [
        "weather",
        "rain",
        "temperature",
        "humidity",
        "wind",
        "बारिश",
        "मौसम",
        "तापमान",
        "हवा",
        "ବର୍ଷା",
        "ପାଗ"
    ]):
        return {
            "domain": "weather",
            "task": "forecast"
        }

    # Climate
    if any(word in text_lower for word in [
        "climate",
        "जलवायु",
        "जलवायु परिवर्तन",
        "ଜଳବାୟୁ"
    ]):
        return {
            "domain": "climate",
            "task": "analysis"
        }

    return {
        "domain": "unknown",
        "task": "unknown"
    }