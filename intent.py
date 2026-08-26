import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_PATH = "models/intent"


# Load trained intent model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()


def detect_intent(text: str) -> str:
    """
    Detect the intent of a weather query using the trained ML model.
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_id = torch.argmax(outputs.logits, dim=1).item()

    return model.config.id2label[predicted_id]