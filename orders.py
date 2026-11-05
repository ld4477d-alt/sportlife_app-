from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.core.database import get_db
from backend.schemas.order import OrderIn, OrderOut, OrderItemOut
from backend.services import order_service
from backend.core.dependencies import current_user
from backend.models.order import Order

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("", response_model=OrderOut)
def checkout(data: OrderIn, db: Session = Depends(get_db), u=Depends(current_user)):
    try:
        # 1. Создаем заказ через сервис
        order = order_service.checkout(db, u.id, data)
        if not order:
            raise ValueError("Корзина пуста")
        
        # 2. Вручную собираем список товаров для ответа
        items_out = []
        for item in order.items:
            items_out.append(OrderItemOut(
                product_name=item.product.name if item.product else "Товар удален",
                quantity=item.quantity,
                price=item.price,
                size=item.size or "-",
                image_path=item.product.image_path if item.product else ""
            ))
            
        # 3. Возвращаем заказ со списком товаров
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
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("", response_model=List[OrderOut])
def my(db: Session = Depends(get_db), u=Depends(current_user)):
    # Тут делаем то же самое, только для всех заказов
    orders = db.query(Order).filter_by(user_id=u.id).order_by(Order.created_at.desc()).all()
    result = []
    for order in orders:
        items_out = []
        for item in order.items:
            items_out.append(OrderItemOut(
                product_name=item.product.name if item.product else "Товар удален",
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