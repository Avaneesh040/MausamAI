import os
import pandas as pd
import torch

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)

# ============================================================
# 1. Paths
# ============================================================

BASE_DIR = r"C:\Users\KIIT\Weather"

TRAIN_FILE = os.path.join(
    BASE_DIR, "training", "data", "language", "train.csv"
)

VALIDATION_FILE = os.path.join(
    BASE_DIR, "training", "data", "language", "validation.csv"
)

TEST_FILE = os.path.join(
    BASE_DIR, "training", "data", "language", "test.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR, "models", "language"
)

# ============================================================
# 2. Language labels
# ============================================================

LABELS = [
    "en",  # English
    "hi",  # Hindi
    "bn",  # Bengali
    "or",  # Odia
    "gu",  # Gujarati
    "mr",  # Marathi
    "pa",  # Punjabi
    "ta",  # Tamil
    "te",  # Telugu
    "kn",  # Kannada
]

label2id = {label: i for i, label in enumerate(LABELS)}
id2label = {i: label for i, label in enumerate(LABELS)}

print("Languages:")
print(label2id)

# ============================================================
# 3. Load CSV files
# ============================================================

print("\nLoading datasets...")

train_df = pd.read_csv(TRAIN_FILE)
validation_df = pd.read_csv(VALIDATION_FILE)
test_df = pd.read_csv(TEST_FILE)

print(f"Training examples:   {len(train_df)}")
print(f"Validation examples: {len(validation_df)}")
print(f"Test examples:       {len(test_df)}")

# Make sure the expected columns exist
for name, df in [
    ("train", train_df),
    ("validation", validation_df),
    ("test", test_df),
]:
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError(
            f"{name}.csv must contain 'text' and 'label' columns."
        )

# Check labels
all_labels = set(train_df["label"]) | set(validation_df["label"]) | set(test_df["label"])

unknown_labels = all_labels - set(LABELS)

if unknown_labels:
    raise ValueError(
        f"Unknown language labels found: {unknown_labels}"
    )

# Convert language labels to integer IDs
train_df["label"] = train_df["label"].map(label2id)
validation_df["label"] = validation_df["label"].map(label2id)
test_df["label"] = test_df["label"].map(label2id)

# Convert pandas -> Hugging Face Dataset
train_dataset = Dataset.from_pandas(
    train_df[["text", "label"]],
    preserve_index=False
)

validation_dataset = Dataset.from_pandas(
    validation_df[["text", "label"]],
    preserve_index=False
)

test_dataset = Dataset.from_pandas(
    test_df[["text", "label"]],
    preserve_index=False
)

# ============================================================
# 4. Load IndicBERT
# ============================================================

MODEL_NAME = "ai4bharat/IndicBERTv2-MLM-Sam-TLM"

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading IndicBERT classification model...")

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS),
    label2id=label2id,
    id2label=id2label,
    ignore_mismatched_sizes=True,
)

print("IndicBERT loaded.")

# ============================================================
# 5. Tokenization
# ============================================================

def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=128,
    )


print("\nTokenizing datasets...")

train_dataset = train_dataset.map(
    tokenize,
    batched=True,
)

validation_dataset = validation_dataset.map(
    tokenize,
    batched=True,
)

test_dataset = test_dataset.map(
    tokenize,
    batched=True,
)

# ============================================================
# 6. Evaluation metric
# ============================================================

def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    predictions = predictions.argmax(axis=-1)

    accuracy = (predictions == labels).mean()

    return {
        "accuracy": accuracy
    }

# ============================================================
# 7. Training configuration
# ============================================================

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    num_train_epochs=5,

    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,

    learning_rate=2e-5,

    weight_decay=0.01,

    eval_strategy="epoch",
    save_strategy="epoch",

    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,

    logging_steps=10,

    report_to="none",

    fp16=False,
)

# ============================================================
# 8. Trainer
# ============================================================

trainer = Trainer(
    model=model,
    args=training_args,

    train_dataset=train_dataset,
    eval_dataset=validation_dataset,

    processing_class=tokenizer,

    compute_metrics=compute_metrics,
)

# ============================================================
# 9. Train
# ============================================================

print("\n========================================")
print("Starting language detection training")
print("========================================\n")

trainer.train()

# ============================================================
# 10. Test the model
# ============================================================

print("\n========================================")
print("Evaluating on test dataset")
print("========================================\n")

test_results = trainer.evaluate(test_dataset)

print("Test results:")
print(test_results)

# ============================================================
# 11. Save final model
# ============================================================

print("\nSaving language detection model...")

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("\n========================================")
print("Training complete!")
print(f"Model saved to: {OUTPUT_DIR}")
print("========================================")