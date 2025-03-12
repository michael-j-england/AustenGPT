import os
from dotenv import load_dotenv
from datasets import load_dataset, DatasetDict
from model_utils import load_tokenizer

def tokenize_and_save():
    load_dotenv()
    CLEANED_TEXT_DIR = os.getenv("CLEANED_TEXT_DIR")
    TOKENIZED_TEXT_DIR = os.getenv("TOKENIZED_TEXT_DIR")
    os.makedirs(TOKENIZED_TEXT_DIR, exist_ok=True)

    data_files = {"train": os.path.join(CLEANED_TEXT_DIR, "*.txt")}
    dataset = load_dataset("text", data_files=data_files)

    tokenizer = load_tokenizer()

    def tokenize_function(examples):
        outputs = tokenizer(
            examples["text"],
            padding="max_length",
            truncation=True,
            max_length=512,  # Ensures uniform input length
        )
        outputs["labels"] = outputs["input_ids"].copy()
        return outputs

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    split_ratio = 0.1
    split = tokenized_dataset["train"].train_test_split(test_size=split_ratio)
    split_dataset = DatasetDict({"train": split["train"], "test": split["test"]})
    split_dataset.save_to_disk(TOKENIZED_TEXT_DIR)

    print(f"Tokenized dataset saved to {TOKENIZED_TEXT_DIR}")

if __name__ == "__main__":
    tokenize_and_save()   