from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load model and tokenizer
model_path = "saved_fake_news_model"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()

# Labels: 0 = FAKE, 1 = REAL
labels = ["FAKE", "REAL"]

print("🧠 Fake News Detector (BERT)")
print("Type a news headline or article below. Type 'exit' to quit.\n")

while True:
    text = input("Enter headline/article:\n> ").strip()

    if text.lower() == "exit":
        print("👋 Exiting detector.")
        break

    if not text:
        print("⚠️ Please enter some text.")
        continue

    # Tokenize and classify
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_id = torch.argmax(logits, dim=-1).item()

    print(f"✅ Prediction: {labels[predicted_id]}\n")
