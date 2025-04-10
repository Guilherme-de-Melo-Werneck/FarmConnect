import flet as ft
from tela_usuario import tela_usuario
from tela_inicial import FarmConnectApp
from tela_cadastro import tela_cadastro
from tela_login import tela_login

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.bgcolor = "#2E7D32"
    page.scroll = ft.ScrollMode.AUTO

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        FarmConnectApp(
                            on_login=lambda e: page.go("/login"),
                            on_register=lambda e: page.go("/cadastro")
                        )
                    ]
                )
            )
            
        elif page.route == "/login":
            page.views.append(tela_login(page))
        elif page.route == "/cadastro":
            page.views.append(tela_cadastro(page))
        elif page.route == "/usuario":
            page.views.append(tela_usuario(page))

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Início do app

ft.app(target=main)
