import os
import platform

# Get the root directory path (the linuxPwd/ folder itself, since storage/,
# backend/ and frontend/ all live alongside this file).
scriptPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get the System OS
operatingSystem = platform.system()

# Common services for the combo box
COMMON_SERVICES = [
    "Google",
    "GitHub",
    "Steam",
    "Microsoft",
]

# Theme (see THEMES dict further down for the available names)
THEME_NAME = "Light"

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
osUrandomSize = 16              # How many bytes should the os generate (chunk size is not recommended)
PBKDF2HMAC_Lenght = 32          # How long should the encryption length be
PBKDF2HMAC_iterations = 480000  # How many time should the encryption be hash

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

# --- Theming -----------------------------------------------------------
# Simple light/dark palettes used by the frontend. Feel free to tweak.
LIGHT_THEME = {
    "bg": "#f2f2f2",
    "fg": "#1a1a1a",
    "entry_bg": "#ffffff",
    "entry_fg": "#1a1a1a",
    "button_bg": "#e0e0e0",
    "button_fg": "#1a1a1a",
    "button_active_bg": "#c9c9c9",   # hover/pressed background -- tweak this to change hover color
    "button_active_fg": "#1a1a1a",   # hover/pressed text color
    "tree_bg": "#ffffff",
    "tree_fg": "#1a1a1a",
    "tree_select_bg": "#3d7eff",
    "tree_select_fg": "#ffffff",
    "tree_heading_active_bg": "#c9c9c9",  # column-header hover background
    "tree_heading_active_fg": "#1a1a1a",
    "error_fg": "#c0392b",
}

DARK_THEME = {
    "bg": "#1e1e1e",
    "fg": "#e6e6e6",
    "entry_bg": "#2d2d2d",
    "entry_fg": "#e6e6e6",
    "button_bg": "#3a3a3a",
    "button_fg": "#e6e6e6",
    "button_active_bg": "#505050",   # hover/pressed background -- tweak this to change hover color
    "button_active_fg": "#ffffff",   # hover/pressed text color
    "tree_bg": "#252525",
    "tree_fg": "#e6e6e6",
    "tree_select_bg": "#3d7eff",
    "tree_select_fg": "#ffffff",
    "tree_heading_active_bg": "#4a4a4a",  # column-header hover background
    "tree_heading_active_fg": "#ffffff",
    "error_fg": "#ff6b6b",
}

SOLARIZED_DARK_THEME = {
    "bg": "#002b36",
    "fg": "#93a1a1",
    "entry_bg": "#073642",
    "entry_fg": "#eee8d5",
    "button_bg": "#073642",
    "button_fg": "#93a1a1",
    "button_active_bg": "#586e75",
    "button_active_fg": "#fdf6e3",
    "tree_bg": "#073642",
    "tree_fg": "#93a1a1",
    "tree_select_bg": "#268bd2",
    "tree_select_fg": "#fdf6e3",
    "tree_heading_active_bg": "#586e75",
    "tree_heading_active_fg": "#fdf6e3",
    "error_fg": "#dc322f",
}

NORD_THEME = {
    "bg": "#2e3440",
    "fg": "#eceff4",
    "entry_bg": "#3b4252",
    "entry_fg": "#e5e9f0",
    "button_bg": "#434c5e",
    "button_fg": "#eceff4",
    "button_active_bg": "#4c566a",
    "button_active_fg": "#ffffff",
    "tree_bg": "#3b4252",
    "tree_fg": "#e5e9f0",
    "tree_select_bg": "#88c0d0",
    "tree_select_fg": "#2e3440",
    "tree_heading_active_bg": "#4c566a",
    "tree_heading_active_fg": "#eceff4",
    "error_fg": "#bf616a",
}

DRACULA_THEME = {
    "bg": "#282a36",
    "fg": "#f8f8f2",
    "entry_bg": "#44475a",
    "entry_fg": "#f8f8f2",
    "button_bg": "#44475a",
    "button_fg": "#f8f8f2",
    "button_active_bg": "#6272a4",
    "button_active_fg": "#ffffff",
    "tree_bg": "#21222c",
    "tree_fg": "#f8f8f2",
    "tree_select_bg": "#bd93f9",
    "tree_select_fg": "#282a36",
    "tree_heading_active_bg": "#6272a4",
    "tree_heading_active_fg": "#f8f8f2",
    "error_fg": "#ff5555",
}

TOKYONIGHT_THEME = {
    "bg": "#1a1b26",
    "fg": "#c0caf5",
    "entry_bg": "#24283b",
    "entry_fg": "#c0caf5",
    "button_bg": "#24283b",
    "button_fg": "#c0caf5",
    "button_active_bg": "#414868",
    "button_active_fg": "#ffffff",
    "tree_bg": "#24283b",
    "tree_fg": "#c0caf5",
    "tree_select_bg": "#7aa2f7",
    "tree_select_fg": "#1a1b26",
    "tree_heading_active_bg": "#414868",
    "tree_heading_active_fg": "#ffffff",
    "error_fg": "#f7768e",
}

CATPPUCCIN_MOCHA_THEME = {
    "bg": "#1e1e2e",
    "fg": "#cdd6f4",
    "entry_bg": "#313244",
    "entry_fg": "#cdd6f4",
    "button_bg": "#313244",
    "button_fg": "#cdd6f4",
    "button_active_bg": "#45475a",
    "button_active_fg": "#ffffff",
    "tree_bg": "#313244",
    "tree_fg": "#cdd6f4",
    "tree_select_bg": "#89b4fa",
    "tree_select_fg": "#1e1e2e",
    "tree_heading_active_bg": "#45475a",
    "tree_heading_active_fg": "#ffffff",
    "error_fg": "#f38ba8",
}

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

