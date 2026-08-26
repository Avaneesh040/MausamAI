from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_PATH = r"C:\Users\KIIT\Weather\models\intent"

print("Loading intent model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.eval()

print("Model loaded!\n")

def predict_intent(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_id = torch.argmax(outputs.logits, dim=1).item()

    return model.config.id2label[predicted_id]


test_queries = [
    "Will it rain tomorrow?",
    "What is the temperature in Delhi?",
    "How humid is Mumbai today?",
    "How strong will the wind be?",
    "Is there a weather warning?",
    "What will the weather be like tomorrow?",
    "क्या कल बारिश होगी?",
    "दिल्ली में तापमान कितना रहेगा?",
    "आज मौसम कैसा है?"
]

print("======================================")
print("INTENT MODEL TEST")
print("======================================")

for query in test_queries:
    intent = predict_intent(query)

    print(f"\nQuery:  {query}")
    print(f"Intent: {intent}")