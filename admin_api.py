from .client import api

def all_orders():
    return api.get("/api/admin/orders").json()

def set_status(oid, status):
    return api.put(f"/api/admin/orders/{oid}/status", json={"status": status}).json()

def promos():
    return api.get("/api/admin/promos").json()

def add_promo(data):
    return api.post("/api/admin/promos", json=data).json()

def del_promo(pid):
    return api.delete(f"/api/admin/promos/{pid}").json()

def users():
    return api.get("/api/admin/users").json()

def set_user_role(uid, role):
    return api.put(f"/api/admin/users/{uid}/role", params={"role": role}).json()

def delete_user(uid):
    return api.delete(f"/api/admin/users/{uid}").json()
