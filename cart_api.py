from .client import api

def get_cart(): return api.get("/api/cart").json() if api.token else []

def add_to_cart(pid, qty=1, size=""): 
    return api.post("/api/cart", json={"product_id": pid, "quantity": qty, "size": size}).json()

def remove_item(iid): return api.delete(f"/api/cart/{iid}").json()

def totals(promo=None):
    r = api.get("/api/cart/totals", params={"promo": promo} if promo else {})
    return r.json()