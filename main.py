import flet as ft
import asyncio

#Teste
def main(page: ft.Page):
    page.title = "Farmconnect"
    page.bgcolor = "#3A936C"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0

    def tela_inicial():
        def on_login(e):
            page.go("/login")

        def on_register(e):
            page.go("/cadastro")

        typing_text = ft.Text("Facilitar seus agendamentos e busca para medicamentos especializados", size=20, color=ft.colors.BLACK87)

        async def start_typing_effect():
            full_text = "Conectando você ao cuidado que merece..."
            typing_text.value = ""
            for char in full_text:
                typing_text.value += char
                await page.update_async()
                await asyncio.sleep(0.05)

        page.on_view_pop = lambda _: start_typing_effect()

        # HEADER MODERNO COM HOVER
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src="logo.png", width=110, height=40),
                    ft.Row(
                        [
                            ft.TextButton("Feedback", style=ft.ButtonStyle(color=ft.colors.WHITE70)),
                            ft.TextButton("Ajuda", style=ft.ButtonStyle(color=ft.colors.WHITE70)),
                            ft.TextButton("Contato", style=ft.ButtonStyle(color=ft.colors.WHITE70)),
                            ft.ElevatedButton(
                                content=ft.Row([ft.Icon(ft.icons.PERSON_ADD), ft.Text("Registrar")]),
                                on_click=on_register,
                                style=ft.ButtonStyle(
                                    bgcolor="white",
                                    color="#1E3A8A",
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                                    overlay_color="#DBEAFE"
                                )
                            ),
                            ft.OutlinedButton(
                                content=ft.Row([ft.Icon(ft.icons.LOGIN), ft.Text("Entrar")]),
                                on_click=on_login,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, ft.colors.WHITE),
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                                    color=ft.colors.WHITE,
                                    overlay_color="#93C5FD"
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=14
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.symmetric(horizontal=32, vertical=20),
            bgcolor="#1E3A8A",
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK38, offset=ft.Offset(0, 6)),
            animate=ft.Animation(600, "easeInOut")
        )

        # CARD COM TYPING EFFECT E INTERAÇÃO
        left_card = ft.Container(
            padding=40,
            bgcolor="white",
            border_radius=30,
            shadow=ft.BoxShadow(blur_radius=35, color=ft.colors.BLACK12, offset=ft.Offset(0, 10)),
            content=ft.Column(
                [
                    ft.Text("FarmConnect", size=48, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                    typing_text,
                    ft.Container(
                        margin=ft.margin.only(top=30),
                        content=ft.Row([
                            ft.Icon(ft.icons.SEARCH, color="#1E3A8A"),
                            ft.TextField(
                                hint_text="Digite sua sugestão...",
                                expand=True,
                                border_color="#1E3A8A",
                                border_radius=12
                            ),
                            ft.ElevatedButton(
                                "Enviar",
                                bgcolor="#1E3A8A",
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                    overlay_color="#3B82F6"
                                )
                            )
                        ], spacing=10),
                        border_radius=12,
                        padding=16,
                        bgcolor=ft.colors.BLUE_50
                    )
                ],
                spacing=28
            ),
            animate_opacity=400,
            animate_scale=ft.Animation(500, "easeInOut")
        )

        # IMAGEM ILUSTRATIVA COM SUAVIDADE
        phone_image = ft.Container(
            content=ft.Image(src="img/celular.png", width=420, height=420),
            rotate=ft.Rotate(angle=0.02),
            shadow=ft.BoxShadow(blur_radius=28, color=ft.colors.BLACK26, offset=ft.Offset(8, 12)),
            animate_rotation=ft.Animation(800, "easeInOut"),
            animate_opacity=ft.Animation(600, "easeInOut")
        )

        # BACKGROUND GRADIENTE ANIMADO
        main_section = ft.Container(
            padding=60,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#F0F9FF", "#E0F2FE"]
            ),
            content=ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col={"sm": 12, "md": 6}, content=left_card),
                    ft.Container(col={"sm": 12, "md": 6}, content=phone_image, alignment=ft.alignment.center)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        # FOOTER SOCIAL COM MICROINTERAÇÃO
        redes = [
            ("https://cdn-icons-png.flaticon.com/512/2111/2111463.png", "Instagram"),
            ("https://cdn-icons-png.flaticon.com/512/733/733547.png", "Facebook"),
            ("https://cdn-icons-png.flaticon.com/512/733/733585.png", "Twitter")
        ]

        social_icons = [
            ft.Container(
                content=ft.Image(src=icon, width=24),
                padding=8,
                border_radius=50,
                bgcolor=ft.colors.WHITE,
                tooltip=name,
                animate_scale=ft.Animation(300, "easeInOut"),
                on_hover=lambda e, cont=icon: setattr(e.control, "scale", 1.15 if e.data == "true" else 1)
            ) for icon, name in redes
        ]

        # FOOTER AJUSTADO COM TEXTO CENTRALIZADO
        footer = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Siga-nos nas redes sociais",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Image(src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png", width=22),
                                padding=6,
                                border_radius=50,
                                bgcolor=ft.colors.WHITE,
                                tooltip="Instagram",
                                on_click=lambda _: print("Instagram")
                            ),
                            ft.Container(
                                content=ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733547.png", width=22),
                                padding=6,
                                border_radius=50,
                                bgcolor=ft.colors.WHITE,
                                tooltip="Facebook",
                                on_click=lambda _: print("Facebook")
                            ),
                            ft.Container(
                                content=ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733585.png", width=22),
                                padding=6,
                                border_radius=50,
                                bgcolor=ft.colors.WHITE,
                                tooltip="Twitter",
                                on_click=lambda _: print("Twitter")
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            ),
            padding=16,
            bgcolor="#1E3A8A",
            shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK26, offset=ft.Offset(0, -4)),
            border_radius=0
        )

        return ft.View(
            route="/",
            controls=[
                ft.Column([header, main_section, footer], spacing=0, expand=True)
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

        email = ft.TextField(
            label="Email",
            prefix_icon=ft.icons.EMAIL,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.WHITE,
            expand=True
        )

        senha = ft.TextField(
            label="Senha",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.icons.LOCK,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.WHITE,
            expand=True
        )

        campos_login = ft.Column(
            controls=[email, senha],
            spacing=10,
        )

        card_container = ft.Container(
            width=380,
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=18,
            height=360,  # << diminuído aqui
            shadow=ft.BoxShadow(
                blur_radius=20,
                color=ft.colors.BLACK26,
                offset=ft.Offset(0, 6)
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Text("Bem-vindo!👋", size=22, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                    ft.Text("Acesse sua conta para continuar", size=13, color=ft.colors.GREY_700),
                    campos_login,
                    ft.ElevatedButton(
                        "Entrar",
                        width=180,
                        height=42,
                        bgcolor="#1E3A8A",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=3
                        ),
                        on_click=login_click
                    ),
                    ft.TextButton(
                        "Voltar à tela inicial",
                        on_click=voltar_click,
                        style=ft.ButtonStyle(color="#1E3A8A")
                    )
                ]
            )
        )

        return ft.View(
            route="/login",
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#F8FAFC", "#E3F2FD"]
                    ),
                    content=ft.ResponsiveRow(
                        columns=12,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                col={"sm": 12, "md": 6, "lg": 4},
                                content=card_container
                            )
                        ]
                    )
                )
            ]
        )


    def tela_cadastro():
        def registrar_click(e):
            if nome.value.strip() and email.value.strip() and cpf.value.strip() and nascimento.value.strip() and senha.value.strip():
                page.snack_bar = ft.SnackBar(ft.Text("Cadastro realizado com sucesso!"))
                page.snack_bar.open = True
                page.go("/login")
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Preencha todos os campos."))
                page.snack_bar.open = True
                page.update()

        def voltar_click(e):
            page.go("/")

        def cpf_change(e):
            texto_original = cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))
            if len(numeros) > 11:
                numeros = numeros[:11]

            formatado = ""
            if len(numeros) >= 3:
                formatado += numeros[:3] + "."
            if len(numeros) >= 6:
                formatado += numeros[3:6] + "."
            if len(numeros) >= 9:
                formatado += numeros[6:9] + "-"
            if len(numeros) > 9:
                formatado += numeros[9:]
            elif len(numeros) > 6:
                formatado += numeros[6:9]
            elif len(numeros) > 3:
                formatado += numeros[3:6]
            elif len(numeros) > 0:
                formatado += numeros[0:3]

            if cpf.value != formatado:
                cpf.value = formatado
                cpf.update()

        def nascimento_change(e):
            texto_original = nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))
            if len(numeros) > 8:
                numeros = numeros[:8]

            formatado = ""
            if len(numeros) >= 2:
                formatado += numeros[:2] + "/"
            if len(numeros) >= 4:
                formatado += numeros[2:4] + "/"
            if len(numeros) > 4:
                formatado += numeros[4:]
            elif len(numeros) > 2:
                formatado += numeros[2:]

            if nascimento.value != formatado:
                nascimento.value = formatado
                nascimento.update()

        nome = ft.TextField(label="Nome completo", prefix_icon=ft.icons.PERSON, border_radius=10, filled=True, bgcolor=ft.colors.WHITE, expand=True)
        email = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.colors.WHITE, expand=True)
        cpf = ft.TextField(label="CPF", prefix_icon=ft.icons.BADGE, border_radius=10, filled=True, bgcolor=ft.colors.WHITE, expand=True, keyboard_type=ft.KeyboardType.NUMBER, hint_text="Apenas números", on_change=cpf_change)
        nascimento = ft.TextField(label="Data de Nascimento", hint_text="DD/MM/AAAA", prefix_icon=ft.icons.CALENDAR_MONTH, border_radius=10, filled=True, bgcolor=ft.colors.WHITE, expand=True, on_blur=nascimento_change)
        senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, border_radius=10, filled=True, bgcolor=ft.colors.WHITE, expand=True)

        campos = ft.Column(
            spacing=10,
            controls=[nome, email, cpf, nascimento, senha]
        )

        card_container = ft.Container(
            width=420,
            padding=25,
            height=500,
            bgcolor=ft.colors.WHITE,
            border_radius=18,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK26, offset=ft.Offset(0, 6)),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.Text("Crie sua conta", size=22, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                    ft.Text("Preencha os dados abaixo", size=13, color=ft.colors.GREY_700),
                    campos,
                    ft.ElevatedButton(
                        "Cadastrar",
                        width=180,
                        height=42,
                        bgcolor="#1E3A8A",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            elevation=3
                        ),
                        on_click=registrar_click
                    ),
                    ft.TextButton(
                        "Voltar à tela inicial",
                        on_click=voltar_click,
                        style=ft.ButtonStyle(color="#1E3A8A")
                    )
                ]
            )
        )

        return ft.View(
            route="/cadastro",
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=["#F8FAFC", "#E3F2FD"]
                    ),
                    content=ft.ResponsiveRow(
                        columns=12,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                col={"sm": 12, "md": 6, "lg": 4},
                                content=card_container
                            )
                        ]
                    )
                )
            ]
        )

    
    def tela_usuario():
        return ft.View(
            route="/usuario",
            controls=[
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#F0F9FF", "#E0F2FE"]
                    ),
                    content=ft.ResponsiveRow([
                        # SIDEBAR
                        ft.Container(
                            width=280,
                            padding=20,
                            bgcolor="#1E3A8A",
                            border_radius=10,
                            col={"xs": 12, "md": 3, "lg": 2}, 
                            content=ft.Column([
                                ft.Image(src="logo.png", width=140, height=50),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.ElevatedButton("Ver Perfil", width=200, style=ft.ButtonStyle(bgcolor="white", color="#1E3A8A")),
                                ft.ElevatedButton("Medicamentos Retirados", width=200, style=ft.ButtonStyle(bgcolor="white", color="#1E3A8A")),
                                ft.ElevatedButton("Agendamentos", width=200, style=ft.ButtonStyle(bgcolor="white", color="#1E3A8A")),
                                ft.ElevatedButton("Documentos Necessários", width=200, style=ft.ButtonStyle(bgcolor="white", color="#1E3A8A")),
                                ft.ElevatedButton("Editar Dados", width=200, style=ft.ButtonStyle(bgcolor="white", color="#1E3A8A")),
                                ft.ElevatedButton("Sair", width=200, bgcolor=ft.colors.RED_400, color=ft.colors.WHITE, on_click=lambda e: page.go("/")),
                            ], spacing=14, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        ),

                        # CONTEÚDO PRINCIPAL
                        ft.Container(
                            expand=True,
                            padding=20,
                            col={"xs": 12, "md": 9},
                            content=ft.Column([
                                # TOPO
                                ft.Container(
                                    bgcolor="#1E40AF",
                                    border_radius=12,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=16),
                                    shadow=ft.BoxShadow(blur_radius=18, color=ft.colors.BLACK12, offset=ft.Offset(0, 4)),
                                    content=ft.ResponsiveRow([
                                        ft.Image(src="logo.png", width=110, col={"xs": 12, "md": 2}),
                                        ft.TextField(
                                            hint_text="Buscar",
                                            prefix_icon=ft.icons.SEARCH,
                                            border_radius=12,
                                            bgcolor=ft.colors.WHITE,
                                            col={"xs": 12, "md": 6}
                                        ),
                                        ft.Row([
                                            ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=22),
                                            ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
                                        ], spacing=10, col={"xs": 12, "md": 4})
                                    ])
                                ),

                                # CONTEÚDO
                                ft.Container(
                                    expand=True,
                                    alignment=ft.alignment.center,
                                    padding=30,
                                    content=ft.Container(
                                        width=900,
                                        padding=30,
                                        bgcolor=ft.colors.WHITE,
                                        border_radius=20,
                                        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 6)),
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Text("MEDICAMENTOS 🩹", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#1E3A8A"),
                                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                            ft.Row([
                                                ft.OutlinedButton("Mais Buscados"),
                                                ft.OutlinedButton("Meus Agendamentos"),
                                                ft.OutlinedButton("Feedback"),
                                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                            ft.Divider(height=20),

                                            # GRID DE MEDICAMENTOS RESPONSIVO
                                            ft.ResponsiveRow([
                                                *[
                                                    ft.Container(
                                                        padding=14,
                                                        bgcolor=ft.colors.BLUE_50,
                                                        border_radius=16,
                                                        shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK12, offset=ft.Offset(0, 4)),
                                                        col={"xs": 12, "sm": 6, "md": 4},
                                                        content=ft.Column([
                                                            ft.Image(src="/images/remedio.png", width=100, height=100),
                                                            ft.Row([
                                                                ft.Text(
                                                                "INTERFERON ALFA 2B\n3MUI INJ",
                                                                text_align=ft.TextAlign.CENTER,
                                                                size=13,
                                                                weight=ft.FontWeight.BOLD,
                                                                color="#1E3A8A"
                                                            ),
                                                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                                            
                                                            ft.Row([
                                                                ft.ElevatedButton(
                                                                "ADICIONAR",
                                                                width=130,
                                                                bgcolor="#1E3A8A",
                                                                color="white",
                                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                                            ),
                                                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                                                        ]
                                                        ),    
                                                    ) for _ in range(6)
                                                ]
                                            ], spacing=20, run_spacing=20)
                                        ], spacing=30)
                                    )
                                )
                            ], spacing=20)
                        )
                    ])
                )
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