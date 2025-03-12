import re
import os
from dotenv import load_dotenv

load_dotenv()
RAW_TEXT_DIR = os.getenv("RAW_TEXT_DIR")
CLEANED_TEXT_DIR= os.getenv("CLEANED_TEXT_DIR")
os.makedirs(CLEANED_TEXT_DIR, exist_ok=True)

def normalize_line_endings(text):
    normalized_text = re.sub(r"\r\n|\r|\n", "\n", text)
    return normalized_text

def clean_before_chapter_1(text):
    target = r"((\*\*\* START OF )|(The Project Gutenberg eBook))[\s\S]*?(Chapter|CHAPTER) (I|1)(\.\]|\.|)\n\n"
    cleaned_text = re.sub(target, r"Chapter I\n\n", text, flags=re.DOTALL)
    return cleaned_text

def remove_illustrations(text):
    text = re.sub(r"\[_Copyright 1894 by George Allen._\]", "", text)
    text = re.sub(r"\[Illustration(:?\s*[^\]]*)?\]", "", text)
    return text

def clean_after_gutenberg_end(text):
    cleaned_text = re.sub(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*", "", text, flags=re.DOTALL)
    return cleaned_text

def remove_extra_newlines(text):
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    # return re.sub(r"(?<=\S)\n(?=\S)", " ", text) 

def remove_multiple_newlines(text):
    return re.sub(r"\n{3,}", "\n\n", text)

def clean_text(text):
    text = normalize_line_endings(text)
    text = clean_before_chapter_1(text)
    text = remove_illustrations(text)
    text = clean_after_gutenberg_end(text)
    text = remove_extra_newlines(text)
    text = remove_multiple_newlines(text)
    return text

def clean_and_save_texts():
    for filename in os.listdir(RAW_TEXT_DIR):
        filepath = os.path.join(RAW_TEXT_DIR, filename)

        if os.path.isfile(filepath):
            with open(filepath, "r", encoding="utf-8", newline='') as f:
                raw_text = f.read()

            cleaned_text = clean_text(raw_text)

            cleaned_filepath = os.path.join(CLEANED_TEXT_DIR, filename)
            with open(cleaned_filepath, "w", encoding="utf-8", newline='') as f:
                f.write(cleaned_text)

            print(f"Cleaned {filename} saved to: {cleaned_filepath}")

if __name__ == "__main__":
    clean_and_save_texts();                