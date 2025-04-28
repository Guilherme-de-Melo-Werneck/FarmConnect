import flet as ft
from home.home import HomeApp
from home.tela_escolha import TelaEscolhaUsuario

# Arquivo PRINCIPAL, para criação das rotas.

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.padding = 0
    page.bgcolor = ft.colors.WHITE
    page.scroll = "auto"

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            HomeApp(page)
        
        elif page.route == "/escolha_usuario":
            TelaEscolhaUsuario(page)

        page.update()

    page.on_route_change = route_change
    page.go("/")  # Inicia na Home

ft.app(target=main)
