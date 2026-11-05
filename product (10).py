from typing import Optional
from pydantic import BaseModel


class ProductIn(BaseModel):
    name: str
    description: str = ""
    price: float
    type: str = "Одежда"
    category: str = "Для новичков"
    brand: str = ""
    size: str = ""
    color: str = ""
    material: str = ""
    availability: bool = True
    image_path: str = ""
    category_id: Optional[int] = None


class ProductOut(ProductIn):
    id: int
    class Config:
        from_attributes = True


class CatalogFilter(BaseModel):
    query: str = ""
    type: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    size: Optional[str] = None
    color: Optional[str] = None
    availability: Optional[bool] = None
    sort_by: str = "name"
    limit: int = 50
    offset: int = 0