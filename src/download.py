import os
import requests
from tqdm import tqdm 
from dotenv import load_dotenv

# Jane Austen's six main movels and their Gutenberg IDs
austen_books = {
    "Pride and Prejudice": 1342,
    "Sense and Sensibility": 161,
    "Emma": 158,
    "Mansfield Park": 141,
    "Northanger Abbey": 121,
    "Persuasion": 105,
}

load_dotenv()
RAW_TEXT_DIR = os.getenv("RAW_TEXT_DIR")
os.makedirs(RAW_TEXT_DIR, exist_ok=True)

# Function to download the raw text from Project Gutenberg
def get_austen_text(book_id):
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching book {book_id}: {e}")
        return None

# Download texts and save them locally
def download_and_save_books(austen_books, output_dir):
    austen_texts = []

    for title, book_id in tqdm(austen_books.items(), desc="Downloading Austen Texts"):
        text = get_austen_text(book_id)
        if text:
            austen_texts.append({"title": title, "text": text})

    for book in austen_texts:
        title = book['title']
        text = book['text']
        filename = f"{title}.txt"
        filepath = os.path.join(output_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8", newline='') as f:
                f.write(text)
            print(f"{title} saved to: {filepath}")
        except Exception as e:
            print(f"Error saving {title}: {e}")


if __name__ == "__main__":    
    download_and_save_books(austen_books, RAW_TEXT_DIR)
