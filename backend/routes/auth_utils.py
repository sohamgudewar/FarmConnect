from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    password = password.encode("utf-8")[:72]  # ✅ FIX (bytes safe)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    plain_password = plain_password.encode("utf-8")[:72]  # ✅ same fix
    return pwd_context.verify(plain_password, hashed_password)
