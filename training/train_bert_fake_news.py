from datasets import load_dataset
from transformers import (
    BertTokenizer,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding,
)
import numpy as np
import evaluate

# Load dataset
dataset = load_dataset("csv", data_files={"train": "train.csv", "test": "test.csv"}, delimiter=",")

# Load tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Tokenization function
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

# Tokenize dataset
dataset = dataset.map(tokenize, batched=True)

# Set dataset format for PyTorch
dataset["train"].set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
dataset["test"].set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# Load model
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

# Data collator (important to fix variable-length error)
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# Metric
accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return accuracy.compute(predictions=predictions, references=labels)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    logging_dir="./logs",
    logging_steps=100,
    eval_strategy="epoch",  # ✅ FIXED HERE
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
    greater_is_better=True,
)


# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics
)

# Start training
trainer.train()

# Save the trained model
model.save_pretrained("saved_fake_news_model")
tokenizer.save_pretrained("saved_fake_news_model")
