from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "language"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

texts = [
    "What is the weather in Delhi today?",
    "कल दिल्ली में मौसम कैसा रहेगा?",
    "દિલ્હીમાં હવામાન કેવું છે?",
    "आज दिल्ली में बारिश होगी क्या?",
    "சென்னையில் இன்று வானிலை எப்படி இருக்கும்?",
    "ఈ రోజు చెన్నైలో వాతావరణం ఎలా ఉంటుంది?",
    "ಚೆನ್ನೈನಲ್ಲಿ ಇಂದು ಹವಾಮಾನ ಹೇಗಿದೆ?",
    "दिल्लीतील हवामान कसे आहे?",
]

for text in texts:

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_id = torch.argmax(outputs.logits, dim=-1).item()

    predicted_language = model.config.id2label[predicted_id]

    print()
    print("Text:", text)
    print("Detected language:", predicted_language)