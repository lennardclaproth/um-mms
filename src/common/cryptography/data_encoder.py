import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64


class Encoder():
    def __init__(self):
        self.generate_keys()
        self._private_key, self._public_key = self.load_keys()

    def generate_keys(self):
        if not os.path.exists("data/private_key.pem") or not os.path.exists("data/public_key.pem"):
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = private_key.public_key()

            # Ensure the directory exists
            os.makedirs("data", exist_ok=True)

            with open("data/private_key.pem", "wb") as private_key_file:
                private_key_file.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                )

            with open("data/public_key.pem", "wb") as public_key_file:
                public_key_file.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )

    def load_keys(self):
        with open("data/private_key.pem", "rb") as private_key_file:
            private_key = serialization.load_pem_private_key(
                private_key_file.read(), password=None, backend=default_backend())

        with open("data/public_key.pem", "rb") as public_key_file:
            public_key = serialization.load_pem_public_key(
                public_key_file.read(), backend=default_backend())

        return private_key, public_key

    def encrypt_data(self, data):
        # Ensure the data is bytes before encrypting
        if isinstance(data, str):
            data = data.encode()

        encrypted = self._public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted)

    def decrypt_data(self, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        decrypted = self._private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted

    def encrypt_file(self, file_path):
        symmetric_key = Fernet.generate_key()
        cipher_suite = Fernet(symmetric_key)

        with open(file_path, 'rb') as file:
            file_data = file.read()
        encrypted_file_data = cipher_suite.encrypt(file_data)

        encrypted_symmetric_key = self.encrypt_data(symmetric_key)

        encrypted_file_path = file_path + '.lcenc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_symmetric_key + b'\n' + encrypted_file_data)

        os.remove(file_path)

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            encrypted_symmetric_key = file.readline().strip()
            encrypted_file_data = file.read()

        symmetric_key = self.decrypt_data(encrypted_symmetric_key)

        cipher_suite = Fernet(symmetric_key)
        decrypted_file_data = cipher_suite.decrypt(encrypted_file_data)

        original_file_path, ext = os.path.splitext(file_path)
        if ext == '.lcenc':
            with open(original_file_path, 'wb') as file:
                file.write(decrypted_file_data)

        os.remove(file_path)

    def encrypt_json(self, json_string):
        if isinstance(json_string, str):
            json_string = json_string.encode('utf-8')

        symmetric_key = Fernet.generate_key()
        cipher_suite = Fernet(symmetric_key)

        encrypted_json_data = cipher_suite.encrypt(json_string)
        encrypted_symmetric_key = self.encrypt_data(symmetric_key)

        combined_encrypted_data = {
            "KEY": encrypted_symmetric_key.decode(),
            "DATA": base64.b64encode(encrypted_json_data).decode()
        }

        return json.dumps(combined_encrypted_data)

    def decrypt_json(self, encrypted_data):
        combined_encrypted_data = json.loads(encrypted_data)

        encrypted_symmetric_key = combined_encrypted_data["KEY"].encode(
            'utf-8')
        encrypted_json_data = base64.b64decode(combined_encrypted_data["DATA"])

        symmetric_key = self.decrypt_data(encrypted_symmetric_key)

        cipher_suite = Fernet(symmetric_key)
        decrypted_json_data = cipher_suite.decrypt(
            encrypted_json_data)

        return decrypted_json_data
