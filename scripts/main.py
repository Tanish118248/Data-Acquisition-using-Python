import os

print("🚀 Starting PDF Data Acquisition Pipeline...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.system(f'python "{os.path.join(BASE_DIR, "fetch_pdfs.py")}"')
os.system(f'python "{os.path.join(BASE_DIR, "extract_text.py")}"')
os.system(f'python "{os.path.join(BASE_DIR, "clean_data.py")}"')

print("🎯 Pipeline completed successfully!")

