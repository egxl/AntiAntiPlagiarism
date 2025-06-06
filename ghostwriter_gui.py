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
        self.auto_copy_enabled = tk.BooleanVar(value=True)
        self.enter_key_enabled = tk.BooleanVar(value=True)  # New toggle for Enter key
        
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
        
        # Center frame for Enter key toggle
        center_frame = tk.Frame(settings_frame)
        center_frame.pack(side="left", expand=True)
        
        enter_frame = tk.Frame(center_frame)
        enter_frame.pack()
        
        tk.Label(enter_frame, text="Enter Key:", font=('Segoe UI', 10)).pack(side="left", padx=(20, 5))
        enter_toggle = tk.Checkbutton(
            enter_frame, 
            text="Auto Encode", 
            variable=self.enter_key_enabled,
            command=self.toggle_enter_key,
            font=('Segoe UI', 10)
        )
        enter_toggle.pack(side="left")
        
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
        self.input_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Bind Enter key events
        self.setup_enter_key_bindings()

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
        self.output_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Status message label
        self.status_text = tk.Label(self.root, text="", justify="center", font=("Segoe UI", 9), height=1)
        self.status_text.pack(fill="x", padx=10, pady=(0, 5))

        # Statistics label with centered positioning
        self.stats_text = tk.Label(self.root, text="", justify="center", font=("Segoe UI", 10), anchor="center")
        self.stats_text.pack(fill="x", padx=10, pady=10)
        
        # Store references to themed widgets for updates
        self.themed_widgets = {
            'frames': [settings_frame, theme_frame, center_frame, enter_frame, copy_frame, button_frame],
            'labels': [theme_frame.winfo_children()[0], enter_frame.winfo_children()[0], copy_frame.winfo_children()[0]],
            'checkbuttons': [theme_frame.winfo_children()[1], enter_frame.winfo_children()[1], copy_frame.winfo_children()[1]],
            'texts': [self.input_text, self.output_text],
            'stats_label': self.stats_text,
            'status_label': self.status_text
        }
        
        # Apply initial theme
        self.update_widget_colors()

    def setup_enter_key_bindings(self):
        """Setup Enter key bindings for the input text widget"""
        # Bind Return (Enter) key
        self.input_text.bind('<Return>', self.on_enter_key)
        # Bind Shift+Return for line breaks when enter key is enabled
        self.input_text.bind('<Shift-Return>', self.on_shift_enter)

    def on_enter_key(self, event):
        """Handle Enter key press in input text"""
        if self.enter_key_enabled.get():
            # Prevent default behavior (adding newline)
            self.encode_action()
            return 'break'
        else:
            # Allow default behavior (add newline)
            return None

    def on_shift_enter(self, event):
        """Handle Shift+Enter key press in input text"""
        if self.enter_key_enabled.get():
            # Insert newline when Enter key auto-encode is enabled
            self.input_text.insert(tk.INSERT, '\n')
            return 'break'
        else:
            # Allow default behavior
            return None

    def toggle_enter_key(self):
        """Toggle Enter key functionality and update status"""
        if self.enter_key_enabled.get():
            self.show_status_message("✓ Enter key auto-encode enabled (Shift+Enter for line breaks)")
        else:
            self.show_status_message("✓ Enter key auto-encode disabled (Enter for line breaks)")

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
        
        # Update status label
        self.themed_widgets['status_label'].configure(bg=colors['bg'], fg=colors['label_fg'])

    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self.apply_theme()
        self.update_ttk_style()
        self.update_widget_colors()

    def show_status_message(self, message, duration=2000):
        """Show a temporary status message"""
        self.status_text.config(text=message)
        # Clear the message after specified duration
        self.root.after(duration, lambda: self.status_text.config(text=""))

    def auto_copy_if_enabled(self, content):
        """Automatically copy content to clipboard if auto-copy is enabled"""
        if self.auto_copy_enabled.get() and content:
            pyperclip.copy(content)
            # Show status message instead of popup
            self.show_status_message("✓ Output automatically copied to clipboard")

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
            self.show_status_message("✓ Text copied to clipboard")
        else:
            messagebox.showwarning("Nothing to copy", "Output area is empty.")

    def clear_fields(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.stats_text.config(text="")

    def batch_mode(self):
        # Create a dialog to choose operation type
        batch_window = tk.Toplevel(self.root)
        batch_window.title("Batch Mode Options")
        batch_window.configure(bg=self.themes['dark' if self.is_dark_mode.get() else 'light']['bg'])
        batch_window.transient(self.root)
        batch_window.grab_set()
        batch_window.resizable(False, False)  # Make window non-resizable for consistent layout
        
        colors = self.themes['dark' if self.is_dark_mode.get() else 'light']
        
        # Main container with padding
        main_frame = tk.Frame(batch_window, bg=colors['bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Operation selection
        tk.Label(main_frame, text="Select Operation:", font=('Segoe UI', 12, 'bold'),
                bg=colors['bg'], fg=colors['label_fg']).pack(pady=(0, 10))
        
        operation_var = tk.StringVar(value="encode")
        
        tk.Radiobutton(main_frame, text="Encode Files", variable=operation_var, value="encode",
                      font=('Segoe UI', 10), bg=colors['bg'], fg=colors['label_fg'],
                      selectcolor=colors['text_bg'], activebackground=colors['bg']).pack(pady=2, anchor="w")
        
        tk.Radiobutton(main_frame, text="Decode Files", variable=operation_var, value="decode",
                      font=('Segoe UI', 10), bg=colors['bg'], fg=colors['label_fg'],
                      selectcolor=colors['text_bg'], activebackground=colors['bg']).pack(pady=2, anchor="w")
        
        # Input selection
        tk.Label(main_frame, text="Select Input:", font=('Segoe UI', 12, 'bold'),
                bg=colors['bg'], fg=colors['label_fg']).pack(pady=(20, 10))
        
        input_var = tk.StringVar(value="files")
        
        tk.Radiobutton(main_frame, text="Select Multiple Files", variable=input_var, value="files",
                      font=('Segoe UI', 10), bg=colors['bg'], fg=colors['label_fg'],
                      selectcolor=colors['text_bg'], activebackground=colors['bg']).pack(pady=2, anchor="w")
        
        tk.Radiobutton(main_frame, text="Select Folder", variable=input_var, value="folder",
                      font=('Segoe UI', 10), bg=colors['bg'], fg=colors['label_fg'],
                      selectcolor=colors['text_bg'], activebackground=colors['bg']).pack(pady=2, anchor="w")
        
        # File selection area
        file_frame = tk.Frame(main_frame, bg=colors['bg'])
        file_frame.pack(fill="x", pady=(20, 0))
        
        tk.Label(file_frame, text="Selected Files:", font=('Segoe UI', 10, 'bold'),
                bg=colors['bg'], fg=colors['label_fg']).pack(anchor="w")
        
        # Listbox to show selected files
        list_frame = tk.Frame(file_frame, bg=colors['bg'])
        list_frame.pack(fill="x", pady=(5, 10))
        
        files_listbox = tk.Listbox(list_frame, height=4, bg=colors['text_bg'], fg=colors['text_fg'],
                                  selectbackground='#0078d4', font=('Segoe UI', 9))
        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        files_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=files_listbox.yview)
        
        files_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Store selected files
        selected_files = []
        
        def update_file_display():
            files_listbox.delete(0, tk.END)
            if selected_files:
                for file_path in selected_files:
                    filename = os.path.basename(file_path)
                    files_listbox.insert(tk.END, filename)
            else:
                files_listbox.insert(tk.END, "No files selected")
        
        def select_files():
            nonlocal selected_files
            if input_var.get() == "files":
                # Select multiple files
                file_paths = filedialog.askopenfilenames(
                    title=f"Select files to {operation_var.get()}",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    parent=batch_window
                )
                if file_paths:  # Only update if files were selected (not cancelled)
                    selected_files = list(file_paths)
            else:
                # Select folder
                folder = filedialog.askdirectory(
                    title=f"Select folder containing files to {operation_var.get()}",
                    parent=batch_window
                )
                if folder:  # Only update if folder was selected (not cancelled)
                    selected_files = []
                    for filename in os.listdir(folder):
                        if filename.endswith(".txt"):
                            selected_files.append(os.path.join(folder, filename))
            
            update_file_display()
        
        # Select files button
        ttk.Button(file_frame, text="Browse Files", command=select_files).pack(pady=(0, 10))
        
        # Initialize display
        update_file_display()
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=colors['bg'])
        button_frame.pack(pady=(10, 0))
        
        def start_batch():
            if not selected_files:
                messagebox.showwarning("No Files Selected", "Please select files before starting batch processing.", parent=batch_window)
                return
            
            batch_window.destroy()
            self.execute_batch_operation(operation_var.get(), selected_files)
        
        ttk.Button(button_frame, text="Start Processing", command=start_batch).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Cancel", command=batch_window.destroy).pack(side="left", padx=10)
        
        # Set proper window size after all widgets are created
        batch_window.update_idletasks()  # Ensure all widgets are rendered
        width = 450
        height = 480
        x = self.root.winfo_rootx() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_rooty() + (self.root.winfo_height() // 2) - (height // 2)
        batch_window.geometry(f"{width}x{height}+{x}+{y}")

    def execute_batch_operation(self, operation, selected_files):
        # Get script directory for output folders
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Process files first, only create output directory if we have results
        results = []
        errors = []
        
        for filepath in selected_files:
            try:
                with open(filepath, 'r', encoding="utf-8") as f:
                    content = f.read()
                
                if operation == "encode":
                    processed_content = encode_text(content)
                    filename = os.path.basename(filepath)
                    new_filename = f"encoded_{filename}"
                else:
                    processed_content = decode_text(content)
                    filename = os.path.basename(filepath)
                    new_filename = f"decoded_{filename}"
                
                results.append((processed_content, new_filename))
                
            except Exception as e:
                filename = os.path.basename(filepath)
                errors.append(f"{filename}: {str(e)}")
        
        # Only create output directory and save files if we have successful results
        if results:
            if operation == "encode":
                output_dir = os.path.join(script_dir, "Encoded Output")
            else:
                output_dir = os.path.join(script_dir, "Decoded Output")
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Save all processed files
            saved_files = []
            for processed_content, new_filename in results:
                try:
                    output_path = os.path.join(output_dir, new_filename)
                    with open(output_path, 'w', encoding="utf-8") as f:
                        f.write(processed_content)
                    saved_files.append(new_filename)
                except Exception as e:
                    errors.append(f"{new_filename}: Failed to save - {str(e)}")
            
            # Show results
            if saved_files:
                success_msg = f"Successfully {operation}d {len(saved_files)} files.\nOutput saved to: {output_dir}"
                if errors:
                    error_msg = f"\n\nErrors encountered:\n" + "\n".join(errors[:5])
                    if len(errors) > 5:
                        error_msg += f"\n... and {len(errors) - 5} more errors"
                    messagebox.showinfo("Batch Complete", success_msg + error_msg)
                else:
                    messagebox.showinfo("Batch Complete", success_msg)
                    self.show_status_message(f"✓ Batch {operation} completed: {len(saved_files)} files processed")
            else:
                messagebox.showerror("Batch Failed", "No files were saved successfully.\n\nErrors:\n" + "\n".join(errors[:10]))
        else:
            messagebox.showerror("Batch Failed", "No files were processed successfully.\n\nErrors:\n" + "\n".join(errors[:10]))

    def display_stats(self, original, modified):
        stats = get_text_statistics(original, modified)
        stat_text = "\n".join([f"{k}: {v}" for k, v in stats.items()])
        self.stats_text.config(text=stat_text)


if __name__ == '__main__':
    root = tk.Tk()
    app = AntiAntiPlagiarismApp(root)
    root.mainloop()
