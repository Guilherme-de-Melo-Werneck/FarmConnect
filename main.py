import flet as ft
from home.home import HomeApp
from home.tela_escolha import TelaEscolhaUsuario
from main_teste import TelaInicial, TelaLogin, TelaCadastro, TelaUsuario

# Arquivo PRINCIPAL para criação das rotas

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.padding = 0
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            HomeApp(page)
        elif page.route == "/escolha_usuario":
             page.views.append(TelaEscolhaUsuario(page).build_tela())
        elif page.route == "/login":
            page.views.append(TelaLogin(page).tela_login()) 
        elif page.route == "/cadastro":
            page.views.append(TelaCadastro(page).tela_cadastro())
        elif page.route == "/usuario":
            page.views.append(TelaUsuario(page).tela_usuario())
        elif page.route == "/admin":
            pass

        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
