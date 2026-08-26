import sys
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification


# ============================================================
# PATH
# ============================================================

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR.parent.parent / "models" / "entity_model"


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading entity model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)

model.eval()

print("Model loaded successfully.")


# ============================================================
# ENTITY EXTRACTION
# ============================================================

def extract_entities(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        return_offsets_mapping=True,
    )

    offset_mapping = inputs.pop("offset_mapping")[0]

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=-1)[0]

    entities = []
    current_entity = None

    for prediction_id, (start, end) in zip(
        predictions,
        offset_mapping,
    ):

        start = int(start)
        end = int(end)

        # Skip special tokens
        if start == end:
            continue

        label = model.config.id2label[prediction_id.item()]

        # Outside any entity
        if label == "O":

            if current_entity:
                entities.append(current_entity)
                current_entity = None

            continue

        prefix, entity_type = label.split("-", 1)

        # Beginning of an entity
        if prefix == "B":

            if current_entity:
                entities.append(current_entity)

            current_entity = {
                "label": entity_type,
                "text": text[start:end],
                "start": start,
                "end": end,
            }

        # Continuation of an entity
        elif prefix == "I":

            if (
                current_entity
                and current_entity["label"] == entity_type
            ):

                current_entity["end"] = end

                # Rebuild from original text.
                # This prevents duplicated subword text.
                current_entity["text"] = text[
                    current_entity["start"]:current_entity["end"]
                ]

            else:

                if current_entity:
                    entities.append(current_entity)

                current_entity = {
                    "label": entity_type,
                    "text": text[start:end],
                    "start": start,
                    "end": end,
                }

    if current_entity:
        entities.append(current_entity)

    return entities


# ============================================================
# TEST QUERIES
# ============================================================

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

    "How hot will it be in Delhi next week?",

]


# ============================================================
# RUN TESTS
# ============================================================

print()
print("=" * 60)
print("ENTITY MODEL TEST")
print("=" * 60)

for query in test_queries:

    entities = extract_entities(query)

    print()
    print("Query:", query)

    if not entities:
        print("Entities: NONE")
        continue

    for entity in entities:
        print(
            f"  {entity['label']:16} -> "
            f"{entity['text']}"
        )