import flet as ft

def tela_usuario(page: ft.Page):
    # Menu lateral esquerdo
    side_menu = ft.Container(
        width=260,
        bgcolor=ft.colors.BLACK,
        content=ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=20),
            bgcolor=ft.colors.BLUE_GREY_900,
            expand=True,
            content=ft.Column([
                ft.Image(src="/images/logo.png", width=150, height=60),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.ElevatedButton("VER PERFIL", width=180),
                ft.ElevatedButton("MEDICAMENTOS RETIRADOS", width=180),
                ft.ElevatedButton("AGENDAMENTOS", width=180),
                ft.ElevatedButton("DOCUMENTOS NECESSÁRIOS", width=180),
                ft.ElevatedButton("EDITAR DADOS", width=180),
                ft.ElevatedButton("SAIR", width=180, bgcolor=ft.colors.RED_400),
            ], spacing=10, alignment=ft.MainAxisAlignment.START)
        )
    )

    # Topo com logo, busca e perfil
    top_bar = ft.Container(
        bgcolor=ft.colors.GREEN_600,
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        content=ft.Row([
            ft.Image(src="/images/farmconnect_logo.png", width=120),
            ft.TextField(hint_text="Buscar", prefix_icon=ft.icons.SEARCH, expand=True),
            ft.Row([
                ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=25),
                ft.Text("JOÃO NASCIMENTO", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
            ], spacing=10)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # Conteúdo central
    welcome_text = ft.Text("OLÁ, SEJA BEM VINDO", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    buttons_row = ft.Row([
        ft.OutlinedButton("MAIS BUSCADOS"),
        ft.OutlinedButton("MEUS AGENDAMENTOS"),
        ft.OutlinedButton("FEEDBACK"),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    medicamentos = ft.Row([
        *[
            ft.Container(
                width=150,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                padding=10,
                content=ft.Column([
                    ft.Image(src="/images/remedio.png", width=100, height=100),
                    ft.Text("INTERFERON ALFA 2B\n3MUI INJ", text_align=ft.TextAlign.CENTER, size=12),
                    ft.ElevatedButton("ADICIONAR", width=130, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER)
            ) for _ in range(3)
        ]
    ], alignment=ft.MainAxisAlignment.CENTER)

    content_area = ft.Container(
        bgcolor=ft.colors.WHITE,
        border_radius=10,
        padding=30,
        width=800,
        content=ft.Column([welcome_text, buttons_row, ft.Divider(height=20), medicamentos], spacing=30)
    )

    return ft.View(
        route="/tela_usuario",
        controls=[
            ft.Row([
                side_menu,
                ft.Container(
                    expand=True,
                    content=ft.Column([
                        top_bar,
                        ft.Container(
                            alignment=ft.alignment.center,
                            expand=True,
                            content=content_area
                        )
                    ], expand=True)
                )
            ], expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)
        ]
    )
