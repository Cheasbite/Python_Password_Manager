import os
import tkinter as tk
from tkinter import TclError

from codes.config import DATA_ENC, DATA_FILE, SALT_BIN, load_user_settings
from codes.frontend.Auth import Auth
from codes.frontend.App import App
from codes.backend.logic.decryption import Decryption

def main():
    load_user_settings()  # pull in saved Dark Mode / generator options, if any

    root = tk.Tk()
    root.withdraw()  # stay hidden until we know whether auth succeeded

    fernet = None
    try:
        if os.path.exists(DATA_ENC) and os.path.exists(SALT_BIN):
            fernet = Auth(root).prompt_master_password()
        else:
            fernet = Auth(root).prompt_new_master_password()

        if fernet is None:
            # User closed the auth window instead of unlocking/creating.
            return

        root.deiconify()
        App(root)
        root.mainloop()
    except TclError:
        print("Failed")
    finally:
        if fernet is not None and os.path.exists(DATA_FILE) and os.path.exists(SALT_BIN):
            Decryption().encrypt(DATA_FILE, DATA_ENC, fernet)
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)


if __name__ == "__main__":
    main()

