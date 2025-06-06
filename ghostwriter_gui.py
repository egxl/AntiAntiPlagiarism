import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import pyperclip
import math
from collections import Counter

ZERO_WIDTH_CHAR = "\u200E"


def encode_text(text, single_char=False):
    mod_words = []
    for word in text.split():
        if single_char:
            middle = len(word) // 2
            mod_word = word[:middle] + ZERO_WIDTH_CHAR + word[middle:]
        else:
            mod_word = ''.join(char + ZERO_WIDTH_CHAR for char in word)
        mod_words.append(mod_word)
    return ' '.join(mod_words)


def decode_text(text):
    return text.replace(ZERO_WIDTH_CHAR, '')


def calc_entropy(s):
    prob = [n_x / len(s) for x, n_x in Counter(s).items()]
    entropy = -sum([p * math.log2(p) for p in prob])
    return round(entropy, 4)


def get_text_statistics(original, modified):
    inserted = modified.count(ZERO_WIDTH_CHAR)
    return {
        "Characters Inserted": inserted,
        "Original Length": len(original),
        "Modified Length": len(modified),
        "Entropy Original": calc_entropy(original),
        "Entropy Modified": calc_entropy(modified)
    }


class AntiAntiPlagiarismApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anti-Anti-Plagiarism Encoder")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 10), padding=6)

        self.input_text = tk.Text(self.root, height=10, wrap="word", bg="#2e2e2e", fg="white")
        self.input_text.pack(fill="x", padx=10, pady=5)

        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Encode", command=self.encode_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Decode", command=self.decode_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Batch Mode", command=self.batch_mode).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side="left", padx=5)

        self.output_text = tk.Text(self.root, height=10, wrap="word", bg="#2e2e2e", fg="white")
        self.output_text.pack(fill="x", padx=10, pady=5)

        self.stats_text = tk.Label(self.root, text="", fg="#c0c0c0", bg="#1e1e1e", justify="left", font=("Segoe UI", 10))
        self.stats_text.pack(fill="x", padx=10)

    def encode_action(self):
        raw = self.input_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("Input missing", "Please enter some text to encode.")
            return
        result = encode_text(raw)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.display_stats(raw, result)

    def decode_action(self):
        raw = self.output_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("Output empty", "There is nothing to decode.")
            return
        decoded = decode_text(raw)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", decoded)
        self.display_stats(decoded, raw)  # reversing the order to reflect decoding

    def copy_to_clipboard(self):
        content = self.output_text.get("1.0", "end").strip()
        if content:
            pyperclip.copy(content)
            messagebox.showinfo("Copied", "Text copied to clipboard.")

    def clear_fields(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.stats_text.config(text="")

    def batch_mode(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        results = []
        for filename in os.listdir(folder):
            if filename.endswith(".txt"):
                filepath = os.path.join(folder, filename)
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                encoded = encode_text(content)
                new_filename = f"encoded_{filename}"
                with open(os.path.join(folder, new_filename), "w", encoding="utf-8") as f:
                    f.write(encoded)
                results.append(new_filename)
        messagebox.showinfo("Batch Complete", f"Processed {len(results)} files.")

    def display_stats(self, original, modified):
        stats = get_text_statistics(original, modified)
        stat_text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
        self.stats_text.config(text=stat_text)


if __name__ == '__main__':
    root = tk.Tk()
    app = AntiAntiPlagiarismApp(root)
    root.mainloop()
