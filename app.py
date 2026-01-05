from flask import Flask, render_template, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import requests

app = Flask(__name__)

# Load BERT model for headline classification
model_path = "saved_fake_news_model"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()
labels = ["FAKE", "REAL"]

# Load GPT-2 model for headline generation
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_model.eval()

# NewsAPI key
NEWS_API_KEY = "2328520a9e384ba9b6508792738035b4"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic", "")
    if not topic:
        return jsonify({"headline": "⚠️ No topic provided."}), 400

    # Generate headline using GPT-2
    input_ids = gpt2_tokenizer.encode(topic, return_tensors="pt", max_length=50, truncation=True)
    with torch.no_grad():
        outputs = gpt2_model.generate(
            input_ids,
            max_length=30,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_p=0.95,
            top_k=50,
            temperature=0.9,
            do_sample=True,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )
    generated_text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({"headline": generated_text})

@app.route("/classify", methods=["POST"])
def classify():
    data = request.get_json()
    headline = data.get("headline", "")
    if not headline:
        return jsonify({"prediction": "⚠️ No headline provided."}), 400

    inputs = tokenizer(headline, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        prediction_id = torch.argmax(logits, dim=-1).item()

    return jsonify({"prediction": labels[prediction_id]})

@app.route("/fetch_news", methods=["GET"])
def fetch_news():
    query = request.args.get("q", "technology")
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=5&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article["title"],
                "content": article["content"] or article["description"],
                "url": article["url"],
                "source": article["source"]["name"],
                "publishedAt": article["publishedAt"]
            })

        return jsonify({"articles": articles})
    except Exception as e:
        print("News fetch error:", e)
        return jsonify({"error": "Failed to fetch news"}), 500

if __name__ == "__main__":
    app.run(debug=True)
