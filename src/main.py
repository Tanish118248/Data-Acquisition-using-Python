import tkinter as tk
from tkinter import messagebox
import os
def run_pipeline():
    os.system("python fetch_pdfs.py")
    os.system("python extract_text.py")
    os.system("python clean_data.py")
    messagebox.showinfo("Success", " Pipeline completed successfully!")

root = tk.Tk()
root.title("PDF Data Acquisition")
root.geometry("400x300")
root.configure(bg="#f2f2f2")

title = tk.Label(root, text=" PDF Data Acquisition Tool", font=("Helvetica", 14, "bold"), bg="#f2f2f2")
title.pack(pady=20)

tk.Button(root, text="Run Full Pipeline", command=run_pipeline, width=20, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Download PDFs", command=lambda: os.system("python fetch_pdfs.py"), width=20).pack(pady=5)
tk.Button(root, text="Extract Text", command=lambda: os.system("python extract_text.py"), width=20).pack(pady=5)
tk.Button(root, text="Clean Data", command=lambda: os.system("python clean_data.py"), width=20).pack(pady=5)

tk.Label(root, text="Developed by: Tanish Garg", bg="#f2f2f2", fg="gray", font=("Helvetica", 9)).pack(side="bottom", pady=10)
root.mainloop()
