from bs4 import BeautifulSoup
import html
import re
import unicodedata
import string
import pandas as pd

def clean_description(html_description):
    # 1. Parse and remove HTML tags
    soup = BeautifulSoup(html_description, 'html.parser')
    text = soup.get_text(separator="\n")  # keep structure with newlines

    # 2. Decode HTML entities (&amp;, etc)
    text = html.unescape(text)

    # 3. Normalize weird unicode characters
    text = unicodedata.normalize("NFKD", text)

    # 4. Fix encoding artifacts (â€™, ðŸ’°, etc)
    text = text.encode("latin1", errors="ignore").decode("utf-8", errors="ignore")

    # 5. Clean up excess whitespace
    text = re.sub(r'\n+', '\n', text)           # collapse multiple newlines
    text = re.sub(r'[ \t]+', ' ', text)         # collapse spaces/tabs
    text = text.strip()

    return text

def preprocess(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_dataset(csv_path, output_path="remoteok_jobs_cleaned.csv"):
    df = pd.read_csv(csv_path)
    df["clean_description"] = df["description"].apply(clean_description)
    df["preprocessed_description"] = df["clean_description"].apply(preprocess)
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")

# Example usage (uncomment if testing standalone)
# preprocess_dataset("remoteok_analyst_jobs.csv")
