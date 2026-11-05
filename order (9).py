from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class OrderItemOut(BaseModel):
    product_name: str
    quantity: int
    price: float
    size: str
    image_path: str

class OrderIn(BaseModel):
    address: str
    delivery_method: str = "Курьер"
    payment_method: str = "Картой"
    promo_code: Optional[str] = None

class OrderOut(BaseModel):
    id: int
    total: float
    status: str
    address: str
    delivery_method: str
    payment_method: str
    promo_code: str
    created_at: datetime
    items: List[OrderItemOut] # <--- ДОБАВИЛИ СПИСОК ТОВАРОВ
    class Config:
        from_attributes = True

class OrderStatusIn(BaseModel):
    status: str