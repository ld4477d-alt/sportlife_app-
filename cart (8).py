from pydantic import BaseModel
from typing import Optional

class CartItemIn(BaseModel):
    product_id: int
    quantity: int = 1
    size: str = "" # <--- ДОБАВИЛИ РАЗМЕР

class CartTotals(BaseModel):
    subtotal: float; discount: float; total: float
    promo_code: Optional[str] = None
    promo_message: str = ""