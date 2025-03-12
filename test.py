import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Test PyTorch
print(torch.__version__)

# Test transformers
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
print("Model and Tokenizer loaded!")