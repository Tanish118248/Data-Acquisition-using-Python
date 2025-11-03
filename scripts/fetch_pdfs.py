import os
import requests
from tqdm import tqdm

DATA_DIR = "../data/raw_pdfs"
os.makedirs(DATA_DIR, exist_ok=True)

pdf_urls = [
    "https://arxiv.org/pdf/2106.01361.pdf",
    "https://arxiv.org/pdf/2001.08361.pdf",
    "https://arxiv.org/pdf/2106.00001.pdf",
]

def download_pdfs(urls):
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
            print(f"⚠️ Error: {url} | {e}")

if __name__ == "__main__":
    download_pdfs(pdf_urls)
