import flet as ft
from frontend.api import cart_api, orders_api
from frontend.api.client import api

def build(app):
    items_box = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    totals_box = ft.Column()
    promo_input = ft.TextField(label="Промокод", width=180)
    applied = {"code": None}

    def render_totals():
        try:
            t = cart_api.totals(applied["code"])
            totals_box.controls = [
                ft.Text(f'Сумма: {t["subtotal"]:.2f} ₽'),
                ft.Text(f'Скидка: -{t["discount"]:.2f} ₽', color=ft.Colors.RED),
                ft.Text(f'Итого: {t["total"]:.2f} ₽', weight=ft.FontWeight.BOLD, size=18),
                ft.Text(t.get("promo_message", ""), color=ft.Colors.GREEN),
            ]
        except Exception:
            totals_box.controls = [ft.Text("Ошибка загрузки", color=ft.Colors.RED)]
        app.page.update()

    def refresh():
        try:
            items = cart_api.get_cart()
            controls = []
            for i in items:
                img_url = "https://via.placeholder.com/50"
                if i.get("image_path"):
                    if i["image_path"].startswith("http"): img_url = i["image_path"]
                    elif i["image_path"].startswith("/uploads/"): img_url = f"http://localhost:8000{i['image_path']}"
                    else: img_url = i["image_path"]

                controls.append(ft.ListTile(
                    leading=ft.Image(src=img_url, width=50, height=50, fit=ft.BoxFit.COVER),
                    title=ft.Text(f'{i["product_name"]} (Размер: {i.get("size", "-")})'),
                    subtitle=ft.Text(f'{i["quantity"]} шт. × {i["product_price"]:.2f} ₽'),
                    trailing=ft.IconButton(ft.Icons.DELETE, on_click=lambda e, iid=i["id"]: (cart_api.remove_item(iid), refresh())),
                ))
            items_box.controls = controls
            render_totals()
        except Exception as e:
            app.error(f"Ошибка: {e}")

    addr = ft.TextField(label="Адрес")
    deliv = ft.Dropdown(label="Доставка", value="Курьер", options=[ft.dropdown.Option("Курьер"), ft.dropdown.Option("Самовывоз")])
    pay_dd = ft.Dropdown(label="Оплата", value="Картой", options=[ft.dropdown.Option("Картой"), ft.dropdown.Option("Наличными")])

    def do_checkout(e):
        try:
            orders_api.checkout(addr.value or "-", deliv.value, pay_dd.value, applied["code"])
            app.ok("Заказ оформлен")
            app.go("orders")
        except Exception as ex:
            # Теперь мы покажем текст ошибки прямо на экране
            app.error(f"ОШИБКА СЕРВЕРА: {ex}")

    def apply_promo(e):
        applied["code"] = promo_input.value.strip().upper()
        render_totals()

    refresh()

    is_guest = api.user.get("role") == "guest" if api.user else True

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Каталог"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART, label="Корзина"),
            ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG, label="Заказы", visible=not is_guest),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Профиль"),
        ],
        selected_index=1,
        on_change=lambda e: [
            lambda _: app.go("catalog"),
            lambda _: None,
            lambda _: app.go("orders"),
            lambda _: app.go("profile")
        ][e.control.selected_index](e)
    )

    return ft.Column(
        controls=[
            ft.Text("Корзина", size=20, weight=ft.FontWeight.BOLD),
            items_box,
            ft.Row([promo_input, ft.Button("Применить", on_click=apply_promo)]),
            totals_box,
            addr,
            ft.Row([deliv, pay_dd]),
            ft.Button("Оформить", on_click=do_checkout),
            nav_bar
        ],
        expand=True,
        spacing=10
    )