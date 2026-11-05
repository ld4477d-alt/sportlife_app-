from .client import api

def checkout(address, delivery="Курьер", payment="Картой", promo=None):
    r = api.post("/api/orders", json={
        "address": address, 
        "delivery_method": delivery, 
        "payment_method": payment,
        "promo_code": promo
    })
    if r.status_code != 200:
        raise ValueError(r.json().get("detail", "Ошибка"))
    return r.json()

def history(): 
    return api.get("/api/orders").json() if api.token else []