import os

# Get the directory path
scriptPath = os.path.dirname(__file__)

# The size of the main window
WINDOW_WIDTH = 600      # Set the main window width
WINDOW_HEIGHT = 400     # Set the main window height

# The size of the prompt window
PROMPT_WINDOW_WIDTH = 300       # Set the prompt window width
PROMPT_WINDOW_HEIGHT = 150      # Set the prompt window height

# Password Generator configurations
USE_UPPER_CHAR = True   # Should the password include capital letters
USE_SYMBOLS = True      # Should the password include symbols
USE_DIGITS = True       # Should the password include numbers
GENERATED_LENGTH = 15   # How long should the password be

# Fonts family and Fonts size configurations (Affect both password prompt window and main window)
FONTS = "Arial"     # Set your own font family here
FONTS_SIZE = 10     # Set your own font size here

# The script path to find the encryption file and json password file
DATA_ENC = f"{scriptPath}\storage\passwords.enc"
DATA_FILE = f"{scriptPath}\storage\passwords.json"
SALT_BIN = f"{scriptPath}\storage\salt.bin"
MAIN_ICON = f"{scriptPath}\Icons\lock_icon.ico"
