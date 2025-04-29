import flet as ft

PRIMARY_COLOR = ft.Colors.BLUE_600
SECONDARY_COLOR = ft.Colors.BLUE_900

class TelaEscolhaUsuario:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "FarmConnect - Escolha de Perfil"
        self.page.scroll = "auto"
        self.page.bgcolor = ft.Colors.WHITE

    def entrar_como_paciente(self, e):
        self.page.go("/login")

    def entrar_como_admin(self, e):
        self.page.go("/login_admin")

    def build_tela(self):
        logo = ft.Image(
            src="home/img_home/logo.png",
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
            color=ft.Colors.GREY_700,
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
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=15),
                overlay_color=ft.Colors.BLUE_700,
            ),
            on_click=self.entrar_como_paciente,
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
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=15),
                overlay_color=ft.Colors.BLUE_800,
            ),
            on_click=self.entrar_como_admin,
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
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                titulo,
                subtitulo,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
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
            bgcolor=ft.Colors.WHITE,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=5,
                blur_radius=30,
                color=ft.Colors.BLACK26,
                offset=ft.Offset(0, 8),
            ),
            animate_opacity=500
        )

        tela = ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
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

