from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .security import decode_token
from backend.models.user import User

oauth = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def current_user(token: str = Depends(oauth), db: Session = Depends(get_db)) -> User:
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Невалидный токен")
    u = db.query(User).get(data["uid"])
    if not u:
        raise HTTPException(401, "Нет пользователя")
    return u


def admin_only(u: User = Depends(current_user)) -> User:
    if u.role != "admin":
        raise HTTPException(403, "Только админ")
    return u