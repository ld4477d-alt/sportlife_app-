import flet as ft
from frontend.api import auth_api


def build(app):
    username = ft.TextField(label="Логин")
    email = ft.TextField(label="Email")
    full_name = ft.TextField(label="ФИО")
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True)

    async def do(e):
        try:
            auth_api.register(username.value, email.value, password.value, full_name.value)
            app.go("catalog")
        except Exception as ex:
            app.error(str(ex))

    return ft.Column(
        controls=[
            ft.Text("Регистрация", size=24, weight=ft.FontWeight.BOLD),
            username,
            email,
            full_name,
            password,
            ft.Button("Создать", on_click=do),
            ft.TextButton("Назад", on_click=lambda e: app.go("login")),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        expand=True
    )