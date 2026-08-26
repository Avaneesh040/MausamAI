import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_PATH = "models/language"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()


def detect_language(text: str) -> str:
    """
    Detect the language of the user's query.

    Returns:
        Language code such as:
        en, hi, bn, or, gu, mr, pa, ta, te, kn
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