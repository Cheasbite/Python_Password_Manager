import tkinter as tk
import os

from ..backend.logic.pwd2key import pwd2key
from ..backend.logic.decryption import Decryption
from ..config import *


class Auth:
    """Handles the two entry points into the app:
    - prompt_master_password():     vault already exists -> ask to unlock
    - prompt_new_master_password():  first run -> ask to create one

    Both return a `Fernet` instance (or None if the user closed the window,
    which main.py treats as "quit without doing anything").
    """

    def __init__(self, root):
        self.root = root
        self.fernet = None
        self.custom_font = (FONTS, FONTS_SIZE)
        self.colors = theme()

    def _new_centered_toplevel(self, title, width=PROMPT_WINDOW_WIDTH, height=PROMPT_WINDOW_HEIGHT):
        prompt = tk.Toplevel(self.root)
        prompt.title(title)
        prompt.resizable(False, False)
        prompt.attributes("-topmost", True)
        prompt.configure(bg=self.colors["bg"])

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        prompt.geometry(f"{width}x{height}+{x}+{y}")

        # Block interaction with the root window until this is closed
        prompt.grab_set()
        return prompt

    def prompt_master_password(self):
        prompt = self._new_centered_toplevel("Enter Master Password")

        tk.Label(
            prompt, text="Enter Master Password:",
            font=self.custom_font, bg=self.colors["bg"], fg=self.colors["fg"],
        ).pack(pady=10)

        self.pwdState = False

        def show_or_hide(event=None):
            self.pwdState = not self.pwdState
            pwd_entry.config(show="" if self.pwdState else "*")

        pwd_entry = tk.Entry(
            prompt, show="*", width=25, font=self.custom_font,
            bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
            insertbackground=self.colors["entry_fg"],
        )
        pwd_entry.pack()
        pwd_entry.focus()

        error_label = tk.Label(prompt, text="", fg=self.colors["error_fg"], bg=self.colors["bg"])
        error_label.pack()

        def _upgrade_iterations_if_needed(entered):
            try:
                if ALLOW_LOWER_ITERATION:
                    pwd2key().generate_salt()
                    new_fernet = pwd2key().derive_key(entered)
                    Decryption().encrypt(DATA_FILE, DATA_ENC, new_fernet)  # re-encrypt NOW, not at exit
                    self.fernet = new_fernet
                    raise Exception("ALLOW_LOWER_ITERATION was set to true!")

                _, iteration = pwd2key().load_salt()
                if iteration >= PBKDF2HMAC_iterations:
                    print(f"\033[93mPBKDF2HMAC_iterations is lower than current iteration={iteration}! Enable ALLOW_LOWER_ITERATION to lower the iteration!\033[00m" if iteration > PBKDF2HMAC_iterations else "")
                    return  # already current (or higher -- never downgrade)

                pwd2key().generate_salt()
                new_fernet = pwd2key().derive_key(entered)
                Decryption().encrypt(DATA_FILE, DATA_ENC, new_fernet)  # re-encrypt NOW, not at exit
                self.fernet = new_fernet
            except Exception as e:
                print(f"\033[93m{e}\033[00m")
                pass  # best-effort; vault stays perfectly usable at its current iteration count

        def submit(event=None):
            entered = pwd_entry.get()
            try:
                self.fernet = pwd2key().derive_key(entered)
                Decryption().decrypt(DATA_FILE, DATA_ENC, self.fernet)
                prompt.destroy()
            except Exception:
                self.fernet = None
                error_label.config(text="Incorrect password, try again.", font=self.custom_font)
                pwd_entry.delete(0, tk.END)

            # Lower the timing window of when writing the new iteration!
            _upgrade_iterations_if_needed(entered)

        def cancel(event=None):
            # Escape here quits the app entirely -- there is nothing "behind"
            # the unlock screen to return to.
            self.fernet = None
            prompt.destroy()
            self.root.destroy()

        tk.Button(
            prompt, text="Unlock", command=submit,
            **button_style(self.colors),
        ).pack(pady=5)

        prompt.bind("<Return>", submit)
        prompt.bind("<Escape>", cancel)
        prompt.bind("<Control-e>", show_or_hide)

        # Prevent closing the prompt without a correct password (the X button
        # quits the whole app rather than leaving it half-open)
        prompt.protocol("WM_DELETE_WINDOW", cancel)

        self.root.wait_window(prompt)  # Pause main app until prompt is closed
        return self.fernet

    def prompt_new_master_password(self, width = PROMPT_WINDOW_WIDTH, height = PROMPT_WINDOW_HEIGHT):
        prompt = self._new_centered_toplevel("Create Master Password")

        tk.Label(
            prompt, text="Create Master Password:",
            font=self.custom_font, bg=self.colors["bg"], fg=self.colors["fg"],
        ).pack(pady=10)

        self.pwdState = False

        def show_or_hide(event=None):
            self.pwdState = not self.pwdState
            pwd_entry.config(show="" if self.pwdState else "*")

        pwd_entry = tk.Entry(
            prompt, show="*", width=25, font=self.custom_font,
            bg=self.colors["entry_bg"], fg=self.colors["entry_fg"],
            insertbackground=self.colors["entry_fg"],
        )
        pwd_entry.pack()
        pwd_entry.focus()

        error_label = tk.Label(prompt, text="", fg=self.colors["error_fg"], bg=self.colors["bg"])
        error_label.pack()

        def cancel(event=None):
            self.fernet = None
            prompt.destroy()
            self.root.destroy()

        def submit(event=None):
            entered = pwd_entry.get()

            if len(entered) == 0:
                error_label.config(text="Password cannot be empty.", font=self.custom_font)
                pwd_entry.delete(0, tk.END)
                return None

            confirmation = tk.Toplevel(prompt)
            confirmation.title("Confirmation")
            sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight(),
            x, y = (sw - width) // 2, (sh - height) // 2
            confirmation.geometry(f"+{x - 50}+{y}")
            confirmation.resizable(False, False)
            confirmation.configure(bg=self.colors["bg"])
            confirmation.grab_set()
            confirmation.focus_set()

            tk.Label(
                confirmation,
                text=f"Are you sure [{entered}] is your Master Password?",
                font=self.custom_font, bg=self.colors["bg"], fg=self.colors["fg"],
            ).grid(row=0, column=0, columnspan=2, padx=(45, 20), pady=(30, 20), sticky="w")

            tk.Label(
                confirmation,
                text="Remember this password -- there is no way to recover it.",
                fg=self.colors["error_fg"], bg=self.colors["bg"],
                font=(FONTS, FONTS_SIZE, "bold"),
            ).grid(row=1, column=0, padx=(40, 20), columnspan=2, sticky="w")

            def on_no():
                confirmation.destroy()

            def on_yes():
                try:
                    # Make sure storage/ exists and there is a plaintext
                    # vault file to seed before we derive the key + encrypt it.
                    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
                    if not os.path.exists(DATA_FILE):
                        with open(DATA_FILE, "w") as f:
                            f.write("{}")

                    pwd2key().generate_salt()
                    self.fernet = pwd2key().derive_key(entered)

                    with open(DATA_FILE, "rb") as f:
                        jsonbyte = f.read()

                    with open(DATA_ENC, "wb") as f:
                        f.write(self.fernet.encrypt(jsonbyte))

                    confirmation.destroy()
                    prompt.destroy()
                except Exception:
                    self.fernet = None
                    confirmation.destroy()
                    error_label.config(text="An error has occurred, try again.", font=self.custom_font)
                    pwd_entry.delete(0, tk.END)

            tk.Button(
                confirmation, text="No", width=8, command=on_no,
                bg="#c0392b", fg="white", activebackground="#e74c3c", activeforeground="white",
                font=self.custom_font,
            ).grid(row=2, column=0, padx=(60, 5), pady=(10, 20), sticky="w")

            tk.Button(
                confirmation, text="Yes", width=8, command=on_yes,
                bg="#27ae60", fg="white", activebackground="#2ecc71", activeforeground="white",
                font=self.custom_font,
            ).grid(row=2, column=1, padx=5, pady=(10, 20), sticky="w")

            confirmation.bind("<Escape>", lambda e: on_no())

        create_btn = tk.Button(
            prompt, text="Create", command=submit,
            **button_style(self.colors),
        )
        create_btn.pack(pady=5)

        prompt.bind("<Return>", submit)
        prompt.bind("<Escape>", cancel)
        prompt.bind("<Control-e>", show_or_hide)

        prompt.protocol("WM_DELETE_WINDOW", cancel)

        self.root.wait_window(prompt)  # Pause main app until prompt is closed
        return self.fernet

