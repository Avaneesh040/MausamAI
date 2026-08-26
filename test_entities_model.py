from entities import extract_weather_entities


test_queries = [
    "Will it rain in Delhi tomorrow evening?",
    "What is the AQI in Mumbai today?",
    "How strong will the wind be in Bangalore tomorrow?",
    "What will the humidity be in Chennai today?",
    "What is the visibility in Kolkata tomorrow morning?",
    "What is the UV index in Delhi today?",
    "Will there be heavy rain in Mumbai tomorrow?",
    "Is there a cyclone warning near Chennai?",
    "Will there be flooding in Kerala tomorrow?",
    "How hot will it be in Delhi next week?"
]


print("=" * 60)
print("ENTITY MODEL TEST")
print("=" * 60)

for query in test_queries:

    entities = extract_weather_entities(query)

    print()
    print("Query:", query)
    print("Entities:", entities)