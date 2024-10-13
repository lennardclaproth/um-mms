from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import os
import base64


class PasswordManager:
    def __init__(self):
        self.algorithm = 'pbkdf2'

    def hash_password(self, password: str) -> str:
        if self.algorithm == 'pbkdf2':
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
        else:
            raise ValueError("Unsupported algorithm")

        key = kdf.derive(password)
        return base64.urlsafe_b64encode(salt + key).decode()

    def verify_password(self, stored_password: str, provided_password: str) -> bool:
        decoded_data = base64.urlsafe_b64decode(stored_password)
        salt = decoded_data[:16]
        stored_key = decoded_data[16:]

        if self.algorithm == 'pbkdf2':
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
        else:
            raise ValueError("Unsupported algorithm")

        try:
            kdf.verify(provided_password, stored_key)
            return True
        except Exception:
            return False
