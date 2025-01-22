# dencer
The Dencer is a secure Python tool for file encryption and decryption using AES-GCM. It features strong password validation, file integrity verification, progress tracking, and secure file deletion to prevent data recovery, ensuring robust protection for your sensitive information.

Advanced Encryption Tool

Overview

The Advanced Encryption Tool is a Python-based utility for encrypting and decrypting files securely using AES-GCM (Advanced Encryption Standard - Galois/Counter Mode). It provides enhanced security features such as password strength validation, file integrity verification, and secure file deletion to prevent data recovery.

Features

1. AES-GCM Encryption

Encrypt files with AES-GCM, providing both confidentiality and integrity.
Uses 256-bit keys for strong encryption.

2. Password Strength Validation

Ensures the password meets security criteria:
Minimum 8 characters.
At least one uppercase letter, one lowercase letter, one digit, and one special character.

3. Progress Bars

Displays progress for large file encryption and decryption using tqdm.

4. File Integrity Verification

Verify if the decrypted file matches the original file to ensure accuracy.

5. Secure Deletion

Overwrite files with random data multiple times before deletion to prevent recovery.

6. Detailed Logging

Logs all operations for traceability and debugging.

Installation

Clone the repository:
git clone https://github.com/your-username/advanced-encryption-tool.git
cd advanced-encryption-tool

Install dependencies:

pip install -r requirements.txt

Dependencies include:

cryptography
tqdm

Usage

1. Encrypt a File

Encrypt a file with a strong password:
python encryptor.py --password YourSecurePassword --encrypt input.txt encrypted.bin

2. Decrypt a File

Decrypt a file using the same password:
python encryptor.py --password YourSecurePassword --decrypt encrypted.bin output.txt

3. Verify Decryption

Verify that the decrypted file matches the original file:
python encryptor.py --password YourSecurePassword --verify input.txt output.txt

4. Securely Delete a File

Overwrite a file multiple times before deleting it:
python encryptor.py --secure-delete input.txt

Security Notes

Ensure your password is strong and unique.
Keep sensitive files and passwords secure.
Combine this tool with best practices like secure backups and regular key rotations.

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

License

This project is licensed under me.

Contact

For questions or feedback, reach out at nijatmmmdv@gmail.com

