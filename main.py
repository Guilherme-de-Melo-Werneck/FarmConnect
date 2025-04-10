import flet as ft
from cadastro import tela_cadastro
from telainicial import tela_inicial

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()

        if page.route == "/cadastro":
            page.views.append(tela_cadastro(page))
        elif page.route == "/telainicial":
            page.views.append(tela_inicial(page))
        else:
            page.go("/cadastro")

        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
