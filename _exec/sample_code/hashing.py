import bcrypt

def encrypt(password: str) -> bytes:
    password_in_bytes: bytes = password.encode("utf-8")
    salt: bytes = bcrypt.gensalt()
    hashed_password: bytes = bcrypt.hashpw(password_in_bytes, salt)
    return hashed_password

print(encrypt("my_password"))