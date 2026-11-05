import flet as ft
from frontend.api import auth_api
from frontend.api.client import api

def build(app):
    username = ft.TextField(label="Логин", width=300)
    password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=300)

    def do(e):
        try:
            auth_api.login(username.value, password.value)
            app.go("catalog")
        except Exception as ex:
            app.error(str(ex))

    def guest(e):
        api.user = {"id": 0, "username": "Гость", "role": "guest"}
        api.token = None
        app.go("catalog")

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Спорт лайф", size=32, weight=ft.FontWeight.BOLD),
                username,
                password,
                ft.Button("Войти", on_click=do, width=300),
                ft.TextButton("Регистрация", on_click=lambda e: app.go("register")),
                ft.Divider(),
                ft.Button("Войти как гость", on_click=guest, width=300),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True
    )