from backend.repositories import order_repo
from backend.services.discount_service import calc


def checkout(db, uid, data):
    t = calc(db, uid, data.promo_code)
    o = order_repo.create(db, uid, data, t.total, t.promo_code or "")
    if not o:
        raise ValueError("Корзина пуста")
    return o


def history(db, uid):
    return order_repo.for_user(db, uid)


def all_orders(db):
    return order_repo.all_orders(db)


def set_status(db, oid, status):
    return order_repo.set_status(db, oid, status)