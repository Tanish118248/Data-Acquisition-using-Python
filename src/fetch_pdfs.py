import os
import requests
from tqdm import tqdm
import sys

DATA_DIR = "../data/raw_pdfs"
os.makedirs(DATA_DIR, exist_ok=True)

def clear_old_pdfs():
    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            os.remove(os.path.join(DATA_DIR, file))
    print("🧹 Cleared old PDFs before downloading new ones.\n")

def download_pdfs(urls):
    clear_old_pdfs() 
    for url in tqdm(urls, desc="Downloading PDFs"):
        filename = os.path.join(DATA_DIR, os.path.basename(url))
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"✅ Downloaded: {filename}")
            else:
                print(f"❌ Failed: {url}")
        except Exception as e:
            print(f"⚠️ Error downloading {url}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        pdf_urls = sys.argv[1:]
        download_pdfs(pdf_urls)
    else:
        print("⚠️ No URLs provided. Please pass URLs as command-line arguments.")
