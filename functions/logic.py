import string
import secrets
import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
from .config import *

class pwd2key:
    def __init__(self):
        self.eneteredKey = None

    def generate_salt(self):
        salt = os.urandom(16)
        with open(SALT_BIN, "wb") as f:
            f.write(salt)
        return salt

    def load_salt(self):
        if not os.path.exists(SALT_BIN):
            return self.generate_salt()

        with open(SALT_BIN, "rb") as f:
            return f.read()

    def derive_key(self, master_password: str) -> Fernet:
        salt = self.load_salt()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=PBKDF2HMAC_Lenght,
            salt=salt,
            iterations=PBKDF2HMAC_iterations,
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return Fernet(self.key)

class Decryption:
    def decrypt(self, file, encFile, fernet):
        # Decrypt encrypted JSON → temp copy (your existing logic)
        with open(encFile, "rb") as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
        with open(file, "wb") as f:
            f.write(decrypted)

    def encrypt(self, file, encFile, fernet):
        # Encrypt temp copy → back to encrypted JSON, delete temp (your existing logic)
        with open(file, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(encFile, "wb") as f:
            f.write(encrypted)

class PasswordsConfig:
    def load_passwords(self):
        if not os.path.exists(DATA_FILE):
            return {}

        with open(DATA_FILE, "r") as file:
            return json.load(file)

    def save_passwords(self, passwords):
        with open(DATA_FILE, "w") as file:
            json.dump(passwords, file, indent=4, sort_keys=True)

    def del_passwords(self, passwords):
        data = self.load_passwords()
        del data[passwords]

        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4, sort_keys=True)

class Functionality:
    def __init__(self):
        self.pwdConfig = PasswordsConfig()
        self.use_upper_char = USE_UPPER_CHAR
        self.use_digits = USE_DIGITS
        self.use_symbols = USE_SYMBOLS
        self.pwdGeneratedLength = GENERATED_LENGTH

    def add_pwd(self, service, email, password):
        passwords = self.pwdConfig.load_passwords()
        passwords[service] = {"Email": email, "Password": password}
        self.pwdConfig.save_passwords(passwords)

    def delete_pwd(self, event):
        tree = event.widget
        selection = [tree.item(item)["values"] for item in tree.selection()][0]
        self.pwdConfig.del_passwords(selection[0])

    def generate_pwd(self):
        char = string.ascii_lowercase

        if self.use_digits:
            char += string.digits
        if self.use_symbols:
            char += string.punctuation
        if self.use_upper_char:
            char += string.ascii_uppercase

        password = ''.join(secrets.choice(char) for _ in range(self.pwdGeneratedLength))
        return password
