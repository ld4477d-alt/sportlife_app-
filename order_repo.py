from sqlalchemy.orm import Session
from backend.models.order import Order, OrderItem
from backend.models.cart import CartItem

def create(db: Session, uid, data, total, promo=""):
    cart = db.query(CartItem).filter_by(user_id=uid).all()
    if not cart:
        return None
    o = Order(
        user_id=uid, total=total, address=data.address,
        delivery_method=data.delivery_method, 
        payment_method=data.payment_method,
        promo_code=promo or ""
    )
    db.add(o)
    db.flush()
    for i in cart:
        db.add(OrderItem(
            order_id=o.id, product_id=i.product_id,
            quantity=i.quantity, price=i.product.price,
            size=i.size
        ))
    db.query(CartItem).filter_by(user_id=uid).delete()
    db.commit()
    db.refresh(o)
    return o

def for_user(db: Session, uid):
    # Возвращаем заказы вместе с их товарами и картинками
    orders = db.query(Order).filter_by(user_id=uid).order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        items_data = []
        for i in o.items:
            items_data.append({
                "product_name": i.product.name if i.product else "Товар удален",
                "quantity": i.quantity,
                "price": i.price,
                "size": i.size or "-",
                "image_path": i.product.image_path if i.product else ""
            })
        
        # Формируем ответ вручную
        result.append({
            "id": o.id,
            "total": o.total,
            "status": o.status,
            "address": o.address,
            "delivery_method": o.delivery_method,
            "payment_method": o.payment_method,
            "promo_code": o.promo_code,
            "created_at": o.created_at,
            "items": items_data
        })
    return result

def all_orders(db: Session):
    return db.query(Order).order_by(Order.created_at.desc()).all()

def set_status(db: Session, oid, status):
    o = db.query(Order).get(oid)
    if o:
        o.status = status
        db.commit()
    return o