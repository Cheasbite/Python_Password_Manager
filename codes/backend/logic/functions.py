import uuid

from .pwdConf import PasswordsConfig


class Functionality:
    """Thin wrapper around PasswordsConfig with no Tk/GUI dependencies,
    so the frontend can call these without coupling logic to widgets."""

    def __init__(self):
        self.pwdConfig = PasswordsConfig()

    def list_pwd(self):
        """Return {id: {"service", "email", "password"}} for every entry."""
        return self.pwdConfig.load_passwords()

    def add_pwd(self, service, email, password, entry_id=None):
        passwords = self.pwdConfig.load_passwords()
        entry_id = entry_id or str(uuid.uuid7())
        passwords[entry_id] = {
            "service": service,
            "email": email,
            "password": password,
        }
        self.pwdConfig.save_passwords(passwords)
        return entry_id

    def edit_pwd(self, entry_id, service=None, email=None, password=None):
        return self.pwdConfig.edit_passwords(entry_id, service, email, password)

    def delete_pwd(self, entry_id):
        self.pwdConfig.del_passwords(entry_id)

    def delete_many(self, entry_ids):
        for entry_id in entry_ids:
            self.pwdConfig.del_passwords(entry_id)

