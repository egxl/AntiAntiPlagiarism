import subprocess
import sys

# Check for pyperclip and ask the user if they want to install it
try:
    import pyperclip
    clipboard_available = True
except ImportError:
    clipboard_available = False
    print("\nClipboard support (via pyperclip) is not available.")
    choice = input("Do you want to install pyperclip for automatic copying? (Y/N): ").strip().lower()
    if choice == "y":
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
            import pyperclip
            clipboard_available = True
            print("\npyperclip installed successfully.\n")
        except Exception as e:
            print(f"Installation failed: {e}")
            clipboard_available = False
    else:
        print("Continuing without clipboard support.\n")

from random import randint
from colorama import init, Fore, Style
import time
import os

init(convert=True)
init(autoreset=True)

bright = Style.BRIGHT
dim = Style.DIM
red = Fore.RED + bright + dim
green = Fore.GREEN + bright + dim
cyan = Fore.CYAN + bright + dim
yellow = Fore.LIGHTYELLOW_EX + bright + dim
blue = Fore.BLUE + bright + dim
white = Fore.WHITE + bright + dim
magenta = Fore.MAGENTA + bright + dim

FILE_IN = "aap_in.txt"
FILE_OUT = "aap_out.txt"
SINGLE_CHAR = False  # Enable if you have a word limit and don't want aap to use many chars

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    cls()
    mod_str = ""
    input_text = input("\n\n > Introduce a text or press enter: ")

    if input_text == "":
        if not os.path.exists(FILE_IN):
            print(red + "{} could not be found, creating\n".format(FILE_IN))
            open(FILE_IN, "w+", encoding="utf-8").close()
            input()
            main()

        input_file = open(FILE_IN, "r", encoding="utf-8")
        input_text = input_file.read()
        input_file.close()

        if input_text == "":
            print(red + "{} file cannot be empty\n".format(FILE_IN))
            input()
            main()

    mod_words = []

    for word in input_text.split():
        if SINGLE_CHAR:
            middle = int(len(word) / 2)
            mod_word = word[:middle] + "‎" + word[middle:]
        else:
            mod_word = "".join(char + "‎" for char in word)
        mod_words.append(mod_word)

    mod_str = " ".join(mod_words)

    f = open(FILE_OUT, "w", encoding="utf-8")
    f.write(mod_str)
    f.close()
    print(green + "\nResult saved into: {}".format(FILE_OUT))
    print(cyan + "\n{}".format(mod_str))

    if clipboard_available:
        try:
            pyperclip.copy(mod_str)
            print(blue + "\n(The result has been copied to the clipboard)")
        except Exception as e:
            print(red + "\nFailed to copy to clipboard:", e)

    input()
    main()

main()
