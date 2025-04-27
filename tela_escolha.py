import flet as ft

PRIMARY_COLOR = ft.colors.BLUE_600
SECONDARY_COLOR = ft.colors.BLUE_900

def tela_escolha_usuario(page: ft.Page):
    def entrar_como_paciente(e):
        page.go("/login_paciente")

    def entrar_como_admin(e):
        page.go("/login_admin")

    logo = ft.Image(
        src="img_home/logo.png",  # Ícone bonito 3D de saúde
        width=100,
        height=100,
    )

    titulo = ft.Text(
        "Bem-vindo à FarmConnect",
        size=32,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        color=SECONDARY_COLOR,
        animate_opacity=300
    )

    subtitulo = ft.Text(
        "Escolha como deseja acessar",
        size=20,
        text_align=ft.TextAlign.CENTER,
        color=ft.colors.GREY_700,
        animate_opacity=400
    )

    botao_paciente = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(name=ft.icons.PERSON_OUTLINE),
            ft.Text("Sou Paciente", size=16)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10),
        width=280,
        style=ft.ButtonStyle(
            bgcolor=PRIMARY_COLOR,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=15),
            overlay_color=ft.colors.BLUE_700,
        ),
        on_click=entrar_como_paciente,
    )

    botao_admin = ft.ElevatedButton(
        content=ft.Row([
            ft.Icon(name=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED),
            ft.Text("Sou Administrador", size=16)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10),
        width=280,
        style=ft.ButtonStyle(
            bgcolor=SECONDARY_COLOR,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=15),
            overlay_color=ft.colors.BLUE_800,
        ),
        on_click=entrar_como_admin,
    )

    botoes = ft.Column(
        controls=[botao_paciente, botao_admin],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        animate_opacity=500
    )

    conteudo_cartao = ft.Column(
        controls=[
            logo,
            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            titulo,
            subtitulo,
            ft.Divider(height=30, color=ft.colors.TRANSPARENT),
            botoes
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )

    card = ft.Container(
        content=conteudo_cartao,
        padding=40,
        width=420,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=5,
            blur_radius=30,
            color=ft.colors.BLACK26,
            offset=ft.Offset(0, 8),
        ),
        animate_opacity=500
    )

    tela = ft.Container(
        expand=True,
        bgcolor=ft.colors.WHITE,  # Fundo agora é totalmente branco
        content=ft.Row(
            [
                ft.Column(
                    controls=[card],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
    )

    return ft.View(
        route="/escolha_usuario",
        controls=[tela]
    )

def main(page: ft.Page):
    page.title = "FarmConnect - Escolha de Perfil"
    page.scroll = "auto"
    page.bgcolor = ft.colors.WHITE  # Fundo branco para toda a aplicação

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.go("/escolha_usuario")
        if page.route == "/escolha_usuario":
            page.views.append(tela_escolha_usuario(page))
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)

