from sqlalchemy.orm import Session
from backend.models.favorite import Favorite


def add(db: Session, uid, pid):
    if not db.query(Favorite).filter_by(user_id=uid, product_id=pid).first():
        db.add(Favorite(user_id=uid, product_id=pid))
        db.commit()


def remove(db: Session, uid, pid):
    f = db.query(Favorite).filter_by(user_id=uid, product_id=pid).first()
    if f:
        db.delete(f)
        db.commit()


def for_user(db: Session, uid):
    return db.query(Favorite).filter_by(user_id=uid).all()