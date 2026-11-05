from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.schemas.cart import CartItemIn, CartTotals
from backend.services import cart_service, discount_service
from backend.core.dependencies import current_user

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("")
def get_cart(db: Session = Depends(get_db), u=Depends(current_user)):
    items = cart_service.items(db, u.id)
    result = []
    for i in items:
        if i.product:
            result.append({
                "id": i.id,
                "product_id": i.product_id,
                "quantity": i.quantity,
                "size": i.size,
                "product_name": i.product.name,
                "product_price": i.product.price,
                "image_path": i.product.image_path,
            })
    return result

@router.post("")
def add(data: CartItemIn, db: Session = Depends(get_db), u=Depends(current_user)):
    cart_service.add(db, u.id, data)
    return {"ok": True}

@router.delete("/{iid}")
def remove(iid: int, db: Session = Depends(get_db), u=Depends(current_user)):
    cart_service.remove(db, iid)
    return {"ok": True}

@router.get("/totals", response_model=CartTotals)
def totals(promo: str | None = None, db: Session = Depends(get_db), u=Depends(current_user)):
    return discount_service.calc(db, u.id, promo)