from passlib.hash import bcrypt_sha256


def hash_password(password: str) -> str:
    return bcrypt_sha256.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_sha256.verify(password, hashed_password)
