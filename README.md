# 📰 Fake News Generator & Detector using Generative AI and NLP

This project demonstrates how AI can both **create and detect fake news**. It combines:
- 🤖 **GPT-2** for generating realistic fake news articles (guided by real news)
- 🕵️‍♂️ **BERT** for detecting real vs. fake headlines
- 🌐 **NewsAPI + Google Search** for live article feed and fact verification

> Built with Python, Flask, HTML/CSS/JS, and Hugging Face Transformers.

---

## 🚀 Features

- ✍️ Generate fake news articles using GPT-2 with real-time guidance
- 🕵️ Classify headlines as FAKE or REAL with reasoning
- 🌐 Browse live news by topic or category
- 📋 Explanations for detection results
- 💻 Built with Flask + modern web frontend

---

## 📁 Folder Structure

```
fake-news-project/
│
├── app.py
├── predict_fake_news.py
├── requirements.txt
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── saved_fake_news_model/
│   ├── config.json
│   ├── model.safetensors       👈 [PLACE HERE]
│   ├── tokenizer_config.json
│   ├── vocab.txt
│   └── special_tokens_map.json
│
├── LICENSE
└── README.md
```

---

## 🧪 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/fake-news-project.git
cd fake-news-project
```

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask torch transformers requests
```

---

### 3️⃣ 🔽 Download the BERT Classification Model

The `model.safetensors` file is **not included** due to size limits.  
👉 **[Click here to download model.safetensors from Google Drive](https://drive.google.com/uc?export=download&id=1H-PIKN2eV-aHzZQtczQGCddFJjtgKuB-)**

After downloading:

```bash
mkdir -p saved_fake_news_model
mv ~/Downloads/model.safetensors saved_fake_news_model/
```

> ✅ It must be saved to:
```
fake-news-project/saved_fake_news_model/model.safetensors
```

---

### 4️⃣ ⚙️ Set API Keys

In `app.py`, replace the placeholders with your actual keys:

```python
NEWS_API_KEY = "your_newsapi_key"
GOOGLE_API_KEY = "your_google_api_key"
CSE_ID = "your_google_search_engine_id"
```

---

### 5️⃣ ▶️ Run the App

```bash
python app.py
```

Visit the app at: [http://localhost:5000](http://localhost:5000)

---


## 🎯 Want to Train Your Own Model?

If you'd like to retrain the fake news detection model:

- Check the **`training/`** folder (if included) for:
  - 📁 Dataset used for training
  - 🧠 Python code to fine-tune BERT
- You can customize, experiment, and improve the detector
- The **already trained model** (`model.safetensors`) is provided in `saved_fake_news_model/`

> Perfect if you want to try new datasets or improve accuracy.

---
