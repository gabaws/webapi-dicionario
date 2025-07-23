from cryptography.fernet import Fernet, InvalidToken
import os
import logging
from typing import Optional

logger = logging.getLogger("crypto")

def get_crypto_key() -> str:
    key = os.getenv("CRYPTO_KEY")
    if not key or len(key) < 32:
        logger.error("CRYPTO_KEY não definida ou muito curta. Defina uma chave segura de pelo menos 32 caracteres.")
        raise ValueError("CRYPTO_KEY não definida ou muito curta.")
    return key

try:
    KEY = get_crypto_key()
    cipher = Fernet(KEY.encode())
except Exception as e:
    logger.error(f"Erro ao inicializar Fernet: {e}")
    raise

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    try:
        return cipher.decrypt(token.encode()).decode()
    except InvalidToken:
        logger.error("Token de senha inválido para descriptografia.")
        raise ValueError("Token de senha inválido para descriptografia.")