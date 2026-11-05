from sqlalchemy.orm import Session
from backend.models.view_history import ViewHistory


def log(db: Session, uid, pid):
    if not db.query(ViewHistory).filter_by(user_id=uid, product_id=pid).first():
        db.add(ViewHistory(user_id=uid, product_id=pid))
        db.commit()


def last(db: Session, uid, limit=10):
    return (db.query(ViewHistory)
            .filter_by(user_id=uid)
            .order_by(ViewHistory.viewed_at.desc())
            .limit(limit).all())