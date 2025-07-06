import flet as ft
from home import HomeApp
from tela_escolha import TelaEscolhaUsuario
# from main_teste import TelaInicial, TelaLogin, TelaCadastro, TelaUsuario
from admin import TelaLoginAdmin
from tela_principal_admin import TelaAdminDashboard
from tela_principal_usuario import TelaUsuarioDashboard
from usuario import TelaLoginUsuario
from database import criar_tabelas, add_qtd_agendamentos

# Arquivo PRINCIPAL para criação das rotas
criar_tabelas()
add_qtd_agendamentos()
def main(page: ft.Page):
    page.title = "FarmConnect"
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.window.maximized = True
    
    def route_change(e):
        page.views.clear()

        if page.route == "/":
            HomeApp(page)
        elif page.route == "/escolha_usuario":
             page.views.append(TelaEscolhaUsuario(page).build_tela())
        # elif page.route == "/login":
        #     page.views.append(TelaLogin(page).tela_login()) 
        # elif page.route == "/cadastro":
        #     page.views.append(TelaCadastro(page).tela_cadastro())
        elif page.route == "/usuario":
            page.views.append(TelaUsuarioDashboard(page).build_tela())
        elif page.route == "/login_admin":
            page.views.append(TelaLoginAdmin(page).build_tela())
        elif page.route == "/admin_dashboard":
            page.views.append(TelaAdminDashboard(page).build_tela())
        elif page.route == "/login_usuario":
            page.views.append(TelaLoginUsuario(page).build_tela())
        elif page.route == "/documentos":
            page.views.append(TelaUsuarioDashboard(page).tela_documentos())
        elif page.route == "/perfil":
            page.views.append(TelaUsuarioDashboard(page).tela_perfil_paciente())
        elif page.route == "/medicamentos_retirados":
            page.views.append(TelaUsuarioDashboard(page).tela_medicamentos_retirados())
        elif page.route == "/agendamento":
            page.views.append(TelaUsuarioDashboard(page).tela_agendamento())
        elif page.route == "/detalhes_medicamento":
            page.views.append(TelaUsuarioDashboard(page).tela_detalhes_medicamento())
        elif page.route == "/agendamentos":
            page.views.append(TelaUsuarioDashboard(page).tela_meus_agendamentos())
        elif page.route == "/agendamento_confirmado":
            page.views.append(TelaUsuarioDashboard(page).tela_agendamento_confirmado())
        elif page.route == "/politica_privacidade":
             page.views.append(HomeApp(page).politica_privacidade_view())
        elif page.route == "/termos_uso":
            page.views.append(HomeApp(page).termos_uso_view())
        elif page.route == "/contato":
            page.views.append(HomeApp(page).contato_view())

        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
