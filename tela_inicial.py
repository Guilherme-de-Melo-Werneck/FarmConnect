import flet as ft

def tela_inicial(page: ft.Page):
    def go_to_login(e):
        page.go("/login")

    def go_to_register(e):
        page.go("/cadastro")

    header = ft.Container(
        padding=ft.padding.symmetric(horizontal=30, vertical=10),
        bgcolor=ft.colors.GREEN_600,
        content=ft.Row(
            controls=[
                ft.Row([
                    ft.Image(src="/images/logo.png", width=50, height=50),
                    ft.Text("FarmConnect", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Row([
                    ft.TextButton("Sobre", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                    ft.TextButton("Ajuda", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                    ft.TextButton("Contato", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.TextButton("Entrar", on_click=go_to_login, style=ft.ButtonStyle(color=ft.colors.WHITE)),
                    ft.TextButton("Registrar", on_click=go_to_register, style=ft.ButtonStyle(color=ft.colors.WHITE)),
                ], alignment=ft.MainAxisAlignment.END),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    content = ft.Column([
        ft.Text(
            "Facilitar seus agendamentos e busca para medicamentos especializados",
            size=18,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER
        ),
        ft.Row([
            ft.TextField(label="Digite um medicamento", expand=True),
            ft.ElevatedButton("Enviar", bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE),
        ], alignment=ft.MainAxisAlignment.CENTER)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)

    footer = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Siga-nos", color=ft.colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.bottom_center,
        padding=10,
    )

    return ft.View(
        route="/",
        controls=[
            ft.Column([
                header,
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=content
                ),
                footer
            ], expand=True)
        ]
    )
