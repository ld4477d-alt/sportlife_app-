from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

from backend.core.database import get_db
from backend.core.config import UPLOAD_DIR
from backend.schemas.order import OrderOut, OrderStatusIn, OrderItemOut
from backend.schemas.promo import PromoCodeIn, PromoCodeOut
from backend.schemas.user import UserOut
from backend.repositories import promo_repo, user_repo
from backend.services import order_service
from backend.core.dependencies import admin_only
from backend.models.order import Order

router = APIRouter(prefix="/api/admin", tags=["admin"],
                   dependencies=[Depends(admin_only)])


@router.get("/orders", response_model=List[OrderOut])
def all_orders(db: Session = Depends(get_db)):
    orders = order_service.all_orders(db)
    result = []
    for order in orders:
        items_out = []
        for item in order.items:
            items_out.append(OrderItemOut(
                product_name=item.product.name if item.product else "Удален",
                quantity=item.quantity,
                price=item.price,
                size=item.size or "-",
                image_path=item.product.image_path if item.product else ""
            ))
            
        result.append(OrderOut(
            id=order.id,
            total=order.total,
            status=order.status,
            address=order.address,
            delivery_method=order.delivery_method,
            payment_method=order.payment_method,
            promo_code=order.promo_code,
            created_at=order.created_at,
            items=items_out
        ))
    return result


@router.put("/orders/{oid}/status", response_model=OrderOut)
def set_status(oid: int, data: OrderStatusIn, db: Session = Depends(get_db)):
    order = order_service.set_status(db, oid, data.status)
    
    items_out = []
    for item in order.items:
        items_out.append(OrderItemOut(
            product_name=item.product.name if item.product else "Удален",
            quantity=item.quantity,
            price=item.price,
            size=item.size or "-",
            image_path=item.product.image_path if item.product else ""
        ))
        
    return OrderOut(
        id=order.id,
        total=order.total,
        status=order.status,
        address=order.address,
        delivery_method=order.delivery_method,
        payment_method=order.payment_method,
        promo_code=order.promo_code,
        created_at=order.created_at,
        items=items_out
    )


@router.get("/promos", response_model=List[PromoCodeOut])
def promos(db: Session = Depends(get_db)):
    return promo_repo.all_promos(db)


@router.post("/promos", response_model=PromoCodeOut)
def add_promo(data: PromoCodeIn, db: Session = Depends(get_db)):
    return promo_repo.create(db, data)


@router.delete("/promos/{pid}")
def del_promo(pid: int, db: Session = Depends(get_db)):
    promo_repo.delete(db, pid)
    return {"ok": True}


@router.get("/users", response_model=List[UserOut])
def users(db: Session = Depends(get_db)):
    return user_repo.all_users(db)


# --- ЗАГРУЗКА ФОТО ---
@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, fname)
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"path": f"/uploads/{fname}"}