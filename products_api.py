from .client import api
import requests
import os
from frontend.config import BASE_URL


def list_products(**params):
    # Очищаем параметры от None и пустых строк, чтобы не ломать запрос
    clean_params = {}
    for k, v in params.items():
        if v is not None and v != "":
            clean_params[k] = v
            
    r = api.get("/api/products", params=clean_params)
    if r.status_code == 200:
        return r.json()
    return []


def get_product(pid):
    r = api.get(f"/api/products/{pid}")
    return r.json() if r.status_code == 200 else None


def create_product(data):
    r = api.post("/api/products", json=data)
    if r.status_code != 200:
        raise ValueError(r.json().get("detail", "Ошибка создания"))
    return r.json()


def update_product(pid, data):
    r = api.put(f"/api/products/{pid}", json=data)
    if r.status_code != 200:
        raise ValueError(r.json().get("detail", "Ошибка обновления"))
    return r.json()


def delete_product(pid):
    return api.delete(f"/api/products/{pid}").json()


def upload_image(file_path: str):
    clean_path = file_path.strip().strip('"').strip("'")
    if not os.path.exists(clean_path):
        raise ValueError(f"Файл не найден: {clean_path}")
    
    with open(clean_path, "rb") as f:
        files = {"file": (os.path.basename(clean_path), f, "image/jpeg")}
        r = requests.post(f"{BASE_URL}/api/admin/upload", files=files, headers=api._h())
    
    if r.status_code != 200:
        raise ValueError(f"Ошибка сервера: {r.text}")
    return r.json()["path"]