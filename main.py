from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.core.database import engine, Base
from backend.core.config import UPLOAD_DIR
from backend.models import *  # noqa
from backend.routers import auth, products, cart, orders, favorites, admin
from backend.seed import init_db

app = FastAPI(title="Sport Life API")


@app.on_event("startup")
def _startup():
    Base.metadata.create_all(bind=engine)
    init_db()


app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(favorites.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Sport Life API"}