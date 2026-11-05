import flet as ft
from frontend.api import products_api, cart_api
from frontend.api.client import api


def build(app, product_id):
    p = products_api.get_product(product_id)
    if not p:
        return ft.Text("Товар не найден")

    is_guest = api.user.get("role") == "guest" if api.user else True

    # Получаем текущий список избранного, чтобы понять, добавлен ли уже товар
    favs = []
    if api.token:
        try:
            favs = api.get("/api/favorites").json()
        except:
            pass
    is_fav = any(f["product_id"] == p["id"] for f in favs)

    # Выбор размера
    sizes_list = [s.strip() for s in p.get("size", "").split(",") if s.strip()]
    size_dd = ft.Dropdown(
        label="Выберите размер", width=200,
        options=[ft.dropdown.Option(s) for s in sizes_list]
    )
    if sizes_list:
        size_dd.value = sizes_list[0]

    qty = ft.TextField(value="1", width=80, keyboard_type=ft.KeyboardType.NUMBER)

    def add_to_cart(e):
        if is_guest:
            app.error("Гостям нельзя добавлять товары в корзину.")
            return
        if not size_dd.value:
            app.error("Выберите размер!")
            return
        try:
            cart_api.add_to_cart(p["id"], int(qty.value), size_dd.value)
            app.ok(f"Добавлено (Размер: {size_dd.value})")
        except Exception as ex:
            app.error(str(ex))

    def toggle_fav(e):
        if is_guest:
            app.error("Гостям нельзя добавлять в избранное.")
            return
        try:
            res = api.post(f"/api/favorites/{p['id']}").json()
            if res.get("added"):
                app.ok("Добавлено в избранное ❤️")
            else:
                app.ok("Удалено из избранного 💔")
            app.go("product", product_id=p["id"]) # Перезагружаем экран
        except Exception as ex:
            app.error(str(ex))

    img_url = "https://via.placeholder.com/300"
    if p.get("image_path"):
        if p["image_path"].startswith("http"): img_url = p["image_path"]
        elif p["image_path"].startswith("/uploads/"): img_url = f"http://localhost:8000{p['image_path']}"

    # Кнопка сердечка (красная, если уже в избранном)
    fav_icon = ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER
    fav_color = ft.Colors.RED if is_fav else ft.Colors.GREY

    return ft.Column([
        ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: app.go("catalog")),
            ft.Text("Назад в каталог"),
            ft.Container(expand=True), # Раздвигаем элементы
            ft.IconButton(icon=fav_icon, icon_color=fav_color, on_click=toggle_fav, tooltip="В избранное")
        ]),
        ft.Image(src=img_url, height=300, fit=ft.BoxFit.CONTAIN),
        ft.Text(p["name"], size=20, weight=ft.FontWeight.BOLD),
        ft.Text(f'{p["price"]:.2f} ₽', size=16, color=ft.Colors.BLUE_600),
        ft.Text(p.get("description", "")),
        ft.Row([size_dd, qty]),
        ft.Button("В корзину", on_click=add_to_cart),
    ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)