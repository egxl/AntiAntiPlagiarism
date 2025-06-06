# 🕵️‍♂️ GhostWriter-GUI

**GhostWriter** is a tool that introduces invisible Unicode characters into text, making it appear different to automated similarity or plagiarism detectors—while remaining identical to human readers.

> ⚠️ This project is intended strictly for **educational and research purposes only**. Misuse of this tool to violate academic integrity policies or institutional rules is strongly discouraged and may carry consequences. Use responsibly.

---

## 🙏 Acknowledgments

GhostWriter is inspired by [tikene/AntiAntiPlagiarism](https://github.com/tikene/AntiAntiPlagiarism), and builds on it with multiple improvements:
- GUI version with user-friendly features
- Live statistics, theming, batch processing
- Decoding support
- CLI version with clipboard support

---

## 🧪 How It Works

Plagiarism detectors often compare exact substrings or similar n-gram matches between texts. GhostWriter introduces invisible characters (e.g. **Braille Pattern Blank** `U+2800`) between letters or in the middle of words. This disrupts pattern-based comparison algorithms without affecting what humans see.

Example:

```
"example" → "e[​]x[​]a[​]m[​]p[​]l[​]e"
```

(Where `[​]` represents an invisible Unicode character.)

---

## 🖥️ GUI Version

```bash
python ghostwriter_gui.py
```

Features:

* Dark/light mode toggle
* Auto-copy output
* Enter key auto-encode option
* Batch processing of `.txt` files or folders
* Entropy and character statistics
* Manual Encode / Decode / Copy / Clear actions

---

## 🔄 Decoding Support (GUI only)

The GUI includes a **Decode** button that restores previously encoded texts to their original form. This is useful for:

* Reversing obfuscation
* Making encoded text editable
* Safe reuse of original content

> Decoding is currently supported only in the GUI.

---

## 🔄 Improvements in `antiantiplagiarism.py`

The updated CLI script is functionally the same as `[antiantiplagiarism.py](https://github.com/tikene/AntiAntiPlagiarism/blob/main/antiantiplagiarism.py)`, but with one key improvement:

- ✅ **Automatic clipboard support**  
  After encoding, the output is automatically copied to the clipboard (if `pyperclip` is installed).  
  If `pyperclip` is missing, the script will offer to install it.

> This simplifies copying results for quick use and avoids manual steps.

---

## 🧑‍💻 CLI Usage

```bash
python antiantiplagiarism.py
````

* Paste or type a string, or leave blank to read from `aap_in.txt`.
* Output is saved to `aap_out.txt` and optionally copied to your clipboard.
* You’ll be prompted to install `pyperclip` if it's not found.

---

## ⚙️ Encoding Modes *(WIP)*

* **Full Mode** *(default)*: Inserts an invisible Unicode character between every letter.
* **Single Mode**: Inserts one character per word (useful when limited by word count).

The mode is currently toggled manually via `SINGLE_CHAR` in the code. GUI support is in development.

---

## 📁 Project Structure

```

GhostWriter-GUI/
├── ghostwriter_gui.py        # GUI version with themes, batch mode, clipboard support
├── antiantiplagiarism.py     # Updated CLI version
├── LICENSE
└── README.md

````

---

## 📜 License

This project is licensed under the terms of the [MIT License](LICENSE).
