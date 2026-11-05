import flet as ft
from frontend.api import admin_api, products_api
from frontend.config import BASE_URL


def build(app):
    products_box = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    def open_product_form(product=None):
        is_edit = product is not None
        title = "Редактировать товар" if is_edit else "Новый товар"

        name = ft.TextField(label="Название", value=product["name"] if is_edit else "")
        desc = ft.TextField(label="Описание", multiline=True, value=product.get("description", "") if is_edit else "")
        price = ft.TextField(label="Цена", keyboard_type=ft.KeyboardType.NUMBER, value=str(product["price"]) if is_edit else "")
        
        type_dd = ft.Dropdown(
            label="Тип товара", value=product.get("type", "Одежда") if is_edit else "Одежда",
            options=[ft.dropdown.Option("Одежда"), ft.dropdown.Option("Обувь")]
        )
        level_dd = ft.Dropdown(
            label="Уровень", value=product.get("category", "Для новичков") if is_edit else "Для новичков",
            options=[ft.dropdown.Option("Для новичков"), ft.dropdown.Option("Для профи")]
        )
        brand_dd = ft.Dropdown(
            label="Бренд", value=product.get("brand", "") if is_edit else "",
            options=[ft.dropdown.Option("Nike"), ft.dropdown.Option("Puma"), ft.dropdown.Option("Adidas"), ft.dropdown.Option("Другой")]
        )

        sizes_container = ft.Column()

        def update_sizes(e=None):
            sizes_container.controls.clear()
            
            if type_dd.value == "Обувь":
                opts = [str(i) for i in range(36, 46)] 
            else:
                opts = ["XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL", "5XL"] 
            
            current_sizes = product.get("size", "").split(", ") if is_edit and product.get("size") else []
            cbs = [ft.Checkbox(label=s, value=(s in current_sizes)) for s in opts]
            sizes_container.data = cbs 
            
            rows = []
            for i in range(0, len(cbs), 4):
                rows.append(ft.Row(cbs[i:i+4]))
                
            sizes_container.controls = [*rows]
            app.page.update()

        type_dd.on_change = update_sizes

        btn_update = ft.TextButton("🔄 Обновить размеры", on_click=update_sizes)

        color = ft.TextField(label="Цвет", value=product.get("color", "") if is_edit else "")
        material = ft.TextField(label="Материал", value=product.get("material", "") if is_edit else "")
        avail = ft.Checkbox(label="В наличии", value=product.get("availability", True) if is_edit else True)

        img_path = ft.TextField(label="Путь к фото на ПК", value=product.get("image_path", "") if is_edit else "")
        preview = ft.Image(src="https://via.placeholder.com/150", width=150, height=150, fit=ft.BoxFit.COVER)

        def save(e):
            try:
                cbs = sizes_container.data or []
                selected_sizes = [cb.label for cb in cbs if cb.value]
                sizes_str = ", ".join(selected_sizes)
                
                final_image_path = img_path.value
                if final_image_path and not final_image_path.startswith("/uploads/"):
                    app.ok("Загрузка фото...")
                    final_image_path = products_api.upload_image(final_image_path)

                data = {
                    "name": name.value,
                    "description": desc.value,
                    "price": float(price.value or 0),
                    "type": type_dd.value,
                    "category": level_dd.value,
                    "brand": brand_dd.value,
                    "size": sizes_str,
                    "color": color.value,
                    "material": material.value,
                    "availability": avail.value,
                    "image_path": final_image_path,
                }
                if is_edit:
                    products_api.update_product(product["id"], data)
                    app.ok("Товар обновлён")
                else:
                    products_api.create_product(data)
                    app.ok("Товар добавлен")
                dlg.open = False
                app.page.update()
                refresh_products()
            except Exception as ex:
                app.error(str(ex))

        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Column([
                name, desc, price, 
                ft.Row([type_dd, level_dd]),
                brand_dd,
                ft.Row([ft.Text("Доступные размеры:"), btn_update]), 
                sizes_container,
                color, material, avail,
                img_path, preview
            ], width=400, height=700, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: setattr(dlg, "open", False) or app.page.update()),
                ft.Button("Сохранить", on_click=save),
            ],
        )
        
        app.page.overlay.append(dlg)
        dlg.open = True
        app.page.update()
        
        update_sizes()

    def refresh_products():
        data = products_api.list_products(limit=200)
        rows = []
        for p in data:
            def make_del(pid, name_):
                def _del(e):
                    products_api.delete_product(pid)
                    app.ok(f"Удалён: {name_}")
                    refresh_products()
                return _del

            img_url = "https://via.placeholder.com/50"
            if p.get("image_path"):
                if p["image_path"].startswith("http"): img_url = p["image_path"]
                elif p["image_path"].startswith("/uploads/"): img_url = f"{BASE_URL}{p['image_path']}"
                else: img_url = p["image_path"]

            rows.append(ft.ListTile(
                leading=ft.Image(src=img_url, width=50, height=50, fit=ft.BoxFit.COVER),
                title=ft.Text(p["name"]),
                subtitle=ft.Text(f'{p["price"]:.2f} ₽ | {p.get("type","")} | {p.get("category","")}'),
                trailing=ft.Row([
                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, prod=p: open_product_form(prod)),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=make_del(p["id"], p["name"])),
                ], width=120),
            ))
        products_box.controls = rows or [ft.Text("Товаров нет")]

    orders_box = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    def refresh_orders():
        orders_box.controls = [ft.ListTile(
            title=ft.Text(f'№{o["id"]} — {o["total"]:.2f} ₽'),
            subtitle=ft.Text(f'Статус: {o["status"]}'),
            trailing=ft.PopupMenuButton(items=[
                ft.PopupMenuItem(content=ft.Text("Оплачен"), on_click=lambda e, oid=o["id"]: (admin_api.set_status(oid, "Оплачен"), refresh_orders())),
                ft.PopupMenuItem(content=ft.Text("Отправлен"), on_click=lambda e, oid=o["id"]: (admin_api.set_status(oid, "Отправлен"), refresh_orders())),
                ft.PopupMenuItem(content=ft.Text("Доставлен"), on_click=lambda e, oid=o["id"]: (admin_api.set_status(oid, "Доставлен"), refresh_orders())),
            ]),
        ) for o in admin_api.all_orders()]

    promos_box = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    code = ft.TextField(label="Код")
    pct = ft.TextField(label="%", width=80)
    fix = ft.TextField(label="₽", width=80)

    def refresh_promos():
        promos_box.controls = [ft.ListTile(
            title=ft.Text(p["code"]),
            subtitle=ft.Text(f'-{p["discount_percent"]}% / -{p["discount_fixed"]} ₽'),
            trailing=ft.IconButton(ft.Icons.DELETE, on_click=lambda e, pid=p["id"]: (admin_api.del_promo(pid), refresh_promos())),
        ) for p in admin_api.promos()]

    def add_promo(e):
        try:
            admin_api.add_promo({"code": code.value.upper(), "discount_percent": float(pct.value or 0),
                                 "discount_fixed": float(fix.value or 0), "is_active": True})
            code.value = pct.value = fix.value = ""
            refresh_promos()
        except Exception as ex:
            app.error(str(ex))

    users_box = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    def refresh_users():
        users = admin_api.users()
        rows = []
        for u in users:
            def make_role(uid, current_role):
                def _toggle(e):
                    new_role = "user" if current_role == "admin" else "admin"
                    admin_api.set_user_role(uid, new_role)
                    app.ok(f"Роль изменена на {new_role}")
                    refresh_users()
                return _toggle
            def make_del(uid, name):
                def _del(e):
                    try:
                        admin_api.delete_user(uid)
                        app.ok(f"Удалён: {name}")
                        refresh_users()
                    except Exception as ex:
                        app.error(str(ex))
                return _del
            rows.append(ft.ListTile(
                title=ft.Text(f'{u["username"]} ({u["role"]})'),
                subtitle=ft.Text(u["email"]),
                trailing=ft.Row([
                    ft.IconButton(ft.Icons.ADMIN_PANEL_SETTINGS, tooltip="Сменить роль", on_click=make_role(u["id"], u["role"])),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=make_del(u["id"], u["username"])),
                ], width=110),
            ))
        users_box.controls = rows

    refresh_products()
    refresh_orders()
    refresh_promos()
    refresh_users()

    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Товары"),
            ft.Tab(label="Заказы"),
            ft.Tab(label="Промокоды"),
            ft.Tab(label="Пользователи"),
        ]
    )

    tab_view = ft.TabBarView(
        expand=True,
        controls=[
            ft.Column([ft.Button("➕ Добавить товар", on_click=lambda e: open_product_form(None)), products_box], expand=True, spacing=10),
            orders_box,
            ft.Column([ft.Row([code, pct, fix, ft.IconButton(ft.Icons.ADD, on_click=add_promo)]), promos_box], expand=True),
            users_box,
        ]
    )

    return ft.Column(
        controls=[
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: app.go("profile")),
                ft.Text("Админ-панель", size=20, weight=ft.FontWeight.BOLD),
            ]),
            ft.Tabs(
                selected_index=0,
                length=4,
                expand=True,
                content=ft.Column([tab_bar, tab_view], expand=True),
            ),
        ],
        expand=True,
        spacing=10
    )