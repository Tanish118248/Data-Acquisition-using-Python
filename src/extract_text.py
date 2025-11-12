import fitz 
import os
import json

PDF_DIR = "../data/raw_pdfs"
OUTPUT_JSON = "../data/raw_extracted.json"

def extract_from_pdfs():
    extracted_data = []

    # ✅ Step 1: Check if folder exists and has PDFs
    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR)
        print("📂 Created missing raw_pdfs folder. Please add some PDF files.")
        return

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No PDF files found in ../data/raw_pdfs/. Please run fetch_pdfs.py first.")
        return

    # ✅ Step 2: Remove old extraction file
    if os.path.exists(OUTPUT_JSON):
        os.remove(OUTPUT_JSON)
        print("🧹 Old extraction file removed.\n")

    # ✅ Step 3: Extract text and metadata from PDFs
    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            metadata = doc.metadata
            title = metadata.get("title") or pdf_file.replace(".pdf", "")
            year = "Unknown"
            if metadata.get("creationDate"):
                year_candidate = metadata["creationDate"][2:6]
                if year_candidate.isdigit():
                    year = year_candidate

            extracted_data.append({
                "file_name": pdf_file,
                "title": title.strip(),
                "year": year,
                "full_text": text.strip()
            })
            print(f"✅ Extracted text from: {pdf_file}")
        except Exception as e:
            print(f"⚠️ Error reading {pdf_file}: {e}")

    # ✅ Step 4: Save the extracted data
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Extracted data saved to {OUTPUT_JSON}")
    print(f"📄 Total papers processed: {len(extracted_data)}")

if __name__ == "__main__":
    extract_from_pdfs()
