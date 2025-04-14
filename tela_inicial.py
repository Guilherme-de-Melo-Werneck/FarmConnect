import flet as ft

def main(page: ft.Page):
    page.title = "Farmconnect"
    page.bgcolor = "#3A936C"
    page.padding = 0

    # Header: logo à esquerda, menu à direita
    header = ft.Container(
        content=ft.Row(
            [
                ft.Image(src="logo.png", width=100, height=50),
                ft.Row(
                    [
                        ft.Text("Feedback", size=14, color=ft.colors.WHITE),
                        ft.Text("Ajuda", size=14, color=ft.colors.WHITE),
                        ft.Text("Contato", size=14, color=ft.colors.WHITE),
                        ft.ElevatedButton("Registrar", bgcolor="#D9F6E6", color="black", height=30),
                        ft.ElevatedButton("Entrar", bgcolor="#D9F6E6", color="black", height=30),
                    ],
                    spacing=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=30, vertical=20),
        bgcolor="#3A936C"
    )

    # Texto principal e campo de sugestão
    left_content = ft.Column(
        [
            ft.Text("Farmconnect", size=50, color="white", weight="bold"),
            ft.Text(
                "Facilitar seus agendamentos e\nbusca para medicamentos\nespecializados",
                size=30,
                color="white"
            ),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.SEARCH, color="black"),
                    ft.TextField(hint_text="Digite uma sugestão", expand=True),
                    ft.ElevatedButton("Enviar", bgcolor="#0066CC", color="white")
                ], spacing=10),
                border=ft.border.all(1, ft.colors.BLACK),
                bgcolor=ft.colors.WHITE,
                padding=10,
                width=400
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START
    )

    # Mockup do celular à direita
    phone_image = ft.Image(
        src= "img/celular.png",
        width=400,
        height=400,
    )

    # Seção principal
    main_section = ft.Container(
        content=ft.Row(
            [left_content, phone_image],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        padding=30,
        expand=True
    )

    # Footer ajustado para ocupar 100% da largura
    footer = ft.Container(
        content=ft.Column(
            [
                ft.Text("Siga-nos:", size=15, color="black"),
                ft.Row(
                    [
                        ft.Image(src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png", width=30),
                        ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733547.png", width=30),
                        ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733585.png", width=30),
                    ],
                    
                    spacing=20
                )
            ],
        ),
        bgcolor="#99ACFF",
        padding=30,
    )

    # Adiciona tudo à página
    page.add(
        ft.Column(
            [header, main_section, footer],
            spacing=0,
            expand=True
        )
    )

ft.app(target=main)


