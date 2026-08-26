import json
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from seqeval.metrics import classification_report, precision_score, recall_score, f1_score


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

MODEL_DIR = BASE_DIR.parent.parent / "models" / "entity_model"
TEST_FILE = BASE_DIR / "test.json"


# ============================================================
# LOAD MODEL
# ============================================================

print("Loading trained entity model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)

model.eval()

print("Model loaded successfully.")


# ============================================================
# LOAD TEST DATA
# ============================================================

with open(TEST_FILE, "r", encoding="utf-8") as f:
    test_data = json.load(f)

print(f"Test examples: {len(test_data)}")


# ============================================================
# CONVERT CHARACTER SPANS TO TOKEN LABELS
# ============================================================

def get_true_labels(text, entities, offsets):

    labels = []

    for start, end in offsets:

        if start == end:
            labels.append("O")
            continue

        label = "O"

        for entity in entities:

            entity_start = entity["start"]
            entity_end = entity["end"]
            entity_label = entity["label"]

            # No overlap
            if end <= entity_start:
                continue

            if start >= entity_end:
                continue

            # Token overlaps entity
            if start >= entity_start:
                label = f"B-{entity_label}"

            else:
                label = f"I-{entity_label}"

            break

        labels.append(label)

    return labels


# ============================================================
# PREDICT ONE EXAMPLE
# ============================================================

def predict(text):

    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
        return_offsets_mapping=True,
    )

    offsets = encoded.pop("offset_mapping")[0].tolist()

    with torch.no_grad():
        outputs = model(**encoded)

    predictions = torch.argmax(
        outputs.logits,
        dim=-1,
    )[0].tolist()

    predicted_labels = []

    for prediction, (start, end) in zip(
        predictions,
        offsets,
    ):

        if start == end:
            predicted_labels.append("O")
        else:
            predicted_labels.append(
                model.config.id2label[prediction]
            )

    return predicted_labels, offsets


# ============================================================
# EVALUATE
# ============================================================

true_sequences = []
pred_sequences = []

print()
print("=" * 60)
print("EVALUATING ENTITY MODEL")
print("=" * 60)

for i, example in enumerate(test_data):

    text = example["text"]
    entities = example["entities"]

    encoded = tokenizer(
        text,
        truncation=True,
        max_length=128,
        return_offsets_mapping=True,
    )

    offsets = encoded["offset_mapping"]

    true_labels = get_true_labels(
        text,
        entities,
        offsets,
    )

    predicted_labels, _ = predict(text)

    # Make sure lengths match
    min_length = min(
        len(true_labels),
        len(predicted_labels),
    )

    true_labels = true_labels[:min_length]
    predicted_labels = predicted_labels[:min_length]

    true_sequences.append(true_labels)
    pred_sequences.append(predicted_labels)


# ============================================================
# METRICS
# ============================================================

precision = precision_score(
    true_sequences,
    pred_sequences,
)

recall = recall_score(
    true_sequences,
    pred_sequences,
)

f1 = f1_score(
    true_sequences,
    pred_sequences,
)


print()
print("=" * 60)
print("OVERALL RESULTS")
print("=" * 60)

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")


# ============================================================
# PER-ENTITY REPORT
# ============================================================

print()
print("=" * 60)
print("PER-ENTITY RESULTS")
print("=" * 60)

print(
    classification_report(
        true_sequences,
        pred_sequences,
        digits=4,
    )
)

print("=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)