from sqlalchemy.orm import Session
from backend.models.cart import CartItem

def add(db: Session, uid, pid, qty=1, size=""):
    # Ищем товар с ТАКИМ ЖЕ размером. Если есть — плюсуем, если нет — создаем новую строку
    it = db.query(CartItem).filter_by(user_id=uid, product_id=pid, size=size).first()
    if it:
        it.quantity += qty
    else:
        db.add(CartItem(user_id=uid, product_id=pid, quantity=qty, size=size))
    db.commit()

def items(db: Session, uid):
    return db.query(CartItem).filter_by(user_id=uid).all()

def total(db: Session, uid):
    return sum(i.product.price * i.quantity for i in items(db, uid) if i.product)

def remove(db: Session, iid):
    it = db.query(CartItem).get(iid)
    if it: db.delete(it); db.commit()

def clear(db: Session, uid):
    db.query(CartItem).filter_by(user_id=uid).delete(); db.commit()