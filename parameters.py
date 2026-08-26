def extract_parameters(text: str):

    text_lower = text.lower()

    parameters = {
        "temperature": False,
        "rain": False,
        "humidity": False,
        "wind": False,
        "pressure": False,
        "visibility": False,
        "cloud_cover": False,
        "air_quality": False
    }

    if any(x in text_lower for x in [
        "temperature", "तापमान", "ताप"
    ]):
        parameters["temperature"] = True

    if any(x in text_lower for x in [
        "rain", "rainfall", "बारिश", "वर्षा", "ବର୍ଷା"
    ]):
        parameters["rain"] = True

    if any(x in text_lower for x in [
        "humidity", "नमी", "आर्द्रता"
    ]):
        parameters["humidity"] = True

    if any(x in text_lower for x in [
        "wind", "हवा", "पवन", "पବନ"
    ]):
        parameters["wind"] = True

    if any(x in text_lower for x in [
        "pressure", "दबाव", "ଚାପ"
    ]):
        parameters["pressure"] = True

    if any(x in text_lower for x in [
        "visibility", "दृश्यता", "ଦୃଶ୍ୟତା"
    ]):
        parameters["visibility"] = True

    if any(x in text_lower for x in [
        "cloud", "cloudy", "बादल", "ମେଘ"
    ]):
        parameters["cloud_cover"] = True

    if any(x in text_lower for x in [
        "aqi", "air quality", "वायु गुणवत्ता"
    ]):
        parameters["air_quality"] = True

    return parameters