from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.schemas.user import UserRegister, UserLogin, UserOut
from backend.schemas.auth import Token
from backend.services import auth_service
from backend.core.dependencies import current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        tok, u = auth_service.register(db, data)
        return Token(access_token=tok, user=UserOut.model_validate(u))
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        tok, u = auth_service.login(db, data)
        return Token(access_token=tok, user=UserOut.model_validate(u))
    except ValueError as e:
        raise HTTPException(401, str(e))


@router.get("/me", response_model=UserOut)
def me(u=Depends(current_user)):
    return u