import fitz  # PyMuPDF
import os
import json

PDF_DIR = "../data/raw_pdfs"
OUTPUT_JSON = "../data/raw_extracted.json"

def extract_from_pdfs():
    extracted_data = []
    for pdf_file in os.listdir(PDF_DIR):
        if not pdf_file.endswith(".pdf"):
            continue
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        metadata = doc.metadata
        title = metadata.get("title") or pdf_file.replace(".pdf", "")
        year = metadata.get("creationDate", "Unknown")[2:6] if metadata.get("creationDate") else "Unknown"
        extracted_data.append({
            "file_name": pdf_file,
            "title": title.strip(),
            "year": year,
            "full_text": text.strip()
        })
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)
    print(f"✅ Extracted data saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    extract_from_pdfs()
