from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services import favorite_service
from backend.core.dependencies import current_user

router = APIRouter(prefix="/api/favorites", tags=["favorites"])

@router.get("")
def list_favs(db: Session = Depends(get_db), u=Depends(current_user)):
    favs = favorite_service.list_favs(db, u.id)
    return [{"product_id": f.product_id} for f in favs]

@router.post("/{pid}")
def toggle(pid: int, db: Session = Depends(get_db), u=Depends(current_user)):
    added = favorite_service.toggle(db, u.id, pid)
    return {"added": added}