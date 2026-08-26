import json
from pathlib import Path

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification,
)

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

TRAIN_FILE = BASE_DIR / "train.json"
VALIDATION_FILE = BASE_DIR / "validation.json"
MODEL_DIR = BASE_DIR.parent.parent / "models" / "entity_model"

# AI4Bharat IndicBERTv2
MODEL_NAME = "ai4bharat/IndicBERTv2-MLM-Sam-TLM"


# ============================================================
# ENTITY LABELS
# ============================================================

ENTITY_LABELS = [
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

# BIO labels
LABEL_LIST = ["O"]

for entity in ENTITY_LABELS:
    LABEL_LIST.append(f"B-{entity}")
    LABEL_LIST.append(f"I-{entity}")

LABEL2ID = {
    label: i
    for i, label in enumerate(LABEL_LIST)
}

ID2LABEL = {
    i: label
    for label, i in LABEL2ID.items()
}


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


print("Loading datasets...")

train_data = load_json(TRAIN_FILE)
validation_data = load_json(VALIDATION_FILE)

train_dataset = Dataset.from_list(train_data)
validation_dataset = Dataset.from_list(validation_data)

print(f"Training examples:   {len(train_dataset)}")
print(f"Validation examples: {len(validation_dataset)}")


# ============================================================
# TOKENIZER
# ============================================================

print()
print("Loading IndicBERTv2 tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=True,
)

print("Tokenizer loaded.")


# ============================================================
# CONVERT CHARACTER SPANS → BIO TOKEN LABELS
# ============================================================

def tokenize_and_align_labels(example):

    text = example["text"]
    entities = example["entities"]

    tokenized = tokenizer(
        text,
        truncation=True,
        max_length=128,
        return_offsets_mapping=True,
    )

    offsets = tokenized["offset_mapping"]

    labels = []

    for token_start, token_end in offsets:

        # Special token
        if token_start == token_end:
            labels.append(-100)
            continue

        token_label = "O"

        for entity in entities:

            entity_start = entity["start"]
            entity_end = entity["end"]
            entity_type = entity["label"]

            # No overlap
            if token_end <= entity_start:
                continue

            if token_start >= entity_end:
                continue

            # Token overlaps entity
            if token_start >= entity_start:
                token_label = f"B-{entity_type}"

                # Determine whether this should be I
                previous_tokens = [
                    x for x in offsets
                    if x[0] >= entity_start
                    and x[1] <= token_start
                    and x[0] != x[1]
                ]

                if previous_tokens:
                    token_label = f"I-{entity_type}"

            else:
                token_label = f"I-{entity_type}"

            break

        labels.append(LABEL2ID[token_label])

    tokenized["labels"] = labels

    # Trainer doesn't need this after labels are created
    tokenized.pop("offset_mapping")

    return tokenized


print()
print("Converting character spans to BIO labels...")

tokenized_train = train_dataset.map(
    tokenize_and_align_labels,
    remove_columns=train_dataset.column_names,
)

tokenized_validation = validation_dataset.map(
    tokenize_and_align_labels,
    remove_columns=validation_dataset.column_names,
)

print("BIO conversion complete.")


# ============================================================
# MODEL
# ============================================================

print()
print("Loading IndicBERTv2 model...")

model = AutoModelForTokenClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABEL_LIST),
    id2label=ID2LABEL,
    label2id=LABEL2ID,
)

print("Model loaded.")


# ============================================================
# DATA COLLATOR
# ============================================================

data_collator = DataCollatorForTokenClassification(
    tokenizer=tokenizer,
)


# ============================================================
# TRAINING CONFIG
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

training_args = TrainingArguments(
    output_dir=str(MODEL_DIR),

    num_train_epochs=3,

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    learning_rate=2e-5,

    weight_decay=0.01,

    logging_steps=50,

    eval_strategy="epoch",
    save_strategy="epoch",

    load_best_model_at_end=True,

    save_total_limit=2,

    report_to="none",

    use_cpu=True,
)


# ============================================================
# TRAINER
# ============================================================

trainer = Trainer(
    model=model,

    args=training_args,

    train_dataset=tokenized_train,

    eval_dataset=tokenized_validation,

    processing_class=tokenizer,

    data_collator=data_collator,
)


# ============================================================
# TRAIN
# ============================================================

print()
print("====================================")
print("STARTING ENTITY MODEL TRAINING")
print("====================================")
print()

trainer.train()


# ============================================================
# SAVE
# ============================================================

print()
print("Saving final model...")

trainer.save_model(str(MODEL_DIR))
tokenizer.save_pretrained(str(MODEL_DIR))

print()
print("====================================")
print("ENTITY MODEL TRAINING COMPLETE")
print("====================================")
print(f"Model saved to: {MODEL_DIR}")