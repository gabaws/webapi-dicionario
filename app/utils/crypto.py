from cryptography.fernet import Fernet
import os

KEY = os.getenv("CRYPTO_KEY", Fernet.generate_key().decode())
cipher = Fernet(KEY.encode())

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()