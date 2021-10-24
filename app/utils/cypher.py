from app.extensions import cipher_suite


def encode_password(password: str) -> str:
    return cipher_suite.encrypt(bytes(password, 'utf-8')).decode('utf-8')


def decode_password(password: str) -> str:
    return cipher_suite.decrypt(bytes(password, 'utf-8')).decode('utf-8')
