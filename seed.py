from datetime import datetime, timedelta
from backend.core.database import SessionLocal
from backend.models.user import User
from backend.models.product import Category
from backend.models.promo import PromoCode
from backend.core.security import hash_password


def init_db():
    db = SessionLocal()
    try:
        admin = db.query(User).filter_by(username="admin").first()
        if not admin:
            db.add(User(username="admin", email="admin@sportlife.ru",
                        password_hash=hash_password("123"),
                        full_name="Администратор", role="admin"))
        else:
            admin.password_hash = hash_password("123")

        for n in ["Обувь", "Футболки", "Шорты", "Куртки", "Аксессуары"]:
            if not db.query(Category).filter_by(name=n).first():
                db.add(Category(name=n))

        if not db.query(PromoCode).filter_by(code="SPORT10").first():
            db.add(PromoCode(code="SPORT10", discount_percent=10))
        if not db.query(PromoCode).filter_by(code="FIX500").first():
            db.add(PromoCode(code="FIX500", discount_fixed=500,
                             valid_until=datetime.utcnow() + timedelta(days=30)))

        db.commit()
    finally:
        db.close()