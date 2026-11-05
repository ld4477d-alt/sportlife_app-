import os

DATABASE_URL = os.getenv("DB_URL", "postgresql+psycopg2://postgres:123@localhost:5432/kucebo")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MIN = 60 * 24

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)