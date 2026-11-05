from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Float, default=0.0)
    status = Column(String(30), default="Ожидает оплаты")
    address = Column(String(255), default="")
    delivery_method = Column(String(60), default="Курьер")
    payment_method = Column(String(60), default="Картой")
    promo_code = Column(String(40), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    items = relationship("OrderItem", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, default=0.0)
    size = Column(String(20), default="")

    # Связи
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")