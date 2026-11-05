from sqlalchemy.orm import Session
from backend.models.user import User
from backend.core.security import hash_password, verify_password


def create(db: Session, username, email, password, full_name="", role="user"):
    u = User(username=username, email=email, password_hash=hash_password(password),
             full_name=full_name, role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def by_username(db: Session, username):
    return db.query(User).filter(User.username == username).first()


def auth(db: Session, username, password):
    u = by_username(db, username)
    return u if u and verify_password(password, u.password_hash) else None


def all_users(db: Session):
    return db.query(User).all()