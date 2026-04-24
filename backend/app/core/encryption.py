import os
from cryptography.fernet import Fernet
from app.core.config import settings

# In production, this should be in AWS Secrets Manager or Vault
# For now, we generate or use a secret key from environment
ENCRYPTION_KEY = os.getenv("FIELD_ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    # Fallback for dev only - Generate a key if missing
    ENCRYPTION_KEY = Fernet.generate_key().decode()

cipher_suite = Fernet(ENCRYPTION_KEY.encode())

def encrypt_field(value: str) -> str:
    """Encrypt a string value for storage."""
    if not value:
        return value
    return cipher_suite.encrypt(value.encode()).decode()

def decrypt_field(encrypted_value: str) -> str:
    """Decrypt a string value from storage."""
    if not encrypted_value:
        return encrypted_value
    try:
        return cipher_suite.decrypt(encrypted_value.encode()).decode()
    except Exception:
        # Fallback for non-encrypted legacy data
        return encrypted_value
