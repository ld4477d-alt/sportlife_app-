from backend.repositories import user_repo
from backend.core.security import create_token


def register(db, data):
    if user_repo.by_username(db, data.username):
        raise ValueError("Логин занят")
    u = user_repo.create(db, data.username, data.email, data.password, data.full_name)
    return create_token(u.id, u.role), u


def login(db, data):
    u = user_repo.auth(db, data.username, data.password)
    if not u:
        raise ValueError("Неверный логин или пароль")
    return create_token(u.id, u.role), u