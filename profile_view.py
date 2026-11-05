import flet as ft
from frontend.api.client import api


def build(app):
    u = api.user or {}
    is_admin = u.get("role") == "admin"

    def logout(e):
        api.token = None
        api.user = None
        app.go("login")

    return ft.Column(
        controls=[
            ft.Row([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: app.go("catalog")),
                ft.Text("Профиль", size=20, weight=ft.FontWeight.BOLD),
            ]),
            ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON), radius=40),
            ft.Text(u.get("username", ""), size=20, weight=ft.FontWeight.BOLD),
            ft.Text(u.get("email", "")),
            ft.Text(f'Роль: {u.get("role", "")}'),
            ft.Button("Админ-панель", visible=is_admin, on_click=lambda e: app.go("admin")),
            ft.TextButton("Избранное", on_click=lambda e: app.go("favorites")),
            ft.TextButton("Выйти", on_click=logout),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        spacing=15
    )