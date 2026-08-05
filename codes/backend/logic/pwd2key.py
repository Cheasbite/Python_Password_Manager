from ...config import SALT_BIN, PBKDF2HMAC_iterations, PBKDF2HMAC_Lenght
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64

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

