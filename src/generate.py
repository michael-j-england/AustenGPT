import os
from transformers import pipeline
from dotenv import load_dotenv

# Load fine-tuned model
load_dotenv()
MODEL_DIR = os.getenv("MODEL_DIR")
generator = pipeline("text-generation", model=MODEL_DIR)

# Generate text
prompt = "It is a truth universally acknowledged"
output = generator(
    prompt,
    max_length=300,
    num_return_sequences=1,
    temperature=0.4,  # Adjusts randomness
    top_p=0.5,        # Nucleus sampling
    repetition_penalty=1.2,  # Penalizes repetitive output
    do_sample=True,  # Enables sampling instead of greedy decoding
)

# Print result
print(output[0]["generated_text"])