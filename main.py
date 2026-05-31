import tkinter as tk
import os
from functions.config import *
from functions.logic import Decryption
from functions.App import App
from functions.Auth import Auth

def main():
    root = tk.Tk()
    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (screen_w - 300) // 2, (screen_h - 200) // 2
    root.geometry(f"300x200+{x}+{y}")
    root.resizable(False, False)

    try:
        if os.path.exists(DATA_ENC) and os.path.exists(SALT_BIN):
            fernet = Auth(root).prompt_master_password()
        else:
            fernet = Auth(root).prompt_new_master_password()

        App(root)
        root.mainloop()
    except tk.TclError:
        print("Failed")
        exit()
    finally:
        if os.path.exists(DATA_FILE) and os.path.exists(SALT_BIN):
            Decryption().encrypt(DATA_FILE, DATA_ENC, fernet)
            os.remove(DATA_FILE)
        else:
            print(None)

if __name__ == "__main__":
    main()
