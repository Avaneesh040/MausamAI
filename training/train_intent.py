import os
import json
import pandas as pd

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

# =========================
# Paths
# =========================

BASE_DIR = r"C:\Users\KIIT\Weather"
DATA_DIR = os.path.join(BASE_DIR, "training", "data", "intent")
OUTPUT_DIR = os.path.join(BASE_DIR, "models", "intent")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Model
# =========================

MODEL_NAME = "ai4bharat/IndicBERTv2-MLM-Sam-TLM"

# =========================
# Load datasets
# =========================

print("Loading intent datasets...")

train_df = pd.read_csv(os.path.join(DATA_DIR, "train.csv"))
val_df = pd.read_csv(os.path.join(DATA_DIR, "validation.csv"))
test_df = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))

print("Train rows:", len(train_df))
print("Validation rows:", len(val_df))
print("Test rows:", len(test_df))

# =========================
# Intent labels
# =========================

labels = sorted(train_df["label"].unique())

label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

print("\n======================================")
print("INTENTS")
print("======================================")

for i, label in id2label.items():
    print(i, "->", label)

# Convert string labels to integers
train_df["label"] = train_df["label"].map(label2id)
val_df["label"] = val_df["label"].map(label2id)
test_df["label"] = test_df["label"].map(label2id)

# Keep language information out of the classifier input.
# Language will be detected separately by our language model.
train_df = train_df[["text", "label"]]
val_df = val_df[["text", "label"]]
test_df = test_df[["text", "label"]]

# =========================
# Hugging Face datasets
# =========================

train_dataset = Dataset.from_pandas(
    train_df,
    preserve_index=False
)

val_dataset = Dataset.from_pandas(
    val_df,
    preserve_index=False
)

test_dataset = Dataset.from_pandas(
    test_df,
    preserve_index=False
)

# =========================
# Tokenizer
# =========================

print("\nLoading IndicBERT tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=128,
    )

print("Tokenizing datasets...")

train_dataset = train_dataset.map(
    tokenize,
    batched=True
)

val_dataset = val_dataset.map(
    tokenize,
    batched=True
)

test_dataset = test_dataset.map(
    tokenize,
    batched=True
)

# =========================
# Model
# =========================

print("\nLoading IndicBERT classification model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(labels),
    label2id=label2id,
    id2label=id2label,
    ignore_mismatched_sizes=True,
)

# =========================
# Training configuration
# =========================

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    eval_strategy="epoch",
    save_strategy="epoch",

    learning_rate=2e-5,

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    num_train_epochs=5,

    weight_decay=0.01,

    logging_steps=20,

    load_best_model_at_end=True,

    report_to="none",
)

# =========================
# Trainer
# =========================

trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=train_dataset,
    eval_dataset=val_dataset,

    processing_class=tokenizer,
)

# =========================
# Train
# =========================

print("\n======================================")
print("STARTING INTENT MODEL TRAINING")
print("======================================\n")

trainer.train()

# =========================
# Evaluation
# =========================

print("\nEvaluating model...")

results = trainer.evaluate(test_dataset)

print("\n======================================")
print("TEST RESULTS")
print("======================================")

print(results)

# =========================
# Save model
# =========================

print("\nSaving intent detection model...")

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

# =========================
# Save label mappings
# =========================

with open(
    os.path.join(OUTPUT_DIR, "labels.json"),
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        {
            "label2id": label2id,
            "id2label": {
                str(k): v
                for k, v in id2label.items()
            }
        },
        f,
        ensure_ascii=False,
        indent=2
    )

print("\n======================================")
print("TRAINING COMPLETE!")
print("======================================")

print("Model saved to:")
print(OUTPUT_DIR)