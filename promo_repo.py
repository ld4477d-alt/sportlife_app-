from datetime import datetime
from sqlalchemy.orm import Session
from backend.models.promo import PromoCode


def create(db: Session, data):
    p = PromoCode(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def active(db: Session, code):
    p = db.query(PromoCode).filter(PromoCode.code == code, PromoCode.is_active == True).first()
    if p and p.valid_until and p.valid_until < datetime.utcnow():
        return None
    return p


def all_promos(db: Session):
    return db.query(PromoCode).all()


def delete(db: Session, pid):
    p = db.query(PromoCode).get(pid)
    if p:
        db.delete(p)
        db.commit()