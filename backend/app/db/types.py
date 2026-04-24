from sqlalchemy import TypeDecorator, String
from app.core.encryption import encrypt_field, decrypt_field

class EncryptedString(TypeDecorator):
    """
    Transparently encrypt/decrypt strings for database storage.
    """
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return encrypt_field(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return decrypt_field(value)
        return value
