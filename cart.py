from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.core.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    size = Column(String(20), default="")
    
    product = relationship("Product", back_populates="cart_items")