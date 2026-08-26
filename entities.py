import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification


MODEL_PATH = "models/entity_model"

# Load trained entity model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForTokenClassification.from_pretrained(MODEL_PATH)

model.eval()


def extract_weather_entities(text: str):
    """
    Extract weather entities using the trained IndicBERT entity model.

    Returns a dictionary compatible with the existing WeatherGPT API.
    """

    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        return_offsets_mapping=True
    )

    # Offset mapping is only needed for converting token predictions
    # back to the original text.
    offsets = encoded.pop("offset_mapping")[0].tolist()

    with torch.no_grad():
        outputs = model(**encoded)

    predictions = torch.argmax(
        outputs.logits,
        dim=-1
    )[0].tolist()

    tokens = []

    for prediction, (start, end) in zip(predictions, offsets):

        # Special tokens
        if start == end:
            continue

        label = model.config.id2label[prediction]

        if label == "O":
            continue

        tokens.append({
            "label": label,
            "start": start,
            "end": end
        })

    # ---------------------------------------------------------
    # Combine BIO tokens into complete entities
    # ---------------------------------------------------------

    extracted = []

    current_label = None
    current_start = None
    current_end = None

    for item in tokens:

        label = item["label"]
        start = item["start"]
        end = item["end"]

        if label.startswith("B-"):

            # Save previous entity
            if current_label is not None:
                extracted.append({
                    "label": current_label,
                    "start": current_start,
                    "end": current_end
                })

            current_label = label[2:]
            current_start = start
            current_end = end

        elif label.startswith("I-"):

            entity_label = label[2:]

            if current_label == entity_label:
                current_end = end

            else:
                # Broken BIO sequence — start a new entity
                if current_label is not None:
                    extracted.append({
                        "label": current_label,
                        "start": current_start,
                        "end": current_end
                    })

                current_label = entity_label
                current_start = start
                current_end = end

    # Save final entity
    if current_label is not None:
        extracted.append({
            "label": current_label,
            "start": current_start,
            "end": current_end
        })

    # ---------------------------------------------------------
    # Convert to application-friendly dictionary
    # ---------------------------------------------------------

    entities = {}

    for entity in extracted:

        label = entity["label"]

        value = text[
            entity["start"]:entity["end"]
        ].strip()

        if not value:
            continue

        # Multiple entities of the same type
        # are stored as a list.
        if label in entities:

            if isinstance(entities[label], list):
                entities[label].append(value)
            else:
                entities[label] = [
                    entities[label],
                    value
                ]

        else:
            entities[label] = value

    return entities