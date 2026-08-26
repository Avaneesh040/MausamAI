import json
import random
from pathlib import Path

random.seed(42)

OUTPUT_DIR = Path(__file__).parent

LABELS = [
    "RAIN",
    "RAIN_INTENSITY",
    "WIND",
    "WIND_INTENSITY",
    "CYCLONE",
    "FLOOD",
    "HEATWAVE",
    "HUMIDITY",
    "VISIBILITY",
    "UV_INDEX",
    "AQI",
    "LOCATION",
    "DATE",
    "TIME",
]


def make_example(text, entities):
    """
    entities:
        [
            ("Delhi", "LOCATION"),
            ("tomorrow", "DATE")
        ]

    Automatically calculates character positions.
    """

    annotations = []

    for entity_text, label in entities:
        start = text.find(entity_text)

        if start == -1:
            raise ValueError(
                f"Could not find '{entity_text}' in:\n{text}"
            )

        end = start + len(entity_text)

        annotations.append({
            "start": start,
            "end": end,
            "label": label,
        })

    return {
        "text": text,
        "entities": annotations,
    }


examples = []


# ============================================================
# WEATHER LOCATIONS
# ============================================================

locations_en = [
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Bhubaneswar",
    "Jaipur",
    "Lucknow",
    "Patna",
    "Guwahati",
    "Kochi",
    "Ahmedabad",
    "Srinagar",
    "Chandigarh",
    "Bhopal",
    "Ranchi",
    "Indore",
    "Visakhapatnam",
]

locations_hi = [
    "दिल्ली",
    "मुंबई",
    "कोलकाता",
    "चेन्नई",
    "बेंगलुरु",
    "हैदराबाद",
    "पुणे",
    "भुवनेश्वर",
    "जयपुर",
    "लखनऊ",
    "पटना",
    "गुवाहाटी",
    "कोच्चि",
    "अहमदाबाद",
]

locations_roman = [
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Chennai",
    "Bengaluru",
    "Hyderabad",
    "Pune",
    "Bhubaneswar",
    "Jaipur",
    "Lucknow",
    "Patna",
    "Guwahati",
]

locations_od = [
    "ଭୁବନେଶ୍ୱର",
    "କଟକ",
    "ପୁରୀ",
    "ରାଉରକେଲା",
    "ସମ୍ବଲପୁର",
    "ବାଲେଶ୍ୱର",
]


dates_en = [
    "today",
    "tomorrow",
    "yesterday",
    "this afternoon",
    "next week",
]

times_en = [
    "tonight",
    "this evening",
    "this morning",
    "6 AM",
    "8 AM",
    "10 AM",
    "12 PM",
    "3 PM",
    "6 PM",
    "9 PM",
    "midnight",
]

dates_hi = [
    "आज",
    "कल",
    "कल सुबह",
    "कल शाम",
    "आज शाम",
    "आज सुबह",
]

dates_roman = [
    "aaj",
    "kal",
    "kal subah",
    "kal shaam",
    "aaj shaam",
    "aaj subah",
]

times_en = [
    "6 AM",
    "8 AM",
    "10 AM",
    "12 PM",
    "3 PM",
    "6 PM",
    "9 PM",
    "midnight",
]

times_hi = [
    "सुबह",
    "दोपहर",
    "शाम",
    "रात",
]

times_roman = [
    "subah",
    "dopahar",
    "shaam",
    "raat",
]


# ============================================================
# TEMPLATE HELPERS
# ============================================================

def add_location_date_examples():
    for location in locations_en:
        for date in dates_en:
            templates = [
                (
                    f"What is the weather in {location} {date}?",
                    [(location, "LOCATION"), (date, "DATE")]
                ),
                (
                    f"How will the weather be in {location} {date}?",
                    [(location, "LOCATION"), (date, "DATE")]
                ),
                (
                    f"What will the weather be like in {location} {date}?",
                    [(location, "LOCATION"), (date, "DATE")]
                ),
            ]

            for text, entities in templates:
                examples.append(make_example(text, entities))


def add_rain_examples():
    for location in locations_en:
        for date in dates_en:
            examples.extend([
                make_example(
                    f"Will it rain in {location} {date}?",
                    [
                        ("rain", "RAIN"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"Is rain expected in {location} {date}?",
                    [
                        ("rain", "RAIN"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"Will there be heavy rain in {location} {date}?",
                    [
                        ("heavy rain", "RAIN_INTENSITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"Will there be light rain in {location} {date}?",
                    [
                        ("light rain", "RAIN_INTENSITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
            ])

    hindi_templates = [
        ("क्या {location} में {date} बारिश होगी?", "बारिश", "RAIN"),
        ("क्या {location} में {date} भारी बारिश होगी?", "भारी बारिश", "RAIN_INTENSITY"),
        ("क्या {location} में {date} हल्की बारिश होगी?", "हल्की बारिश", "RAIN_INTENSITY"),
    ]

    for location in locations_hi:
        for date in dates_hi:
            for template, rain_word, label in hindi_templates:
                text = template.format(location=location, date=date)

                examples.append(
                    make_example(
                        text,
                        [
                            (location, "LOCATION"),
                            (date, "DATE"),
                            (rain_word, label),
                        ],
                    )
                )


def add_wind_examples():
    for location in locations_en:
        for date in dates_en:
            examples.extend([
                make_example(
                    f"How strong will the wind be in {location} {date}?",
                    [
                        ("wind", "WIND"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"What will the wind speed be in {location} {date}?",
                    [
                        ("wind", "WIND"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"Will there be strong wind in {location} {date}?",
                    [
                        ("strong wind", "WIND_INTENSITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
            ])


def add_humidity_examples():
    for location in locations_en:
        for date in dates_en:
            examples.extend([
                make_example(
                    f"What will the humidity be in {location} {date}?",
                    [
                        ("humidity", "HUMIDITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"How humid will {location} be {date}?",
                    [
                        ("humid", "HUMIDITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
            ])

    for location in locations_hi:
        examples.append(
            make_example(
                f"{location} में नमी कितनी होगी?",
                [
                    (location, "LOCATION"),
                    ("नमी", "HUMIDITY"),
                ],
            )
        )


def add_visibility_examples():
    for location in locations_en:
        for date in dates_en:
            examples.extend([
                make_example(
                    f"What will the visibility be in {location} {date}?",
                    [
                        ("visibility", "VISIBILITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"Will visibility be low in {location} {date}?",
                    [
                        ("visibility", "VISIBILITY"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
            ])


def add_uv_examples():
    for location in locations_en:
        for date in dates_en:
            examples.extend([
                make_example(
                    f"What is the UV index in {location} {date}?",
                    [
                        ("UV index", "UV_INDEX"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"How high will the UV index be in {location} {date}?",
                    [
                        ("UV index", "UV_INDEX"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
            ])

    for date in dates_hi:
        examples.append(
            make_example(
                f"{date} UV index कितना है?",
                [
                    (date, "DATE"),
                    ("UV index", "UV_INDEX"),
                ],
            )
        )


def add_aqi_examples():
    for location in locations_en:
        for date in dates_en:
            examples.extend([
                make_example(
                    f"What is the AQI in {location} {date}?",
                    [
                        ("AQI", "AQI"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
                make_example(
                    f"How bad is the air quality in {location} {date}?",
                    [
                        ("air quality", "AQI"),
                        (location, "LOCATION"),
                        (date, "DATE"),
                    ],
                ),
            ])

    for location in locations_hi:
        examples.append(
            make_example(
                f"{location} का AQI कितना है?",
                [
                    (location, "LOCATION"),
                    ("AQI", "AQI"),
                ],
            )
        )


def add_disaster_examples():
    for location in locations_en:
        examples.extend([
            make_example(
                f"Is there a cyclone near {location}?",
                [
                    ("cyclone", "CYCLONE"),
                    (location, "LOCATION"),
                ],
            ),
            make_example(
                f"Is there a flood warning for {location}?",
                [
                    ("flood", "FLOOD"),
                    (location, "LOCATION"),
                ],
            ),
            make_example(
                f"Is there a heatwave in {location}?",
                [
                    ("heatwave", "HEATWAVE"),
                    (location, "LOCATION"),
                ],
            ),
        ])


def add_time_examples():
    for location in locations_en:
        for time in times_en:
            examples.extend([
                make_example(
                    f"What is the weather in {location} at {time}?",
                    [
                        (location, "LOCATION"),
                        (time, "TIME"),
                    ],
                ),
                make_example(
                    f"Will it rain in {location} at {time}?",
                    [
                        ("rain", "RAIN"),
                        (location, "LOCATION"),
                        (time, "TIME"),
                    ],
                ),
            ])


def add_romanized_examples():
    for location in locations_roman:
        for date in dates_roman:
            examples.extend([
                make_example(
                    f"{location} mein {date} baarish hogi?",
                    [
                        (location, "LOCATION"),
                        (date, "DATE"),
                        ("baarish", "RAIN"),
                    ],
                ),
                make_example(
                    f"{location} mein {date} humidity kitni hogi?",
                    [
                        (location, "LOCATION"),
                        (date, "DATE"),
                        ("humidity", "HUMIDITY"),
                    ],
                ),
                make_example(
                    f"{location} mein {date} hawa tez hogi?",
                    [
                        (location, "LOCATION"),
                        (date, "DATE"),
                        ("hawa", "WIND"),
                    ],
                ),
                make_example(
                    f"{location} ka AQI {date} kitna hoga?",
                    [
                        (location, "LOCATION"),
                        ("AQI", "AQI"),
                        (date, "DATE"),
                    ],
                ),
            ])


# ============================================================
# GENERATE
# ============================================================

add_location_date_examples()
add_rain_examples()
add_wind_examples()
add_humidity_examples()
add_visibility_examples()
add_uv_examples()
add_aqi_examples()
add_disaster_examples()
add_time_examples()
add_romanized_examples()


# ============================================================
# REMOVE DUPLICATES
# ============================================================

unique = {}
for example in examples:
    unique[example["text"]] = example

examples = list(unique.values())

random.shuffle(examples)


# ============================================================
# SPLIT DATA
# ============================================================

total = len(examples)

train_end = int(total * 0.70)
validation_end = int(total * 0.85)

train_data = examples[:train_end]
validation_data = examples[train_end:validation_end]
test_data = examples[validation_end:]


# ============================================================
# SAVE
# ============================================================

def save_json(filename, data):
    path = OUTPUT_DIR / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Saved {len(data)} examples -> {path}")


save_json("train.json", train_data)
save_json("validation.json", validation_data)
save_json("test.json", test_data)


# ============================================================
# SUMMARY
# ============================================================

print()
print("====================================")
print("ENTITY DATASET CREATED")
print("====================================")
print(f"Total examples:      {total}")
print(f"Training examples:   {len(train_data)}")
print(f"Validation examples: {len(validation_data)}")
print(f"Test examples:       {len(test_data)}")

print()
print("Labels:")

for label in LABELS:
    print(label)