import json
import pandas as pd
import re

INPUT_JSON = "../data/raw_extracted.json"
OUTPUT_JSON = "../data/papers_dataset.json"
OUTPUT_CSV = "../data/papers_dataset.csv"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def clean_data():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    cleaned = []
    for paper in data:
        title = clean_text(paper.get("title", "Untitled"))
        year = re.findall(r'\d{4}', paper.get("year", ""))
        full_text = clean_text(paper.get("full_text", ""))
        cleaned.append({
            "title": title,
            "year": year[0] if year else "Unknown",
            "file_name": paper["file_name"],
            "full_text": full_text
        })
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
    df = pd.DataFrame(cleaned)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"✅ Clean JSON saved: {OUTPUT_JSON}")
    print(f"✅ Clean CSV saved: {OUTPUT_CSV}")

if __name__ == "__main__":
    clean_data()
