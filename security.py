from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from .config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MIN

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(p: str) -> str:
    return pwd.hash(p)


def verify_password(p: str, h: str) -> bool:
    return pwd.verify(p, h)


def create_token(uid: int, role: str) -> str:
    payload = {"uid": uid, "role": role, "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MIN)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None