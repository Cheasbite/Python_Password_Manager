import os
from .theme import *

# Get the root directory path (the linuxPwd/ folder itself, since storage/,
# backend/ and frontend/ all live alongside this file).
scriptPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Common services for the combo box
COMMON_SERVICES = [
    "Google",
    "GitHub",
    "Steam",
    "Microsoft",
]

# The size of the main window
WINDOW_WIDTH = 600      # Set the main window width
WINDOW_HEIGHT = 400     # Set the main window height

# The size of the prompt window
PROMPT_WINDOW_WIDTH = 320       # Set the prompt window width
PROMPT_WINDOW_HEIGHT = 170      # Set the prompt window height

# Password Generator configurations
USE_UPPER_CHAR = True   # Should the password include capital letters
USE_SYMBOLS = True      # Should the password include symbols
USE_DIGITS = True       # Should the password include numbers
GENERATED_LENGTH = 15   # How long should the password be

# Security
# Reference for the amount of iterations should be used:
# https://github.com/cudocharles/OWASP-CheatSheetSeries/blob/master/cheatsheets/Password_Storage_Cheat_Sheet.md#pbkdf2
ALLOW_LOWER_ITERATION = False   # If set to true, you can lower the PBKDF2HMAC_iterations (not recommended)
osUrandomSize = 16              # How many bytes should the os generate (chunk size is not recommended)
PBKDF2HMAC_Lenght = 32          # How long should the encryption length be
PBKDF2HMAC_iterations = 600000  # How many time should the encryption be hash

# Fonts family and Fonts size configurations (Affect both password prompt window and main window)
FONTS = "JetBrainsMono Nerd Font"     # Set your own font family here
FONTS_SIZE = 10     # Set your own font size here

# The script path to find the encryption file and json password file
# (os.path.join is used so this works correctly on both Windows and Linux)
DATA_ENC = os.path.join(scriptPath, "storage", "passwords.enc")
DATA_FILE = os.path.join(scriptPath, "storage", "passwords.json")
SALT_BIN = os.path.join(scriptPath, "storage", "salt.bin")
SETTINGS_FILE = os.path.join(scriptPath, "storage", "settings.json")
MAIN_ICON = os.path.join(scriptPath, "Icons", "lock_icon.ico")

# Registry of all selectable themes. The Settings dialog's combobox is
# populated straight from this dict's keys, so adding a new theme is just
# adding one more entry here -- every palette needs the same set of keys
# as the ones above.
THEMES = {
    "Light": LIGHT_THEME,
    "Dark": DARK_THEME,
    "Solarized Dark": SOLARIZED_DARK_THEME,
    "Nord": NORD_THEME,
    "Dracula": DRACULA_THEME,
    "Tokyo Night": TOKYONIGHT_THEME,
    "Catppuccin Mocha": CATPPUCCIN_MOCHA_THEME,
}

def theme():
    """Return the palette dict for the current THEME_NAME, falling back to
    Light if that name isn't in THEMES for some reason (e.g. an old
    settings.json referencing a theme that got renamed/removed)."""
    return THEMES.get(THEME_NAME, LIGHT_THEME)

def button_style(colors=None):
    """Kwargs to spread into every tk.Button(...) call so hover/pressed
    colors are always set explicitly (rather than falling back to the
    system default, which is usually a stark white). Change
    button_active_bg / button_active_fg in LIGHT_THEME / DARK_THEME above
    to customize the hover color everywhere at once.

        tk.Button(parent, text="Save", command=save, **config.button_style(self.colors))
    """
    c = colors or theme()
    return {
        "bg": c["button_bg"],
        "fg": c["button_fg"],
        "activebackground": c["button_active_bg"],
        "activeforeground": c["button_active_fg"],
    }

def check_style(colors=None):
    """Same idea as button_style(), but for tk.Checkbutton / tk.Radiobutton.
    These default to a plain background/foreground with no active state set,
    which is what caused the hover-highlight-doesn't-match-theme bug --
    without this, moving the mouse over a checkbox falls back to the
    system's default (usually white) hover color.

        tk.Checkbutton(parent, text="...", variable=v, **config.check_style(self.colors))
    """
    c = colors or theme()
    return {
        "bg": c["bg"],
        "fg": c["fg"],
        "activebackground": c["button_active_bg"],
        "activeforeground": c["button_active_fg"],
        "selectcolor": c["entry_bg"],
        "background": c["button_bg"]
    }

def load_user_settings():
    """Overwrite the defaults above with whatever was saved from the
    Settings dialog last time (storage/settings.json). Safe to call even
    if the file doesn't exist yet -- defaults just stay as-is.

    Other modules that need these values while the app is running should
    read them off this module (e.g. `config.THEME_NAME`) rather than
    `from .config import THEME_NAME`, since the latter freezes the value
    at import time and won't see later changes.
    """
    import json

    global THEME_NAME, USE_UPPER_CHAR, USE_SYMBOLS, USE_DIGITS, GENERATED_LENGTH

    if not os.path.exists(SETTINGS_FILE):
        return

    try:
        with open(SETTINGS_FILE, "r") as f:
            saved = json.load(f)
    except (json.JSONDecodeError, OSError):
        return

    saved_theme = saved.get("theme_name")
    if saved_theme is None:
        # Migrate an old settings.json from before themes were a thing.
        saved_theme = "Dark" if saved.get("dark_mode") else "Light"
    THEME_NAME = saved_theme if saved_theme in THEMES else THEME_NAME

    USE_UPPER_CHAR = saved.get("use_upper_char", USE_UPPER_CHAR)
    USE_SYMBOLS = saved.get("use_symbols", USE_SYMBOLS)
    USE_DIGITS = saved.get("use_digits", USE_DIGITS)
    GENERATED_LENGTH = saved.get("generated_length", GENERATED_LENGTH)

def save_user_settings():
    """Persist the current settings to storage/settings.json."""
    import json

    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(
            {
                "theme_name": THEME_NAME,
                "use_upper_char": USE_UPPER_CHAR,
                "use_symbols": USE_SYMBOLS,
                "use_digits": USE_DIGITS,
                "generated_length": GENERATED_LENGTH,
            },
            f,
            indent=4,
        )

