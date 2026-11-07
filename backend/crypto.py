import hashlib
import re
import sys
import os

from cryptography.fernet import Fernet

sys.path.insert(0, os.path.dirname(__file__))
from config import FERNET_KEY

_fernet = Fernet(FERNET_KEY.encode())


def encrypt_email(email: str) -> str:
    return _fernet.encrypt(email.lower().encode()).decode()


def decrypt_email(token: str) -> str:
    return _fernet.decrypt(token.encode()).decode()


def hash_email(email: str) -> str:
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()


PASSWORD_RULES = [
    (r'.{8,}',          'Mínimo de 8 caracteres'),
    (r'[A-Z]',          'Pelo menos uma letra maiúscula'),
    (r'[a-z]',          'Pelo menos uma letra minúscula'),
    (r'\d',             'Pelo menos um número'),
    (r'[^A-Za-z0-9]',   'Pelo menos um caractere especial'),
]


def validate_password(password: str) -> list[str]:
    errors = []
    for pattern, message in PASSWORD_RULES:
        if not re.search(pattern, password):
            errors.append(message)
    return errors
