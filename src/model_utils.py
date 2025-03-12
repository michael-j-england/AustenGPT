from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model(model_name="gpt2"):
    return AutoModelForCausalLM.from_pretrained(model_name)

def load_tokenizer(model_name="gpt2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token 
    return tokenizer
