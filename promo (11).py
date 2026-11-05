from pydantic import BaseModel


class PromoCodeIn(BaseModel):
    code: str
    discount_percent: float = 0.0
    discount_fixed: float = 0.0
    is_active: bool = True


class PromoCodeOut(PromoCodeIn):
    id: int

    class Config:
        from_attributes = True