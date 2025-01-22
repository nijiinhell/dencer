#Written by https://www.linkedin.com/in/nijat-mammadov-cyber/

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from os import urandom
import argparse
import base64
import logging
from tqdm import tqdm
import os

class AdvancedEncryptionTool:
    def __init__(self, password=None):
        """Initialize the encryption tool with a password for key derivation."""
        self.password = password.encode() if password else None
        self.backend = default_backend()

        # Set up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def _derive_key(self, salt):
        """Derive a key using PBKDF2-HMAC with the provided password and salt."""
        if not self.password:
            raise ValueError("Password is required for key derivation.")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(self.password)

    def validate_password(self):
        """Validate the password for strength."""
        if not self.password:
            return
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in self.password.decode()):
            raise ValueError("Password must contain at least one digit.")
        if not any(char.isupper() for char in self.password.decode()):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in self.password.decode()):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(char in '!@#$%^&*()-_=+[]{};:,.<>?' for char in self.password.decode()):
            raise ValueError("Password must contain at least one special character.")

    def encrypt_file(self, input_file, output_file, secure_delete=False):
        """Encrypt a file using AES-GCM for advanced encryption."""
        salt = urandom(16)
        iv = urandom(12)  # 96-bit nonce for AES-GCM
        key = self._derive_key(salt)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        try:
            file_size = os.path.getsize(input_file)
            with open(input_file, "rb") as f:
                plaintext = f.read()

            with tqdm(total=file_size, desc="Encrypting", unit="B", unit_scale=True) as pbar:
                ciphertext = encryptor.update(plaintext) + encryptor.finalize()
                pbar.update(file_size)

            with open(output_file, "wb") as f:
                f.write(salt + iv + encryptor.tag + ciphertext)

            logging.info(f"File '{input_file}' encrypted successfully to '{output_file}'.")

            if secure_delete:
                self.secure_delete_file(input_file)
        except FileNotFoundError:
            logging.error(f"Error: File '{input_file}' not found.")

    def decrypt_file(self, input_file, output_file):
        """Decrypt a file encrypted with AES-GCM."""
        try:
            file_size = os.path.getsize(input_file)
            with open(input_file, "rb") as f:
                data = f.read()

            salt = data[:16]
            iv = data[16:28]
            tag = data[28:44]
            ciphertext = data[44:]

            key = self._derive_key(salt)
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=self.backend)
            decryptor = cipher.decryptor()

            with tqdm(total=file_size, desc="Decrypting", unit="B", unit_scale=True) as pbar:
                plaintext = decryptor.update(ciphertext) + decryptor.finalize()
                pbar.update(file_size)

            with open(output_file, "wb") as f:
                f.write(plaintext)

            logging.info(f"File '{input_file}' decrypted successfully to '{output_file}'.")
        except FileNotFoundError:
            logging.error(f"Error: File '{input_file}' not found.")
        except Exception as e:
            logging.error(f"Error during decryption: {e}")

    def secure_delete_file(self, file_path):
        """Securely overwrite and delete a file."""
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, "ba+") as f:
                for _ in tqdm(range(3), desc="Overwriting", unit="pass"):
                    f.seek(0)
                    f.write(urandom(file_size))
            os.remove(file_path)
            logging.info(f"File '{file_path}' securely deleted.")
        except FileNotFoundError:
            logging.error(f"Error: File '{file_path}' not found for secure deletion.")
        except Exception as e:
            logging.error(f"Error during secure deletion: {e}")

    def verify_decryption(self, original_file, decrypted_file):
        """Verify that the decrypted file matches the original file."""
        try:
            with open(original_file, "rb") as f1, open(decrypted_file, "rb") as f2:
                original_data = f1.read()
                decrypted_data = f2.read()

            if original_data == decrypted_data:
                logging.info("Verification successful: Decrypted file matches the original file.")
            else:
                logging.warning("Verification failed: Decrypted file does not match the original file.")
        except FileNotFoundError as e:
            logging.error(f"Error during verification: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Encryption/Decryption Tool with AES-GCM")
    parser.add_argument("--password", help="Password for encryption/decryption.")
    parser.add_argument("--encrypt", nargs=2, metavar=("INPUT_FILE", "OUTPUT_FILE"), help="Encrypt a file.")
    parser.add_argument("--decrypt", nargs=2, metavar=("INPUT_FILE", "OUTPUT_FILE"), help="Decrypt a file.")
    parser.add_argument("--verify", nargs=2, metavar=("ORIGINAL_FILE", "DECRYPTED_FILE"), help="Verify decrypted file matches original file.")
    parser.add_argument("--secure-delete", metavar="FILE_PATH", help="Securely delete a file.")
    args = parser.parse_args()

    tool = AdvancedEncryptionTool(args.password)

    if args.password:
        try:
            tool.validate_password()
        except ValueError as e:
            logging.error(f"Password validation failed: {e}")
            exit(1)

    if args.encrypt:
        input_file, output_file = args.encrypt
        tool.encrypt_file(input_file, output_file, secure_delete=False)

    if args.decrypt:
        input_file, output_file = args.decrypt
        tool.decrypt_file(input_file, output_file)

    if args.verify:
        original_file, decrypted_file = args.verify
        tool.verify_decryption(original_file, decrypted_file)

    if args.secure_delete:
        tool.secure_delete_file(args.secure_delete)
