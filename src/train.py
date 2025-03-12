import os
from datasets import load_from_disk
from transformers import TrainingArguments, Trainer, EarlyStoppingCallback
import torch
from dotenv import load_dotenv
from model_utils import load_model, load_tokenizer

def train():
    load_dotenv()
    TOKENIZED_TEXT_DIR = os.getenv("TOKENIZED_TEXT_DIR")
    MODEL_DIR = os.getenv("MODEL_DIR")
    os.makedirs(MODEL_DIR, exist_ok=True)

    tokenized_datasets = load_from_disk(TOKENIZED_TEXT_DIR)

    # Select training and evaluation sets (use .select(range(x)) for subsets)
    train_dataset = tokenized_datasets["train"].select(range(1000))
    eval_dataset = tokenized_datasets["test"].select(range(200))

    # Disable Weights & Biases logging
    os.environ["WANDB_DISABLED"] = "true"

    model = load_model()
    tokenizer = load_tokenizer()

    # Training arguments
    training_args = TrainingArguments(
        output_dir=MODEL_DIR,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=False,
        per_device_train_batch_size=1, #8,
        per_device_eval_batch_size=1, #8,
        num_train_epochs=1, # 5
        weight_decay=0.01,
        logging_dir="./logs",
        save_total_limit=2,
        learning_rate=5e-5,
        gradient_accumulation_steps=2,
        fp16=torch.cuda.is_available(),  # Enables mixed-precision training if GPU available
        logging_steps=100,
    )

    # Early stopping callback
    early_stopping = EarlyStoppingCallback(
        early_stopping_patience=2,
        early_stopping_threshold=0.02,
    )

    # Initialize Trainer    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        callbacks=[early_stopping],
    )

    # Train the model
    trainer.train()

    # Save model and tokenizer
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)
    print(f"Model saved to {MODEL_DIR}")

if __name__ == "__main__":
    train()