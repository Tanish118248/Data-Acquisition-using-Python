import json
import pandas as pd
import re
import os

INPUT_JSON = "../data/raw_extracted.json"
OUTPUT_JSON = "../data/papers_dataset.json"
OUTPUT_CSV = "../data/papers_dataset.csv"

def clean_text(text):
    text = re.sub(r'\s+', ' ', text) 
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) 
    return text.strip()

def clean_data():
    if not os.path.exists(INPUT_JSON):
        print("⚠️ No extracted data found. Please run extract_text.py first.")
        return 

    if os.path.exists(OUTPUT_JSON):
        os.remove(OUTPUT_JSON)
    if os.path.exists(OUTPUT_CSV):
        os.remove(OUTPUT_CSV)
    print("🧹 Old cleaned output files removed.\n")

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    for paper in data:
        title = clean_text(paper.get("title", "Untitled"))
        year_match = re.findall(r'\d{4}', str(paper.get("year", "")))
        year = year_match[0] if year_match else "Unknown"
        file_name = paper.get("file_name", "unknown.pdf")
        full_text = clean_text(paper.get("full_text", ""))

        cleaned.append({
            "title": title,
            "year": year,
            "file_name": file_name,
            "full_text": full_text
        })
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
    print(f"✅ Cleaned JSON saved: {OUTPUT_JSON}")

    df = pd.DataFrame(cleaned)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"✅ Cleaned CSV saved: {OUTPUT_CSV}")
    print(f"📄 Total records cleaned: {len(cleaned)}")

if __name__ == "__main__":
    clean_data()

