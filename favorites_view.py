import flet as ft
from frontend.api.client import api
from frontend.api import products_api
from frontend.config import BASE_URL

def build(app):
    try:
        favs = api.get("/api/favorites").json() if api.token else []
    except:
        favs = []
        
    rows = []
    for f in favs:
        p = products_api.get_product(f["product_id"])
        if p:
            img_url = "https://via.placeholder.com/50"
            if p.get("image_path"):
                if p["image_path"].startswith("http"): img_url = p["image_path"]
                elif p["image_path"].startswith("/uploads/"): img_url = f"{BASE_URL}{p['image_path']}"

            rows.append(ft.ListTile(
                leading=ft.Image(src=img_url, width=50, height=50, fit=ft.BoxFit.COVER),
                title=ft.Text(p["name"]),
                subtitle=ft.Text(f'{p["price"]:.2f} ₽'),
                on_click=lambda e, pid=p["id"]: app.go("product", product_id=pid),
            ))
            
    if not rows:
        rows = [ft.Text("В избранном пусто", size=16)]

    # Оборачиваем в Container, чтобы избежать ошибки с padding
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: app.go("catalog")),
                ft.Text("Избранное", size=20, weight=ft.FontWeight.BOLD),
            ]),
            ft.Column(rows, scroll=ft.ScrollMode.AUTO, expand=True),
        ], expand=True, spacing=10),
        padding=10,
        expand=True
    )