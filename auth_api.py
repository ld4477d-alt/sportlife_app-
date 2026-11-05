from .client import api


def register(username, email, password, full_name=""):
    r = api.post("/api/auth/register", json={
        "username": username, "email": email, "password": password, "full_name": full_name})
    if r.status_code != 200:
        raise ValueError(r.json().get("detail", "Ошибка"))
    d = r.json()
    api.token = d["access_token"]
    api.user = d["user"]
    return d["user"]


def login(username, password):
    r = api.post("/api/auth/login", json={"username": username, "password": password})
    if r.status_code != 200:
        raise ValueError(r.json().get("detail", "Ошибка"))
    d = r.json()
    api.token = d["access_token"]
    api.user = d["user"]
    return d["user"]
