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
        self.root.geometry("900x650")
        
        # Initialize theme variables
        self.is_dark_mode = tk.BooleanVar(value=True)
        self.auto_copy_enabled = tk.BooleanVar(value=False)
        
        # Define color schemes
        self.themes = {
            'dark': {
                'bg': '#1e1e1e',
                'text_bg': '#2e2e2e',
                'text_fg': 'white',
                'label_fg': '#c0c0c0'
            },
            'light': {
                'bg': '#f0f0f0',
                'text_bg': 'white',
                'text_fg': 'black',
                'label_fg': '#333333'
            }
        }
        
        self.apply_theme()
        self.setup_ui()

    def apply_theme(self):
        """Apply the current theme to the root window"""
        theme = 'dark' if self.is_dark_mode.get() else 'light'
        colors = self.themes[theme]
        self.root.configure(bg=colors['bg'])

    def setup_ui(self):
        # Configure ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.update_ttk_style()

        # Settings frame at the top
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        # Dark/Light mode toggle
        theme_frame = tk.Frame(settings_frame)
        theme_frame.pack(side="left")
        
        tk.Label(theme_frame, text="Theme:", font=('Segoe UI', 10)).pack(side="left", padx=(0, 5))
        theme_toggle = tk.Checkbutton(
            theme_frame, 
            text="Dark Mode", 
            variable=self.is_dark_mode,
            command=self.toggle_theme,
            font=('Segoe UI', 10)
        )
        theme_toggle.pack(side="left")
        
        # Auto-copy toggle
        copy_frame = tk.Frame(settings_frame)
        copy_frame.pack(side="right")
        
        tk.Label(copy_frame, text="Auto-copy:", font=('Segoe UI', 10)).pack(side="left", padx=(0, 5))
        copy_toggle = tk.Checkbutton(
            copy_frame, 
            text="Enable", 
            variable=self.auto_copy_enabled,
            font=('Segoe UI', 10)
        )
        copy_toggle.pack(side="left")

        # Input text area
        self.input_text = tk.Text(self.root, height=10, wrap="word")
        self.input_text.pack(fill="x", padx=10, pady=5)

        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="Encode", command=self.encode_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Decode", command=self.decode_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Batch Mode", command=self.batch_mode).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_fields).pack(side="left", padx=5)

        # Output text area
        self.output_text = tk.Text(self.root, height=10, wrap="word")
        self.output_text.pack(fill="x", padx=10, pady=5)

        # Statistics label
        self.stats_text = tk.Label(self.root, text="", justify="left", font=("Segoe UI", 10))
        self.stats_text.pack(fill="x", padx=10)
        
        # Store references to themed widgets for updates
        self.themed_widgets = {
            'frames': [settings_frame, theme_frame, copy_frame, button_frame],
            'labels': [theme_frame.winfo_children()[0], copy_frame.winfo_children()[0]],
            'checkbuttons': [theme_frame.winfo_children()[1], copy_frame.winfo_children()[1]],
            'texts': [self.input_text, self.output_text],
            'stats_label': self.stats_text
        }
        
        # Apply initial theme
        self.update_widget_colors()

    def update_ttk_style(self):
        """Update ttk widget styles based on current theme"""
        if self.is_dark_mode.get():
            self.style.configure('TButton', 
                               font=('Segoe UI', 10), 
                               padding=6,
                               background='#404040',
                               foreground='white')
        else:
            self.style.configure('TButton', 
                               font=('Segoe UI', 10), 
                               padding=6,
                               background='#e0e0e0',
                               foreground='black')

    def update_widget_colors(self):
        """Update colors of all widgets based on current theme"""
        theme = 'dark' if self.is_dark_mode.get() else 'light'
        colors = self.themes[theme]
        
        # Update frames
        for frame in self.themed_widgets['frames']:
            frame.configure(bg=colors['bg'])
        
        # Update labels
        for label in self.themed_widgets['labels']:
            label.configure(bg=colors['bg'], fg=colors['label_fg'])
        
        # Update checkbuttons
        for checkbutton in self.themed_widgets['checkbuttons']:
            checkbutton.configure(bg=colors['bg'], fg=colors['label_fg'],
                                selectcolor=colors['text_bg'],
                                activebackground=colors['bg'])
        
        # Update text widgets
        for text_widget in self.themed_widgets['texts']:
            text_widget.configure(bg=colors['text_bg'], fg=colors['text_fg'],
                                insertbackground=colors['text_fg'])
        
        # Update stats label
        self.themed_widgets['stats_label'].configure(bg=colors['bg'], fg=colors['label_fg'])

    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.apply_theme()
        self.update_ttk_style()
        self.update_widget_colors()

    def auto_copy_if_enabled(self, content):
        """Automatically copy content to clipboard if auto-copy is enabled"""
        if self.auto_copy_enabled.get() and content:
            pyperclip.copy(content)
            # Show a brief status message
            self.root.after(100, lambda: messagebox.showinfo("Auto-copied", "Output automatically copied to clipboard!", parent=self.root))

    def encode_action(self):
        raw = self.input_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("Input missing", "Please enter some text to encode.")
            return
        result = encode_text(raw)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.display_stats(raw, result)
        
        # Auto-copy if enabled
        self.auto_copy_if_enabled(result)

    def decode_action(self):
        raw = self.output_text.get("1.0", "end").strip()
        if not raw:
            messagebox.showwarning("Output empty", "There is nothing to decode.")
            return
        decoded = decode_text(raw)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", decoded)
        self.display_stats(decoded, raw)  # reversing the order to reflect decoding
        
        # Auto-copy if enabled
        self.auto_copy_if_enabled(decoded)

    def copy_to_clipboard(self):
        content = self.output_text.get("1.0", "end").strip()
        if content:
            pyperclip.copy(content)
            messagebox.showinfo("Copied", "Text copied to clipboard.")
        else:
            messagebox.showwarning("Nothing to copy", "Output area is empty.")

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
