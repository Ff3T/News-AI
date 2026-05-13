# security.py
from passlib.context import CryptContext

# 换用 pbkdf2_sha256，完全避开 bcrypt 长度问题
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # 无需预哈希/截断，直接支持任意长度

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)