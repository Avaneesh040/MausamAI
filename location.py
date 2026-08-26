KNOWN_LOCATIONS = {
    "bhubaneswar": "Bhubaneswar",
    "भुवनेश्वर": "Bhubaneswar",
    "ଭୁବନେଶ୍ୱର": "Bhubaneswar",

    "mumbai": "Mumbai",
    "मुंबई": "Mumbai",

    "delhi": "Delhi",
    "दिल्ली": "Delhi",

    "kolkata": "Kolkata",
    "कोलकाता": "Kolkata",

    "chennai": "Chennai",
    "चेन्नई": "Chennai",

    "bengaluru": "Bengaluru",
    "bangalore": "Bengaluru",
    "बेंगलुरु": "Bengaluru",

    "hyderabad": "Hyderabad",
    "हैदराबाद": "Hyderabad",

    "pune": "Pune",
    "पुणे": "Pune",

    "odisha": "Odisha",
    "ओडिशा": "Odisha",

    "india": "India",
    "भारत": "India"
}


def extract_location(text: str):

    text_lower = text.lower()

    for location, standard_name in KNOWN_LOCATIONS.items():

        if location in text_lower:
            return standard_name

    return None