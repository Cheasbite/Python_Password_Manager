import tkinter as tk
from tkinter import ttk, messagebox

from .. import config
from ..backend.logic.functions import Functionality
from ..backend.logic.genPwd import generatePwd

MASK = "\u2022" * 20  # bullet characters, easier on the eyes than "*"

class App:
    def __init__(self, root):
        self.root = root
        self.functions = Functionality()
        self.colors = config.theme()
        self.show_passwords = False
        self.entries = {}  # entry_id -> {"service", "email", "password"}

        self._build_ui()
        self.refresh_tree()

    # ------------------------------------------------------------------ #
    # UI construction
    # ------------------------------------------------------------------ #
    def _build_ui(self):
        root = self.root
        root.title("Password Manager")

        screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
        x = (screen_w - config.WINDOW_WIDTH) // 2
        y = (screen_h - config.WINDOW_HEIGHT) // 2
        root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}+{x}+{y}")
        root.minsize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        root.configure(bg=self.colors["bg"])

        self.style = ttk.Style()
        self._apply_treeview_style()

        # --- Treeview --------------------------------------------------
        tree_frame = tk.Frame(root, bg=self.colors["bg"])
        tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        self.tree_frame = tree_frame

        columns = ("service", "email", "password")
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show="headings", selectmode="browse",
        )
        for col, label, width in (
            ("service", "Service", 160),
            ("email", "Email", 220),
            ("password", "Password", 150),
        ):
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.tree.focus_set()

        self.tree.bind("<Double-1>", self._on_double_click)

        # --- Status bar (feedback for copy-to-clipboard, etc.) ---------
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            root, textvariable=self.status_var, anchor="w",
            bg=self.colors["bg"], fg=self.colors["fg"], font=(config.FONTS, config.FONTS_SIZE - 1),
        )
        self.status_label.pack(fill="x", padx=12)

        # --- Buttons -----------------------------------------------------
        btn_frame = tk.Frame(root, bg=self.colors["bg"])
        btn_frame.pack(fill="x", padx=10, pady=10)

        addVar = tk.StringVar(root, "Add")
        editVar = tk.StringVar(root, "Edit")
        delVar = tk.StringVar(root, "Delete")
        self.hideVar = tk.StringVar(root, "Hide" if self.show_passwords else "Show")
        settingVar = tk.StringVar(root, "Settings")

        button_specs = (
            (addVar, self.open_add_dialog),
            (editVar, self.open_edit_dialog),
            (delVar, self.open_delete_dialog),
            (self.hideVar, self.toggle_show_hide),
            (settingVar, self.open_settings_dialog),
        )
        self.buttons = []
        for var, cmd in button_specs:
            b = tk.Button(
                btn_frame, textvariable=var, command=cmd, width=12,
                **config.button_style(self.colors),
            )
            b.pack(side="left", padx=4, pady=(0, 20), expand=True)
            self.buttons.append(b)

        # Global shortcuts (work regardless of which widget has focus)
        root.bind("h", self.toggle_show_hide)
        root.bind("s", self.open_settings_dialog)
        root.bind("a", self.open_add_dialog)
        root.bind("e", self.open_edit_dialog)
        root.bind("d", self.open_delete_dialog)
        root.bind("q", lambda e: self.root.destroy())

        # Tree movement
        self.tree.bind("<j>", lambda e: self._move_selection(1))
        self.tree.bind("<Down>", lambda e: self._move_selection(1))
        self.tree.bind("<k>", lambda e: self._move_selection(-1))
        self.tree.bind("<Up>", lambda e: self._move_selection(-1))
        self.tree.bind("<y>", self._on_yank)

    def _apply_treeview_style(self):
        c = self.colors
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview",
            background=c["tree_bg"], fieldbackground=c["tree_bg"], foreground=c["tree_fg"],
            rowheight=24, font=(config.FONTS, config.FONTS_SIZE),
        )
        self.style.map(
            "Treeview",
            background=[("selected", c["tree_select_bg"])],
            foreground=[("selected", c["tree_select_fg"])],
        )
        self.style.configure(
            "Treeview.Heading",
            background=c["button_bg"], foreground=c["button_fg"],
            font=(config.FONTS, config.FONTS_SIZE, "bold"),
        )
        self.style.map(
            "Treeview.Heading",
            background=[("active", c["tree_heading_active_bg"])],
            foreground=[("active", c["tree_heading_active_fg"])],
        )

        # ttk widgets (Combobox, Scrollbar, ...) ignore plain tk bg=/fg=
        # kwargs entirely -- they only respond to ttk.Style. Without this,
        # the Service combobox in Add/Edit stays white regardless of theme.
        self.style.configure(
            "TCombobox",
            fieldbackground=c["entry_bg"], background=c["entry_bg"], foreground=c["entry_fg"],
            arrowcolor=c["fg"], selectbackground=c["entry_bg"], selectforeground=c["entry_fg"],
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", c["entry_bg"]), ("disabled", c["entry_bg"])],
            foreground=[("readonly", c["entry_fg"]), ("disabled", c["entry_fg"])],
            background=[("active", c["entry_bg"])],
        )
        # The dropdown list itself is a plain Tk Listbox under the hood and
        # isn't reachable via ttk.Style at all -- it's only themeable
        # through the option database.
        self.root.option_add("*TCombobox*Listbox.background", c["entry_bg"])
        self.root.option_add("*TCombobox*Listbox.foreground", c["entry_fg"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", c["tree_select_bg"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", c["tree_select_fg"])

    def apply_theme(self):
        self.colors = config.theme()
        c = self.colors

        self.root.configure(bg=c["bg"])
        self.tree_frame.configure(bg=c["bg"])
        self.status_label.configure(bg=c["bg"], fg=c["fg"])
        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=c["bg"])
        for b in self.buttons:
            b.configure(**config.button_style(c))
        self._apply_treeview_style()

    # ------------------------------------------------------------------ #
    # Data / tree refresh
    # ------------------------------------------------------------------ #
    def refresh_tree(self):
        self.entries = self.functions.list_pwd()
        self.tree.delete(*self.tree.get_children())

        for entry_id, data in sorted(self.entries.items(), key=lambda kv: kv[1].get("service", "").lower()):
            password_display = data.get("password", "") if self.show_passwords else MASK
            self.tree.insert(
                "", "end", iid=entry_id,
                values=(data.get("service", ""), data.get("email", ""), password_display),
            )

    def _flash_status(self, text, ms=1800):
        self.status_var.set(text)
        self.root.after(ms, lambda: self.status_var.set("") if self.status_var.get() == text else None)

    # ------------------------------------------------------------------ #
    # Tree Movement
    # ------------------------------------------------------------------ #
    def _move_selection(self, direction):
        children = self.tree.get_children()
        if not children:
            return "break"

        current = self.tree.selection()
        if not current:
            next_item = children[0]
        else:
            try:
                idx = children.index(current[0])
            except ValueError:
                idx = -1

            #next_item = children[(idx + direction) % len(children)]  # wraps at both ends
            # no loops on J and K
            next_item = children[max(0, min(len(children)-1, idx+direction))]

        self.tree.selection_set(next_item)
        self.tree.focus(next_item)
        self.tree.see(next_item)  # auto-scrolls if the row is off-screen
        return "break"

    # ------------------------------------------------------------------ #
    # Hide / Show
    # ------------------------------------------------------------------ #
    def toggle_show_hide(self, event=None):
        self.show_passwords = not self.show_passwords
        self.hideVar.set("Hide" if self.show_passwords else "Show")
        self.refresh_tree()

    # ------------------------------------------------------------------ #
    # On copy
    # ------------------------------------------------------------------ #
    def _on_double_click(self, event):
        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)  # "#1", "#2", "#3"
        if not row_id or row_id not in self.entries:
            return

        col_map = {"#1": "service", "#2": "email", "#3": "password"}
        field = col_map.get(col_id)
        if field is None:
            return

        value = self.entries[row_id].get(field, "")
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self._flash_status(f"Copied {field} to clipboard.")

    def _on_yank(self, event=None):
        id = self.tree.selection()

        value = self.entries[id[0]].get("password", "")
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self._flash_status(f"Copied password to clipboard.")

    # ------------------------------------------------------------------ #
    # Add / Edit (shared dialog)
    # ------------------------------------------------------------------ #
    def open_add_dialog(self, event=None):
        self._open_entry_dialog(mode="add")

    def open_edit_dialog(self, event=None):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Edit Password", "Select a row to edit first.")
            return
        entry_id = selection[0]
        self._open_entry_dialog(mode="edit", entry_id=entry_id)

    def _open_entry_dialog(self, mode, entry_id=None):
        c = self.colors
        is_edit = mode == "edit"
        existing = self.entries.get(entry_id, {}) if is_edit else {}

        win = tk.Toplevel(self.root)
        win.title("Edit Password" if is_edit else "Add Password")
        win.resizable(False, False)
        win.configure(bg=c["bg"])
        win.grab_set()

        w, h = 360, 260
        sx, sy = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sx - w) // 2}+{(sy - h) // 2}")

        font = (config.FONTS, config.FONTS_SIZE)
        pad = {"padx": 12, "pady": 6}

        # Service (free-entry combobox with a few common suggestions)
        tk.Label(win, text="Service:", bg=c["bg"], fg=c["fg"], font=font).grid(row=0, column=0, sticky="w", **pad)
        service_var = tk.StringVar(value=existing.get("service", ""))
        service_box = ttk.Combobox(win, textvariable=service_var, values=config.COMMON_SERVICES, font=font, width=24)
        service_box.grid(row=0, column=1, columnspan=2, sticky="w", **pad)

        # Email
        tk.Label(win, text="Email:", bg=c["bg"], fg=c["fg"], font=font).grid(row=1, column=0, sticky="w", **pad)
        email_var = tk.StringVar(value=existing.get("email", ""))
        email_entry = tk.Entry(win, textvariable=email_var, font=font, width=26,
                                bg=c["entry_bg"], fg=c["entry_fg"], insertbackground=c["entry_fg"])
        email_entry.grid(row=1, column=1, columnspan=2, sticky="w", **pad)

        # Password (+ show/hide toggle + generate button)
        tk.Label(win, text="Password:", bg=c["bg"], fg=c["fg"], font=font).grid(row=2, column=0, sticky="w", **pad)
        pwd_var = tk.StringVar(value=existing.get("password", ""))
        pwd_entry = tk.Entry(win, textvariable=pwd_var, font=font, width=18, show="*",
                              bg=c["entry_bg"], fg=c["entry_fg"], insertbackground=c["entry_fg"])
        pwd_entry.config(show="*")
        pwd_entry.grid(row=2, column=1, sticky="w", **pad)

        pwd_shown = {"state": False}

        def toggle_pwd_visible(event=None):
            pwd_shown["state"] = not pwd_shown["state"]
            pwd_entry.config(show="" if pwd_shown["state"] else "*")

        tk.Button(
            win, text="\U0001F441", width=2, command=toggle_pwd_visible,
            **config.button_style(c),
        ).grid(row=2, column=2, sticky="w")

        def generate(event=None):
            pwd_var.set(generatePwd())
            if pwd_shown["state"]:
                pwd_entry.config(show="")
            else:
                pwd_entry.config(show="*")

        tk.Button(
            win, text="Generate Password", command=generate, font=font,
            **config.button_style(c),
        ).grid(row=3, column=0, columnspan=3, pady=(10, 10), padx=(30, 0))

        error_var = tk.StringVar(value="")
        tk.Label(win, textvariable=error_var, fg=c["error_fg"], bg=c["bg"], font=font).grid(
            row=4, column=0, columnspan=3, sticky="w", padx=12
        )

        def cancel(event=None):
            win.destroy()

        def submit(event=None):
            service = service_var.get().strip()
            email = email_var.get().strip()
            password = pwd_var.get()

            if not service or not email or not password:
                error_var.set("All fields are required.")
                return

            if is_edit:
                self.functions.edit_pwd(entry_id, service=service, email=email, password=password)
            else:
                self.functions.add_pwd(service=service, email=email, password=password)

            win.destroy()
            self.refresh_tree()

        tk.Button(
            win, text="Submit", command=submit, width=12, font=font,
            **config.button_style(c),
        ).grid(row=5, column=0, columnspan=3, pady=10, padx=(30, 0))

        # Press Enter to go to next prompt
        def next_focus(event):
            event.widget.tk_focusNext().focus()
            return "break"

        for entry in (service_box, email_entry, pwd_entry):
            entry.bind("<Return>", lambda e: next_focus(e))

        win.bind("<Control-g>", generate)
        win.bind("<Control-s>", submit)
        win.bind("<Control-e>", toggle_pwd_visible)
        win.bind("<Escape>", cancel)  # Escape returns without saving, per readme
        service_box.focus()

    # ------------------------------------------------------------------ #
    # Delete
    # ------------------------------------------------------------------ #
    def open_delete_dialog(self, event=None):
        c = self.colors
        win = tk.Toplevel(self.root)
        win.title("Delete Passwords")
        win.configure(bg=c["bg"])
        win.grab_set()

        w, h = 480, 360
        sx, sy = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sx - w) // 2}+{(sy - h) // 2}")

        tk.Label(
            win, text="Select entries, then press Enter to mark them for deletion.\n"
                       "Nothing is deleted until you click Save.",
            bg=c["bg"], fg=c["fg"], font=(config.FONTS, config.FONTS_SIZE), justify="left",
        ).pack(fill="x", padx=10, pady=(10, 6))

        frame = tk.Frame(win, bg=c["bg"])
        frame.pack(fill="both", expand=True, padx=10)

        columns = ("service", "email")
        tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="extended")
        tree.heading("service", text="Service")
        tree.heading("email", text="Email")
        tree.column("service", width=200)
        tree.column("email", width=220)
        tree.focus_set()

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # Work off a fresh, independent clone of the current data so
        # cancelling this dialog never touches the real vault.
        clone = dict(self.entries)
        for entry_id, data in sorted(clone.items(), key=lambda kv: kv[1].get("service", "").lower()):
            tree.insert("", "end", iid=entry_id, values=(data.get("service", ""), data.get("email", "")))

        nav_anchor = [None]
        nav_cursor = [None]

        def _children():
            return tree.get_children()

        def _apply_single(row_id):
            nav_anchor[0] = row_id
            nav_cursor[0] = row_id
            tree.selection_set(row_id)
            tree.focus(row_id)
            tree.see(row_id)

        def _apply_range(anchor_id, cursor_id):
            children = _children()
            try:
                i1, i2 = children.index(anchor_id), children.index(cursor_id)
            except ValueError:
                return
            lo, hi = min(i1, i2), max(i1, i2)
            tree.selection_set(children[lo:hi + 1])
            tree.focus(cursor_id)
            tree.see(cursor_id)

        def move_single(direction, event=None):
            """j / k: move to the next/previous row, collapsing any
            existing multi-row selection down to just that one row.
            Nothing navigated yet -> jump to the first row, same as the
            main window's tree. Wraps at the ends."""
            children = _children()
            if not children:
                return "break"
            if nav_cursor[0] is None or nav_cursor[0] not in children:
                _apply_single(children[0])
                return "break"
            idx = children.index(nav_cursor[0])
            _apply_single(children[max(0, min(len(children)-1, idx+direction))])
            return "break"

        def extend_selection(direction, event=None):
            """J / K (shift): grow the selection by one row in that
            direction from wherever nav_cursor currently is, keeping
            nav_anchor fixed at whichever row the extension started from.
            Clamped at the ends rather than wrapping -- wrapping a
            multi-row selection around the list doesn't have an obvious
            meaning the way single-row wraparound does."""
            children = _children()
            if not children:
                return "break"
            if nav_cursor[0] is None or nav_cursor[0] not in children:
                _apply_single(children[0])  # same "first press" rule as move_single
                return "break"
            if nav_anchor[0] is None or nav_anchor[0] not in children:
                nav_anchor[0] = nav_cursor[0]
            idx = children.index(nav_cursor[0])
            next_idx = max(0, min(len(children) - 1, idx + direction))
            nav_cursor[0] = children[next_idx]
            _apply_range(nav_anchor[0], nav_cursor[0])
            return "break"

        def toggle_active_end(event=None):
            """o: jump the active end to the opposite side of whatever's
            currently selected (top -> bottom or bottom -> top), without
            changing which rows are selected -- so a following J/K then
            extends from that new side instead."""
            selected = tree.selection()
            if not selected:
                return "break"
            children = _children()
            indices = sorted(children.index(i) for i in selected if i in children)
            if not indices:
                return "break"
            top_id, bottom_id = children[indices[0]], children[indices[-1]]
            if nav_cursor[0] == bottom_id:
                nav_anchor[0], nav_cursor[0] = bottom_id, top_id
            else:
                nav_anchor[0], nav_cursor[0] = top_id, bottom_id
            tree.focus(nav_cursor[0])
            tree.see(nav_cursor[0])
            return "break"

        tree.bind("<j>", lambda e: move_single(1))
        tree.bind("<k>", lambda e: move_single(-1))
        tree.bind("<Down>", lambda e: move_single(1))
        tree.bind("<Up>", lambda e: move_single(-1))

        tree.bind("<J>", lambda e: extend_selection(1))
        tree.bind("<K>", lambda e: extend_selection(-1))
        tree.bind("<Shift-Down>", lambda e: extend_selection(1))
        tree.bind("<Shift-Up>", lambda e: extend_selection(-1))

        tree.bind("<o>", toggle_active_end)
        tree.bind("<O>", toggle_active_end)

        pending_delete_ids = set()
        status_var = tk.StringVar(value="")
        tk.Label(win, textvariable=status_var, bg=c["bg"], fg=c["error_fg"],
                 font=(config.FONTS, config.FONTS_SIZE)).pack(fill="x", padx=10)

        def mark_for_deletion(event=None):
            selected = tree.selection()
            if not selected:
                return
            names = ", ".join(clone[i].get("service", i) for i in selected)
            if not messagebox.askyesno(
                "Confirm", f"Mark {len(selected)} entrie(s) for deletion?\n({names})\n\n"
                           "They will only be removed for good once you click Save.", parent=win
            ):
                return
            for entry_id in selected:
                pending_delete_ids.add(entry_id)
                tree.delete(entry_id)
            status_var.set(f"{len(pending_delete_ids)} entrie(s) marked for deletion (not yet saved).")

        tree.bind("<d>", mark_for_deletion)

        tk.Button(
            win, text="Mark Selected for Deletion", command=mark_for_deletion,
            **config.button_style(c),
        ).pack(pady=(4, 0))

        btn_row = tk.Frame(win, bg=c["bg"])
        btn_row.pack(fill="x", padx=10, pady=10)

        def cancel(event=None):
            win.destroy()

        def save(event=None):
            if pending_delete_ids:
                self.functions.delete_many(pending_delete_ids)
                self.refresh_tree()
            win.destroy()

        tk.Button(btn_row, text="Cancel", command=cancel, **config.button_style(c)).pack(side="right", padx=4)
        tk.Button(btn_row, text="Save", command=save, **config.button_style(c)).pack(side="right", padx=4)

        win.bind("<Escape>", cancel)  # Escape returns back without saving
        win.bind("<Control-s>", save)

    # ------------------------------------------------------------------ #
    # Settings
    # ------------------------------------------------------------------ #
    def open_settings_dialog(self, event=None):
        c = self.colors
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.configure(bg=c["bg"])
        win.grab_set()
        win.resizable(False, False)

        w, h = 320, 300
        sx, sy = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        win.geometry(f"{w}x{h}+{(sx - w) // 2}+{(sy - h) // 2}")

        font = (config.FONTS, config.FONTS_SIZE)
        pad = {"padx": 12, "pady": 4}

        tk.Label(win, text="Theme:", bg=c["bg"], fg=c["fg"], font=font).grid(row=0, column=0, sticky="w", **pad)
        theme_var = tk.StringVar(value=config.THEME_NAME)
        theme_box = ttk.Combobox(
            win, textvariable=theme_var, values=list(config.THEMES.keys()),
            state="readonly", font=font, width=16,
        )
        theme_box.grid(row=0, column=1, columnspan=2, sticky="w", padx=12, pady=4)

        tk.Label(win, text="Password Generator", bg=c["bg"], fg=c["fg"], font=(config.FONTS, config.FONTS_SIZE, "bold")).grid(
            row=1, column=0, columnspan=3, sticky="w", padx=12, pady=(14, 2)
        )

        upper_var = tk.BooleanVar(value=config.USE_UPPER_CHAR)
        symbols_var = tk.BooleanVar(value=config.USE_SYMBOLS)
        digits_var = tk.BooleanVar(value=config.USE_DIGITS)

        tk.Checkbutton(win, text="Use uppercase letters", variable=upper_var, font=font,
                        **config.check_style(c)).grid(row=2, column=0, columnspan=3, sticky="w", padx=12)
        tk.Checkbutton(win, text="Use symbols", variable=symbols_var, font=font,
                        **config.check_style(c)).grid(row=3, column=0, columnspan=3, sticky="w", padx=12)
        tk.Checkbutton(win, text="Use digits", variable=digits_var, font=font,
                        **config.check_style(c)).grid(row=4, column=0, columnspan=3, sticky="w", padx=12)

        tk.Label(win, text="Length:", bg=c["bg"], fg=c["fg"], font=font).grid(row=5, column=0, sticky="w", **pad)
        length_var = tk.IntVar(value=config.GENERATED_LENGTH)
        tk.Spinbox(
            win, from_=0, to=128, textvariable=length_var, width=6, font=font,
            bg=c["entry_bg"], fg=c["entry_fg"], insertbackground=c["entry_fg"],
            buttonbackground=c["button_bg"], relief="flat",
        ).grid(row=5, column=1, sticky="w")

        error_var = tk.StringVar(value="")
        tk.Label(win, textvariable=error_var, fg=c["error_fg"], bg=c["bg"], font=font).grid(
            row=6, column=0, columnspan=3, sticky="w", padx=12
        )

        def cancel(event=None):
            win.destroy()

        def save(event=None):
            try:
                length = int(length_var.get())
            except (tk.TclError, ValueError):
                error_var.set("Length must be a whole number.")
                return
            if length < 0:
                error_var.set("Length cannot be negative.")
                return

            config.THEME_NAME = theme_var.get()
            config.USE_UPPER_CHAR = upper_var.get()
            config.USE_SYMBOLS = symbols_var.get()
            config.USE_DIGITS = digits_var.get()
            config.GENERATED_LENGTH = length
            config.save_user_settings()

            win.destroy()
            self.apply_theme()

        tk.Button(win, text="Save", command=save, font=font, **config.button_style(c)).grid(
            row=7, column=0, columnspan=3, pady=14
        )

        win.bind("<Control-s>", save)
        win.bind("<Escape>", cancel)  # Escape returns back without saving

