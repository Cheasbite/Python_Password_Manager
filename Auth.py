import tkinter as tk
from logic import pwd2key, Decryption
from config import *

class Auth:
    def __init__(self, root):
        self.root = root
        self.fernet = None
        self.custom_font = (FONTS, FONTS_SIZE)

    def prompt_master_password(self):
        prompt = tk.Toplevel(self.root)
        prompt.title("Enter Master Password")
        prompt.geometry(f"{PROMPT_WINDOW_WIDTH}x{PROMPT_WINDOW_HEIGHT}")
        prompt.resizable(False, False)
        prompt.attributes('-topmost', -1)

        # Get the window width and height
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        # Center the prompt
        prompt_x = (self.screen_width - PROMPT_WINDOW_WIDTH) // 2
        prompt_y = (self.screen_height - PROMPT_WINDOW_HEIGHT) // 2
        prompt.geometry(f"{PROMPT_WINDOW_WIDTH}x{PROMPT_WINDOW_HEIGHT}+{prompt_x}+{prompt_y}")

        # Block interaction with the root window until this is closed
        prompt.grab_set()

        tk.Label(prompt, text="Enter Master Password:", font=self.custom_font).pack(pady=10)

        # Show or Hide passwords
        self.pwdState = False
        def show_or_hide(event = None):
            self.pwdState = not self.pwdState
            pwd_entry.config(show="" if self.pwdState else "*")

        pwd_entry = tk.Entry(prompt, show="*", width=25, font=self.custom_font)
        pwd_entry.pack()
        pwd_entry.focus()

        error_label = tk.Label(prompt, text="", fg="red")
        error_label.pack()

        def submit(event=None):
            entered = pwd_entry.get()
            try:
                self.fernet = pwd2key().derive_key(entered)
                Decryption().decrypt(DATA_FILE, DATA_ENC, self.fernet)
                prompt.destroy()
            except Exception:
                error_label.config(text="Incorrect password, try again.", font=self.custom_font)
                pwd_entry.delete(0, tk.END)

        tk.Button(prompt, text="Unlock", command=submit).pack(pady=5)
        prompt.bind("<Return>", submit)

        # Prevent closing the prompt without a correct password
        prompt.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

        # Shortcuts
        prompt.bind('<Control-e>', show_or_hide)

        self.root.wait_window(prompt)  # Pause main app until prompt is closed

        return self.fernet

    def prompt_new_master_password(self):
        prompt = tk.Toplevel(self.root)
        prompt.title("Create Master Password")
        prompt.geometry(f"{PROMPT_WINDOW_WIDTH}x{PROMPT_WINDOW_HEIGHT}")
        prompt.resizable(False, False)
        prompt.attributes('-topmost', -1)

        # Get the window width and height
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()

        # Center the prompt
        prompt_x = (self.screen_width - PROMPT_WINDOW_WIDTH) // 2
        prompt_y = (self.screen_height - PROMPT_WINDOW_HEIGHT) // 2
        prompt.geometry(f"{PROMPT_WINDOW_WIDTH}x{PROMPT_WINDOW_HEIGHT}+{prompt_x}+{prompt_y}")

        # Block interaction with the root window until this is closed
        prompt.grab_set()

        tk.Label(prompt, text="Create Master Password:", font=self.custom_font).pack(pady=10)

        # Show or Hide passwords
        self.pwdState = False
        def show_or_hide(event = None):
            self.pwdState = not self.pwdState
            pwd_entry.config(show="" if self.pwdState else "*")

        pwd_entry = tk.Entry(prompt, show="*", width=25, font=self.custom_font)
        pwd_entry.pack()
        pwd_entry.focus()

        error_label = tk.Label(prompt, text="", fg="red")
        error_label.pack()

        def submit(event=None):
            entered = pwd_entry.get()

            if len(entered) == 0:
                error_label.config(text="Incorrect password, try again.", font=self.custom_font)
                pwd_entry.delete(0, tk.END)
                return None

            # Generate the salt
            pwd2key().generate_salt()

            try:
                self.fernet = pwd2key().derive_key(entered)

                with open(DATA_FILE, "rb") as f:
                    jsonbyte = f.read()

                with open(DATA_ENC, "wb") as f:
                    f.write(self.fernet.encrypt(jsonbyte))

                prompt.destroy()
            except Exception:
                error_label.config(text="An error has occured, try again.", font=self.custom_font)
                pwd_entry.delete(0, tk.END)

        create_btn = tk.Button(prompt, text="Create", command=submit)
        create_btn.pack(pady=5)
        prompt.bind("<Return>", submit)

        # Prevent closing the prompt without a correct password
        prompt.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

        # Shortcuts
        prompt.bind('<Control-e>', show_or_hide)

        self.root.wait_window(prompt)  # Pause main app until prompt is closed

        return self.fernet
