from transformers import TrainingArguments

args = TrainingArguments(
    output_dir="./test_output",
    eval_strategy="epoch",  # Use 'eval_strategy' for transformers 4.54.1
    per_device_train_batch_size=8,
    num_train_epochs=1
)

print("✅ TrainingArguments works!")
