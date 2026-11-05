from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.core.database import get_db
from backend.schemas.product import ProductIn, ProductOut, CatalogFilter
from backend.services import catalog_service
from backend.core.dependencies import admin_only

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[ProductOut])
def list_products(q: str = "", category_id: Optional[int] = None,
                  min_price: Optional[float] = None, max_price: Optional[float] = None,
                  size: Optional[str] = None, color: Optional[str] = None,
                  availability: Optional[bool] = None, sort_by: str = "name",
                  limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    f = CatalogFilter(query=q, category_id=category_id, min_price=min_price,
                      max_price=max_price, size=size, color=color,
                      availability=availability, sort_by=sort_by,
                      limit=limit, offset=offset)
    return catalog_service.list_products(db, f)


@router.get("/{pid}", response_model=ProductOut)
def get_one(pid: int, db: Session = Depends(get_db)):
    p = catalog_service.get(db, pid)
    if not p:
        raise HTTPException(404, "Не найден")
    return p


@router.post("", response_model=ProductOut)
def create(data: ProductIn, db: Session = Depends(get_db), _=Depends(admin_only)):
    return catalog_service.create(db, data)


@router.put("/{pid}", response_model=ProductOut)
def update(pid: int, data: ProductIn, db: Session = Depends(get_db), _=Depends(admin_only)):
    p = catalog_service.update(db, pid, data)
    if not p:
        raise HTTPException(404, "Не найден")
    return p


@router.delete("/{pid}")
def delete(pid: int, db: Session = Depends(get_db), _=Depends(admin_only)):
    if not catalog_service.delete(db, pid):
        raise HTTPException(404, "Не найден")
    return {"ok": True}