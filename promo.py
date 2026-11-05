from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from backend.core.database import Base


class PromoCode(Base):
    __tablename__ = "promo_codes"
    id = Column(Integer, primary_key=True)
    code = Column(String(40), unique=True, index=True, nullable=False)
    discount_percent = Column(Float, default=0.0)
    discount_fixed = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    valid_until = Column(DateTime, nullable=True)