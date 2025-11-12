import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import os
import webbrowser
import subprocess
import threading
import time

OUTPUT_JSON = "../data/papers_dataset.json"
OUTPUT_CSV = "../data/papers_dataset.csv"

def open_file(file_path):
    if os.path.exists(file_path):
        webbrowser.open(os.path.abspath(file_path))
    else:
        messagebox.showwarning("File Not Found", f"⚠️ {file_path} not found!")

def refresh_output_buttons():
    for widget in output_frame.winfo_children():
        widget.destroy()

    if os.path.exists(OUTPUT_JSON):
        create_button(output_frame, "📄 Open JSON Output", lambda: open_file(OUTPUT_JSON), "#1976D2").pack(pady=5)
    if os.path.exists(OUTPUT_CSV):
        create_button(output_frame, "📊 Open CSV Output", lambda: open_file(OUTPUT_CSV), "#388E3C").pack(pady=5)
    if not (os.path.exists(OUTPUT_JSON) or os.path.exists(OUTPUT_CSV)):
        tk.Label(output_frame, text="No output files yet. Run the pipeline first.", bg="#E8EAF6", fg="gray").pack()

def log_message(message):
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, message + "\n")
    log_box.yview(tk.END)
    log_box.config(state=tk.DISABLED)
    root.update_idletasks()

def create_button(parent, text, command, color):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg="white", font=("Arial", 10, "bold"),
        activebackground=color, relief="flat", width=30, height=1, bd=0
    )
    btn.bind("<Enter>", lambda e: btn.config(bg="#333", fg="white"))
    btn.bind("<Leave>", lambda e: btn.config(bg=color, fg="white"))
    return btn

def run_pipeline_thread():
    progress_bar.start(10)
    log_box.config(state=tk.NORMAL)
    log_box.delete(1.0, tk.END)
    log_message("🚀 Starting the data acquisition pipeline...\n")

    urls = url_text.get("1.0", tk.END).strip().split("\n")
    urls = [u.strip() for u in urls if u.strip()]
    if not urls:
        messagebox.showwarning("No URLs", "Please enter at least one PDF URL before running the pipeline.")
        progress_bar.stop()
        return

    try:
        log_message("📥 Downloading PDFs...")
        subprocess.run(["python", "fetch_pdfs.py", *urls], check=True)

        log_message("🧾 Extracting text from PDFs...")
        subprocess.run(["python", "extract_text.py"], check=True)

        log_message("🧹 Cleaning and organizing data...")
        subprocess.run(["python", "clean_data.py"], check=True)

        progress_bar.stop()
        log_message("✅ Pipeline completed successfully!\n")
        messagebox.showinfo("Success", "🎉 Data Pipeline Completed Successfully!")
    except Exception as e:
        progress_bar.stop()
        log_message(f"❌ Error: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

    refresh_output_buttons()

def run_pipeline():
    thread = threading.Thread(target=run_pipeline_thread)
    thread.start()

root = tk.Tk()
root.title("📚 AI-Based PDF Data Acquisition")
root.geometry("720x700")
root.configure(bg="#E8EAF6")

header = tk.Frame(root, bg="#3F51B5", height=80)
header.pack(fill="x")
tk.Label(
    header, text="AI-Based PDF Data Acquisition System",
    font=("Helvetica", 18, "bold"), fg="white", bg="#3F51B5"
).pack(pady=20)

tk.Label(root, text="🔗 Enter PDF URLs (one per line):", font=("Arial", 11, "bold"), bg="#E8EAF6", fg="#212121").pack(pady=8)
url_text = scrolledtext.ScrolledText(root, width=75, height=6, font=("Arial", 10), wrap=tk.WORD, relief="solid", bd=1)
url_text.pack(pady=6)

button_frame = tk.Frame(root, bg="#E8EAF6")
button_frame.pack(pady=15)

create_button(button_frame, "▶ Run Full Pipeline", run_pipeline, "#4CAF50").pack(pady=6)
create_button(button_frame, "⬇ Download PDFs Only", lambda: subprocess.run(["python", "fetch_pdfs.py"]), "#2196F3").pack(pady=6)
create_button(button_frame, "📄 Extract Text Only", lambda: subprocess.run(["python", "extract_text.py"]), "#FFC107").pack(pady=6)
create_button(button_frame, "🧹 Clean Data Only", lambda: subprocess.run(["python", "clean_data.py"]), "#9C27B0").pack(pady=6)

progress_bar = ttk.Progressbar(root, mode="indeterminate", length=300)
progress_bar.pack(pady=10)

tk.Label(root, text="📜 Live Pipeline Logs:", font=("Arial", 11, "bold"), bg="#E8EAF6", fg="#212121").pack(pady=5)
log_box = scrolledtext.ScrolledText(root, width=85, height=10, font=("Consolas", 9), bg="#FAFAFA", state=tk.DISABLED, relief="ridge", bd=1)
log_box.pack(pady=5)

tk.Label(root, text="📂 Output Files:", font=("Helvetica", 12, "bold"), bg="#E8EAF6", fg="#212121").pack(pady=10)
output_frame = tk.Frame(root, bg="#E8EAF6")
output_frame.pack()
refresh_output_buttons()

footer = tk.Frame(root, bg="#3F51B5", height=50)
footer.pack(fill="x", side="bottom")
tk.Label(
    footer, text="Developed by: Tanish Garg | AI & Data Systems", fg="white", bg="#3F51B5",
    font=("Arial", 10, "italic")
).pack(pady=10)

root.mainloop()



