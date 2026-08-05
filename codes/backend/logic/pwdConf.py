from ...config import DATA_FILE
import json
import os


class PasswordsConfig:
    """Reads/writes the plaintext working copy of the vault (DATA_FILE).

    This file only exists on disk *while the app is unlocked* -- main.py
    decrypts passwords.enc into it on startup and re-encrypts + deletes it
    on exit (see the flow described in readme.md).
    """

    def load_passwords(self):
        if not os.path.exists(DATA_FILE):
            return {}

        with open(DATA_FILE, "r") as file:
            content = file.read().strip()
            return json.loads(content) if content else {}

    def save_passwords(self, passwords):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as file:
            json.dump(passwords, file, indent=4, sort_keys=True)

    def del_passwords(self, entry_id):
        data = self.load_passwords()
        if entry_id in data:
            del data[entry_id]
            self.save_passwords(data)

    def edit_passwords(self, entry_id, service=None, email=None, password=None):
        """Update only the fields that were provided for an existing entry."""
        data = self.load_passwords()
        if entry_id not in data:
            raise KeyError(f"No password entry with id {entry_id!r}")

        if service is not None:
            data[entry_id]["service"] = service
        if email is not None:
            data[entry_id]["email"] = email
        if password is not None:
            data[entry_id]["password"] = password

        self.save_passwords(data)
        return data[entry_id]
