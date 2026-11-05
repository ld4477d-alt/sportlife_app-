import flet as ft
from frontend.api import products_api
from frontend.api.client import api
from frontend.config import BASE_URL


def build(app):
    search = ft.TextField(hint_text="Поиск...", width=200)
    
    type_dd = ft.Dropdown(
        label="Тип", width=130, value="",
        options=[ft.dropdown.Option(""), ft.dropdown.Option("Одежда"), ft.dropdown.Option("Обувь")],
    )
    level_dd = ft.Dropdown(
        label="Уровень", width=150, value="",
        options=[ft.dropdown.Option(""), ft.dropdown.Option("Для новичков"), ft.dropdown.Option("Для профи")],
    )
    brand_dd = ft.Dropdown(
        label="Бренд", width=130, value="",
        options=[ft.dropdown.Option(""), ft.dropdown.Option("Nike"), ft.dropdown.Option("Puma"), ft.dropdown.Option("Adidas")],
    )

    grid = ft.GridView(expand=True, runs_count=2, max_extent=180, spacing=8)
    
    # Метка для вывода "Ничего не найдено"
    empty_label = ft.Text("Ничего не найдено по этим фильтрам", color=ft.Colors.RED, size=16, visible=False)

    favs_ids = []
    if api.token:
        try:
            favs = api.get("/api/favorites").json()
            favs_ids = [f["product_id"] for f in favs]
        except:
            pass

    def toggle_fav(pid, btn):
        if not api.token:
            app.error("Войдите, чтобы добавлять в избранное")
            return
        try:
            res = api.post(f"/api/favorites/{pid}").json()
            if res.get("added"):
                btn.icon = ft.Icons.FAVORITE
                btn.icon_color = ft.Colors.RED
                app.ok("Добавлено в избранное ❤️")
            else:
                btn.icon = ft.Icons.FAVORITE_BORDER
                btn.icon_color = ft.Colors.GREY
                app.ok("Удалено из избранного 💔")
            app.page.update()
        except Exception as ex:
            app.error(str(ex))

    def card(p):
        def open_(e):
            app.go("product", product_id=p["id"])
            
        img_url = "https://via.placeholder.com/150"
        if p.get("image_path"):
            if p["image_path"].startswith("http"):
                img_url = p["image_path"]
            elif p["image_path"].startswith("/uploads/"):
                img_url = f"{BASE_URL}{p['image_path']}"
            else:
                img_url = p["image_path"]

        is_fav = p["id"] in favs_ids
        fav_icon = ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER
        fav_color = ft.Colors.RED if is_fav else ft.Colors.GREY

        fav_btn = ft.IconButton(
            icon=fav_icon, 
            icon_color=fav_color, 
            icon_size=20,
            on_click=lambda e: toggle_fav(p["id"], e.control)
        )

        return ft.Card(content=ft.Container(
            content=ft.Column([
                ft.Stack([
                    ft.Image(src=img_url, width=150, height=150, fit=ft.BoxFit.COVER),
                    ft.Container(content=fav_btn, alignment=ft.Alignment.TOP_RIGHT, padding=0)
                ]),
                ft.Text(p["name"], weight=ft.FontWeight.BOLD, max_lines=1),
                ft.Text(f'{p.get("brand", "")} | {p.get("category", "")}', size=12, color=ft.Colors.GREY),
                ft.Text(f'{p["price"]:.2f} ₽', color=ft.Colors.BLUE_600),
            ]),
            padding=8, on_click=open_, width=170))

    def refresh(e=None):
        # ПРИНУДИТЕЛЬНО БЕРЕМ ЗНАЧЕНИЯ ИЗ САМИХ КОМПОНЕНТОВ
        t_val = type_dd.value if type_dd.value else ""
        c_val = level_dd.value if level_dd.value else ""
        b_val = brand_dd.value if brand_dd.value else ""
        q_val = search.value if search.value else ""

        print(f"ОТПРАВЛЯЕМ НА СЕРВЕР: Тип='{t_val}', Уровень='{c_val}', Бренд='{b_val}', Поиск='{q_val}'")

        data = products_api.list_products(
            q=q_val, 
            type=t_val,
            category=c_val, 
            brand=b_val
        )
        
        grid.controls.clear()
        if not data:
            empty_label.visible = True
        else:
            empty_label.visible = False
            grid.controls = [card(p) for p in data]
            
        app.page.update()

    btn_apply = ft.Button("🔍 Применить", on_click=refresh)
    search.on_change = refresh

    refresh()

    is_guest = api.user.get("role") == "guest" if api.user else True

    top_bar = ft.Row([
        ft.Text("Каталог", size=20, weight=ft.FontWeight.BOLD),
        ft.IconButton(ft.Icons.FAVORITE, on_click=lambda e: app.go("favorites"), tooltip="Мое избранное"),
        ft.IconButton(ft.Icons.RECEIPT_LONG, visible=not is_guest, on_click=lambda e: app.go("orders")),
        ft.IconButton(ft.Icons.PERSON, on_click=lambda e: app.go("profile")),
    ])

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Каталог"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART, label="Корзина", visible=not is_guest),
            ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG, label="Заказы", visible=not is_guest),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Профиль"),
        ],
        selected_index=0,
        on_change=lambda e: [
            lambda _: None, 
            lambda _: app.go("cart"), 
            lambda _: app.go("orders"), 
            lambda _: app.go("profile")
        ][e.control.selected_index](e)
    )

    return ft.Column([
        top_bar,
        ft.Row([search]),
        ft.Row([type_dd, level_dd, brand_dd, btn_apply]),
        empty_label,
        grid,
        nav_bar
    ], expand=True, spacing=10)