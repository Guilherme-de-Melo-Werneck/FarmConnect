import flet as ft
from farmconnect.home.home import HomeApp
from farmconnect.home.tela_escolha import TelaEscolhaUsuario
from main_teste import TelaInicial, TelaLogin, TelaCadastro, TelaUsuario
from farmconnect.administrador.admin import TelaLoginAdmin
from farmconnect.administrador.tela_principal import TelaAdminDashboard
from farmconnect.usuario.usuario import TelaLoginUsuario

# Arquivo PRINCIPAL para criação das rotas

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE
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
        elif page.route == "/login_admin":
            page.views.append(TelaLoginAdmin(page).build_tela())
        elif page.route == "/admin_dashboard":
            page.views.append(TelaAdminDashboard(page).build_tela())
        elif page.route == "/login_usuario":
            page.views.append(TelaLoginUsuario(page).build_tela())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)
