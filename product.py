from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, index=True)
    description = Column(Text, default="")
    price = Column(Float, default=0.0)
    type = Column(String(50), default="Одежда")
    category = Column(String(50), default="Для новичков")
    brand = Column(String(50), default="")
    size = Column(String(100), default="")
    color = Column(String(40), default="")
    material = Column(String(80), default="")
    availability = Column(Boolean, default=True)
    image_path = Column(String(255), default="")
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Связи
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")