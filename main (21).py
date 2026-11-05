import sys
import os

# Добавляем папку frontend в пути поиска, чтобы работали импорты из неё
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

import flet as ft
from views import (
    login_view, register_view, catalog_view, product_view,
    cart_view, orders_view, profile_view, admin_view, favorites_view
)

class App:
    def __init__(self, page):
        self.page = page
        self.page.title = "Спорт лайф"
        self.page.padding = 0

    def go(self, name, **kw):
        self.page.controls.clear()
        
        views = {
            "login": lambda: login_view.build(self),
            "register": lambda: register_view.build(self),
            "catalog": lambda: catalog_view.build(self),
            "product": lambda: product_view.build(self, kw.get("product_id")),
            "cart": lambda: cart_view.build(self),
            "orders": lambda: orders_view.build(self),
            "profile": lambda: profile_view.build(self),
            "admin": lambda: admin_view.build(self),
            "favorites": lambda: favorites_view.build(self),
        }
        
        self.page.controls.append(views[name]())
        self.page.update()

    def ok(self, m):
        s = ft.SnackBar(ft.Text(m, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN)
        self.page.overlay.append(s)
        s.open = True
        self.page.update()

    def error(self, m):
        s = ft.SnackBar(ft.Text(m, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
        self.page.overlay.append(s)
        s.open = True
        self.page.update()

def main(page: ft.Page):
    App(page).go("login")

if __name__ == "__main__":
    ft.run(main)