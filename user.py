from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from backend.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(120), default="")
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)