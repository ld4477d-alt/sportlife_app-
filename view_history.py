from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from backend.core.database import Base


class ViewHistory(Base):
    __tablename__ = "view_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow, index=True)