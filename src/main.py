import tkinter as tk
from tkinter import messagebox
import os
import webbrowser

OUTPUT_JSON = "../data/papers_dataset.json"
OUTPUT_CSV = "../data/papers_dataset.csv"

def run_pipeline():
    
    os.system("python fetch_pdfs.py")
    os.system("python extract_text.py")
    os.system("python clean_data.py")

    messagebox.showinfo("Success", "✅ Pipeline completed successfully!")
    refresh_output_buttons()

def open_file(file_path):
    if os.path.exists(file_path):
        webbrowser.open(os.path.abspath(file_path))
    else:
        messagebox.showwarning("File Not Found", f"⚠️ {file_path} not found!")

def refresh_output_buttons():
    for widget in output_frame.winfo_children():
        widget.destroy()

    if os.path.exists(OUTPUT_JSON):
        tk.Button(
            output_frame, text="📄 Open JSON Output", 
            command=lambda: open_file(OUTPUT_JSON),
            width=25, bg="#1976D2", fg="white"
        ).pack(pady=5)

    if os.path.exists(OUTPUT_CSV):
        tk.Button(
            output_frame, text="📊 Open CSV Output", 
            command=lambda: open_file(OUTPUT_CSV),
            width=25, bg="#388E3C", fg="white"
        ).pack(pady=5)

    if not os.path.exists(OUTPUT_JSON) and not os.path.exists(OUTPUT_CSV):
        tk.Label(
            output_frame, text="No output files yet. Run the pipeline first.", bg="#f2f2f2", fg="gray").pack()

root = tk.Tk()
root.title("PDF Data Acquisition Tool")
root.geometry("450x400")
root.configure(bg="#f2f2f2")

title = tk.Label(root, text="📚 AI-Based PDF Data Acquisition", font=("Helvetica", 14, "bold"), bg="#f2f2f2")
title.pack(pady=20)

tk.Button(root, text="▶ Run Full Pipeline", command=run_pipeline, width=25, bg="#4CAF50", fg="white").pack(pady=8)
tk.Button(root, text="⬇ Download PDFs", command=lambda: os.system("python fetch_pdfs.py"), width=25).pack(pady=5)
tk.Button(root, text="📄 Extract Text", command=lambda: os.system("python extract_text.py"), width=25).pack(pady=5)
tk.Button(root, text="🧹 Clean Data", command=lambda: os.system("python clean_data.py"), width=25).pack(pady=5)

tk.Label(root, text="Output Files:", font=("Helvetica", 11, "bold"), bg="#f2f2f2").pack(pady=10)
output_frame = tk.Frame(root, bg="#f2f2f2")
output_frame.pack()

refresh_output_buttons()

tk.Label(root, text="Developed by: Tanish Garg", bg="#f2f2f2", fg="gray", font=("Helvetica", 9)).pack(side="bottom", pady=10)

root.mainloop()

