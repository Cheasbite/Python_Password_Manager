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

