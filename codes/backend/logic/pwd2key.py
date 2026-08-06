from ...config import SALT_BIN, PBKDF2HMAC_iterations, PBKDF2HMAC_Lenght, osUrandomSize
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64
import json

class pwd2key:
    def __init__(self):
        self.eneteredKey = None

    def generate_salt(self):
        salt = os.urandom(osUrandomSize)
        self._write_salt_file(salt, PBKDF2HMAC_iterations)
        return salt, PBKDF2HMAC_iterations

    def _write_salt_file(self, salt, iterations):
        payload = {
            "salt": base64.b64encode(salt).decode("ascii"),
            "iterations": iterations,
        }
        with open(SALT_BIN, "w") as f:
            json.dump(payload, f)

    def load_salt(self):
        if not os.path.exists(SALT_BIN):
            return self.generate_salt()

        with open(SALT_BIN, "rb") as f:
            raw = f.read()

            payload = json.loads(raw.decode("utf-8"))
            salt = base64.b64decode(payload["salt"])
            iterations = payload["iterations"]

        return salt, iterations

    def derive_key(self, master_password: str) -> Fernet:
        salt, iterations = self.load_salt()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=PBKDF2HMAC_Lenght,
            salt=salt,
            iterations=iterations,
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return Fernet(self.key)

