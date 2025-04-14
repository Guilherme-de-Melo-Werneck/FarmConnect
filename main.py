import flet as ft

def main(page: ft.Page):
    page.title = "Farmconnect"
    page.bgcolor = "#3A936C"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    def tela_inicial():
        def on_login(e):
            page.go("/login")

        def on_register(e):
            page.go("/cadastro")

        # Header
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src="logo.png", width=100, height=50),
                    ft.Row(
                        [
                            ft.Text("Feedback", size=14, color="white"),
                            ft.Text("Ajuda", size=14, color="white"),
                            ft.Text("Contato", size=14, color="white"),
                            ft.ElevatedButton("Registrar", bgcolor="#D9F6E6", color="black", height=30, on_click=on_register),
                            ft.ElevatedButton("Entrar", bgcolor="#D9F6E6", color="black", height=30, on_click=on_login),
                        ],
                        spacing=20,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            margin = 0,
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            bgcolor="#3A936C"
        )

        # Texto principal e campo de sugestão
        left_content = ft.Column(
            [
                ft.Text("Farmconnect", size=50, color="black", weight="bold"),
                ft.Text(
                    "Facilitar seus agendamentos e\nbusca para medicamentos\nespecializados",
                    size=30,
                    color="black"
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
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        )

        # Imagem à direita
        phone_image = ft.Image(
            src="img/celular.png",
            width=400,
            height=400,
        )

        # Seção principal com fundo verde
        main_section = ft.Container(
            content=ft.Row(
                [left_content, phone_image],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            padding=30,
            margin = 0,
            expand=True,
            bgcolor="#3A936C",
        )

        # Rodapé
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
            margin = 0,
            padding=30,
        )

        return ft.View(
            route="/",
            controls= [ft.Column(
                [header, main_section, footer], 
                spacing=0, 
                expand=True
                )
            ]
        )
    

    def tela_login():
        def login_click(e):
            if email.value.strip() and senha.value.strip():
                page.go("/usuario")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos."))
                page.snack_bar.open = True
                page.update()

        def voltar_click(e):
            page.go("/")

        email = ft.TextField(label="Email", width=400)
        senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=400)

        return ft.View(
            route="/login",
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=25,
                        controls=[
                            ft.Text("LOGIN", size=28, weight=ft.FontWeight.BOLD),
                            email,
                            senha,
                            ft.Row([
                                ft.ElevatedButton("Entrar", on_click=login_click),
                                ft.TextButton("Voltar", on_click=voltar_click)
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                    ),
                    padding=20,
                    bgcolor = "#99ACFF",
                    border_radius=10,
                    margin=50
                ) 
            ]
        )

    def tela_cadastro():
        def cancelar_click(e):
            page.go("/")

        return ft.View(
            route="/cadastro",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.TextField(label="Nome Completo *", width=400),
                            ft.TextField(label="Endereço", width=400),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.TextField(label="CPF *", width=400),
                            ft.TextField(label="Telefone *", width=400),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.TextField(label="E-mail *", width=400),
                            ft.TextField(label="Verificar E-mail *", width=400),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.TextField(label="Senha *", password=True, width=400),
                            ft.TextField(label="Confirmar Senha *", password=True, width=400),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text("* Campos Obrigatórios", size=10, color="red")
                    ], spacing=15),
                    padding=20,
                    bgcolor = "#99ACFF",
                    border_radius=10,
                    margin=20
                ),

                ft.Row([
                    ft.ElevatedButton("CADASTRAR", bgcolor="white", color="black", width=150, on_click=lambda e: page.go("/login")),
                    ft.ElevatedButton("CANCELAR", bgcolor="white", color="black", width=150, on_click=cancelar_click),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=50),

                ft.Container(
                    content=ft.Column([
                        ft.Text("Siga-nos", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Row([
                            ft.Image(src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png", width=30),
                            ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733547.png", width=30),
                            ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733585.png", width=30),
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    padding=20
                )
            ]
        )

    def tela_usuario():
        return ft.View(
            route="/usuario",
            controls=[
                ft.Row([
                    ft.Container(
                        width=260,
                        bgcolor=ft.colors.WHITE,
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
                                ft.ElevatedButton("SAIR", width=180, bgcolor=ft.colors.RED_400, on_click=lambda e: page.go("/")),
                            ], spacing=10)
                        )
                    ),

                    ft.Container(
                        expand=True,
                        content=ft.Column([
                            ft.Container(
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
                            ),
                            
                            ft.Container(
                                alignment=ft.alignment.center,
                                expand=True,
                                content=ft.Container(
                                    bgcolor=ft.colors.WHITE,
                                    border_radius=10,
                                    padding=30,
                                    width=800,
                                    content=ft.Column([
                                        ft.Text("OLÁ, SEJA BEM VINDO", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                        ft.Row([
                                            ft.OutlinedButton("MAIS BUSCADOS"),
                                            ft.OutlinedButton("MEUS AGENDAMENTOS"),
                                            ft.OutlinedButton("FEEDBACK"),
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                        ft.Divider(height=20),
                                        ft.Row([
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
                                    ], spacing=30)
                                )
                            )
                        ], expand=True)
                    )
                ], expand=True, vertical_alignment=ft.CrossAxisAlignment.STRETCH)
            ]
        )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(tela_inicial())
        elif page.route == "/login":
            page.views.append(tela_login())
        elif page.route == "/cadastro":
            page.views.append(tela_cadastro())
        elif page.route == "/usuario":
            page.views.append(tela_usuario())
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
