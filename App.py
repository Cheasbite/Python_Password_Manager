import tkinter as tk
import pyperclip
from tkinter import messagebox, ttk
from logic import PasswordsConfig, Functionality
from config import *

class App:
    def __init__(self, root, fernet = None):
        self.root = root
        self.title = self.root.title("Password Manager v2.1.0")
        self.resize = self.root.resizable(width=False, height=False)
        self.icon = self.root.iconbitmap(MAIN_ICON)
        self.fernet = fernet
        self.custom_font = (FONTS, FONTS_SIZE)
        self.pwdConfig = PasswordsConfig()
        self.func = Functionality()

        self.home()

    def home(self):
        self.isHide = True

        # Center the window position
        self.screen_width, self.screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        WINDOW_X, WINDOW_Y = (self.screen_width - WINDOW_WIDTH) // 2, (self.screen_height - WINDOW_HEIGHT) // 2

        # Window Size and Position
        self.posRoot = self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{WINDOW_X}+{WINDOW_Y}")

        # Frame for buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)

        self.add_btn = tk.Button(btn_frame,
                                 text="Add Password",
                                 command=self.add_password_window,
                                 bg="lime",
                                 activebackground="green",
                                 font=self.custom_font
                                 )
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.del_btn = tk.Button(btn_frame,
                                 text="Delete Password",
                                 command=self.delete_password_window,
                                 bg="red",
                                 activebackground="crimson",
                                 font=self.custom_font
                                 )
        self.del_btn.pack(side=tk.LEFT, padx=5)

        self.hide_pwd_btn = tk.Button(btn_frame,
                                 text="Show Password",
                                 command=self.hs_load_table,
                                 bg="aqua",
                                 activebackground="indigo",
                                 font=self.custom_font
                                 )
        self.hide_pwd_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_btn = tk.Button(btn_frame,
                                     text="Refresh",
                                     command=lambda: self.load_table(self.isHide),
                                     activebackground="light gray",
                                     font=self.custom_font
                                     )
        self.refresh_btn.pack(side=tk.LEFT, padx=5)

        # Table for stored passwords
        self.tree = ttk.Treeview(self.root, columns=("Service", "Email", "Password"), show="headings")
        self.tree.heading("Service", text="Service")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Password", text="Password")

        self.tree.column("Service", width=180)
        self.tree.column("Email", width=180)
        self.tree.column("Password", width=180)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Copy
        self.tree.bind("<Double-1>", self.copy_password)
        self.tree.bind("<Control-c>", self.copy_password)

        # Shortcuts
        self.root.bind('<Control-a>', self.add_password_window)
        self.root.bind('<Control-x>', self.delete_password_window)
        self.root.bind('<Control-r>', self.load_table)

        # Initialize table
        self.load_table(self.isHide)

    def copy_password(self, event = None):
        # Get all the password as a json format
        loadpwd = self.pwdConfig.load_passwords()

        # Get all trees then use the service to get the pwd
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        service = values[0]
        password = loadpwd[service]["Password"]
        if password != "[Invalid Key]":
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard.")

    def load_table(self, hide: bool, event = None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        passwords = self.pwdConfig.load_passwords()
        for service, creds in passwords.items():
            self.tree.insert("", tk.END, values=(service, creds["Email"], creds["Password"] if not hide else "-"))

    def hs_load_table(self, event = None):
        self.isHide = not self.isHide

        self.hide_pwd_btn.config(text="Show Password" if self.isHide else "Hide Password")
        self.hide_pwd_btn.config(bg="aqua" if self.isHide else "orange")
        self.load_table(self.isHide)

    def delete_password_window(self, event = None):
        win = tk.Toplevel(self.root)
        win.title("Delete Password")
        win.focus_set()
        win.grab_set()
        win.resizable(False, False)

        DEL_PWD_WINDOW_WIDTH = WINDOW_WIDTH
        DEL_PWD_WINDOW_HEIGHT = WINDOW_HEIGHT
        DEL_PWD_X = (self.screen_width - DEL_PWD_WINDOW_WIDTH) // 2
        DEL_PWD_Y = (self.screen_height - DEL_PWD_WINDOW_HEIGHT) // 2
        win.geometry(f"{DEL_PWD_WINDOW_WIDTH}x{DEL_PWD_WINDOW_HEIGHT}+{DEL_PWD_X}+{DEL_PWD_Y}")

        # --- Setup top_tree columns to match root table ---
        top_tree = ttk.Treeview(win, columns=("Service", "Email", "Password"), show="headings")
        top_tree.heading("Service", text="Service")
        top_tree.heading("Email", text="Email")
        top_tree.heading("Password", text="Password")
        top_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Load data into top_tree (mirrors load_table but local) ---
        def load_top_tree():
            for row in top_tree.get_children():
                top_tree.delete(row)

            passwords = self.pwdConfig.load_passwords()
            for service, creds in passwords.items():
                top_tree.insert("", tk.END, values=(service, creds["Email"], creds["Password"]))

        load_top_tree()

        # --- Delete logic ---
        def on_return(e):
            selected = top_tree.selection()
            if not selected:
                messagebox.showinfo("Error!")
                tk.Label(text="Select a row!")
                return

            item_values = top_tree.item(selected[0], "values")
            service_name = item_values[0]

            # --- Confirmation box ---
            confirm = tk.Toplevel(win)
            confirm.title("Confirmation")
            confirm.resizable(False, False)
            confirm.grab_set()
            confirm.focus_set()

            # Center over the delete window
            confirm.geometry(f"250x100+{win.winfo_x() + 50}+{win.winfo_y() + 50}")

            tk.Label(confirm, text=f"Delete '{service_name}'?").grid(
                row=0, column=0, columnspan=2, padx=10, pady=15, sticky="w"
            )

            def on_no():
                confirm.destroy()

            def on_yes():
                self.func.delete_pwd(e)
                load_top_tree()
                self.load_table(self.isHide)
                confirm.destroy()

            tk.Button(confirm, text="No", width=8, command=on_no, bg="red", activebackground="crimson", font=self.custom_font).grid(
                row=1, column=0, padx=10, pady=5, sticky="w"
            )
            tk.Button(confirm, text="Yes", width=8, command=on_yes, bg="lime", activebackground="green", font=self.custom_font).grid(
                row=1, column=1, padx=5, pady=5, sticky="w"
            )

            confirm.bind("<Return>", lambda e: on_yes())
            confirm.bind("<Escape>", lambda e: on_no())

        def on_select(e):
            top_tree.unbind("<Return>")
            top_tree.bind("<Return>", on_return)

        top_tree.bind("<<TreeviewSelect>>", on_select)

        def save(event = None):
            win.destroy()
            self.load_table(self.isHide)

        tk.Button(win, text="Save", command=save, font=self.custom_font).pack(pady=10)

        # Shortcut
        win.bind('<Control-s>', save)
        win.bind('<Escape>', lambda e: win.destroy())

    def add_password_window(self, event = None):
        win = tk.Toplevel(self.root)
        win.title("Add Password")
        win.resizable(False, False)
        win.focus_set()
        win.grab_set()
        self.pwdState = False

        ADD_PWD_WINDOW_WIDTH = 300
        ADD_PWD_WINDOW_HEIGHT = 200
        ADD_PWD_X, ADD_PWD_Y = (self.screen_width - ADD_PWD_WINDOW_WIDTH) // 2, (self.screen_height - ADD_PWD_WINDOW_HEIGHT) // 2
        win.geometry(f"{ADD_PWD_WINDOW_WIDTH}x{ADD_PWD_WINDOW_HEIGHT}+{ADD_PWD_X}+{ADD_PWD_Y}")

        tk.Label(win, text="Service:", font=self.custom_font).pack()
        service_entry = tk.Entry(win, font=self.custom_font)
        service_entry.pack()
        service_entry.focus_set()

        tk.Label(win, text="Email:", font=self.custom_font).pack()
        email_entry = tk.Entry(win, font=self.custom_font)
        email_entry.pack()

        def show_or_hide(event = None):
            self.pwdState = not self.pwdState
            password_entry.config(show="" if self.pwdState else "*")

        tk.Label(win, text="Password:", font=self.custom_font).pack()
        password_entry = tk.Entry(win, show="*", font=self.custom_font)
        password_entry.pack()

        # Generate Password
        def password_input(event = None):
            if password_entry:
                password_entry.delete(0, 'end')

            pwd = self.func.generate_pwd()
            password_entry.insert(0, pwd)

        tk.Button(win, text="Generate Password", command=password_input, font=self.custom_font).pack()

        # Enter Key
        def next_focus(event):
            event.widget.tk_focusNext().focus()
            return "break"

        for entry in (service_entry, email_entry, password_entry):
            entry.bind("<Return>", lambda e: next_focus(e))

        def save(event = None):
            service = service_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            if service and email and password:
                self.func.add_pwd(service, email, password)
                self.load_table(self.isHide)
                win.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")
                win.destroy()
                self.add_password_window()

        tk.Button(win, text="Save", command=save, font=self.custom_font).pack(pady=10)

        # Shortcut
        win.bind('<Control-s>', save)
        win.bind('<Escape>', lambda e: win.destroy())
        win.bind('<Control-g>', password_input) # Auto Generate Password
        win.bind('<Control-e>', show_or_hide)
