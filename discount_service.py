from backend.repositories import cart_repo, promo_repo
from backend.schemas.cart import CartTotals


def calc(db, uid, code=None):
    sub = cart_repo.total(db, uid)
    disc, msg, applied = 0.0, "", None
    if code:
        p = promo_repo.active(db, code.strip().upper())
        if not p:
            return CartTotals(subtotal=sub, discount=0, total=sub,
                              promo_message="Промокод не найден")
        if p.discount_percent > 0:
            disc = sub * p.discount_percent / 100
            msg = f"-{p.discount_percent:.0f}%"
        elif p.discount_fixed > 0:
            disc = min(p.discount_fixed, sub)
            msg = f"-{p.discount_fixed:.0f} руб."
        applied = p.code
    return CartTotals(subtotal=sub, discount=disc, total=max(0, sub - disc),
                      promo_code=applied,
                      promo_message=("Промокод применён: " + msg) if msg else "")