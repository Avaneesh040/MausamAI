from intent import detect_intent


test_queries = [
    "Will it rain tomorrow?",
    "What is the temperature in Delhi?",
    "How humid is Mumbai today?",
    "How strong will the wind be?",
    "What is the AQI in Mumbai?",
    "What is the UV index in Delhi?",
    "What is the visibility in Kolkata?",
    "Is there a weather warning?",
    "What will the weather be like tomorrow?",
    "Will the weather be better tomorrow than today?",
    "When is sunrise in Delhi?",
]


print("=" * 55)
print("INTENT MODEL TEST")
print("=" * 55)

for query in test_queries:
    intent = detect_intent(query)

    print()
    print("Query:", query)
    print("Intent:", intent)