import flet as ft
from frontend.api import orders_api
from frontend.config import BASE_URL

def build(app):
    try:
        data = orders_api.history()
    except Exception:
        data = []
    
    rows = []
    for o in data:
        items_controls = []
        for item in o.get("items", []):
            img_url = "https://via.placeholder.com/50"
            if item.get("image_path"):
                if item["image_path"].startswith("http"): img_url = item["image_path"]
                elif item["image_path"].startswith("/uploads/"): img_url = f"{BASE_URL}{item['image_path']}"
                else: img_url = item["image_path"]

            items_controls.append(ft.ListTile(
                leading=ft.Image(src=img_url, width=40, height=40, fit=ft.BoxFit.COVER),
                title=ft.Text(item["product_name"]),
                subtitle=ft.Text(f'Размер: {item["size"]} | {item["quantity"]} шт.'),
                dense=True
            ))

        rows.append(ft.Card(content=ft.Container(
            content=ft.Column([
                ft.Text(f'Заказ №{o["id"]}', weight=ft.FontWeight.BOLD, size=18),
                ft.Text(f'Сумма: {o["total"]:.2f} ₽', color=ft.Colors.BLUE_600, weight=ft.FontWeight.BOLD),
                ft.Text(f'Статус: {o["status"]}'),
                ft.Text(f'Доставка: {o["delivery_method"]} | Оплата: {o.get("payment_method", "-")}'),
                ft.Text(f'Адрес: {o["address"]}'),
                ft.Divider(),
                ft.Text("Товары в заказе:"),
                ft.Column(items_controls)
            ]),
            padding=15
        ), margin=10))
        
    if not rows:
        rows = [ft.Text("Заказов нет", size=16)]

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Каталог"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART, label="Корзина"),
            ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG, label="Заказы"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Профиль"),
        ],
        selected_index=2,
        on_change=lambda e: [
            lambda _: app.go("catalog"),
            lambda _: app.go("cart"),
            lambda _: None,
            lambda _: app.go("profile")
        ][e.control.selected_index](e)
    )

    return ft.Column([
        ft.Text("Мои заказы", size=20, weight=ft.FontWeight.BOLD),
        ft.Column(rows, scroll=ft.ScrollMode.AUTO, expand=True),
        nav_bar
    ], expand=True, spacing=10)