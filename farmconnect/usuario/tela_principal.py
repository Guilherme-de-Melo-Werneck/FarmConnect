import flet as ft

def tela_usuario(page: ft.Page):
    return ft.View(
        route="/usuario",
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#EFF6FF", "#DBEAFE"]
                ),
                content=ft.ResponsiveRow([
                    # SIDEBAR
                    ft.Container(
                        width=260,
                        padding=20,
                        bgcolor="#1E3A8A",
                        border_radius=16,
                        col={"xs": 12, "md": 3, "lg": 2},
                        content=ft.Column([
                            ft.Image(src="logo.png", width=120, height=40),
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            *[
                                ft.ElevatedButton(
                                    text,
                                    width=220,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.WHITE,
                                        color="#1E3A8A",
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(vertical=12),
                                    )
                                ) for text in [
                                    "Ver Perfil", "Medicamentos Retirados", "Agendamentos",
                                    "Documentos Necessários", "Editar Dados"
                                ]
                            ],
                            ft.Container(expand=True),  # empurra o botão para baixo
                            ft.ElevatedButton(
                                "Sair",
                                width=220,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.RED_400,
                                    color=ft.colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(vertical=12),
                                ),
                                on_click=lambda e: page.go("/")
                            ),
                        ], spacing=16, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # CONTEÚDO PRINCIPAL
                    ft.Container(
                        expand=True,
                        padding=20,
                        col={"xs": 12, "md": 9, "lg": 10},
                        content=ft.Column([
                            # TOPO
                            ft.Container(
                                bgcolor="#1E40AF",
                                border_radius=16,
                                padding=ft.padding.symmetric(horizontal=20, vertical=18),
                                shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK12, offset=ft.Offset(0, 3)),
                                content=ft.ResponsiveRow([
                                    ft.Image(src="logo.png", width=110, col={"xs": 12, "md": 2}),
                                    ft.TextField(
                                        hint_text="Buscar medicamentos...",
                                        prefix_icon=ft.icons.SEARCH,
                                        border_radius=12,
                                        bgcolor=ft.colors.WHITE,
                                        height=45,
                                        col={"xs": 12, "md": 6}
                                    ),
                                    ft.Row([
                                        ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                                        ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                    ], spacing=10, alignment=ft.MainAxisAlignment.END, col={"xs": 12, "md": 4})
                                ])
                            ),

                            # CONTEÚDO
                            ft.Container(
                                expand=True,
                                alignment=ft.alignment.top_center,
                                padding=30,
                                content=ft.Container(
                                    width=900,
                                    padding=30,
                                    bgcolor=ft.colors.WHITE,
                                    border_radius=20,
                                    shadow=ft.BoxShadow(blur_radius=18, color=ft.colors.BLACK12, offset=ft.Offset(0, 5)),
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Text(
                                                "MEDICAMENTOS DISPONÍVEIS",
                                                size=24,
                                                weight=ft.FontWeight.W_600,
                                                color="#1E3A8A"
                                            )
                                        ], alignment=ft.MainAxisAlignment.CENTER),

                                        ft.Row([
                                            ft.OutlinedButton("Mais Buscados"),
                                            ft.OutlinedButton("Meus Agendamentos"),
                                            ft.OutlinedButton("Feedback"),
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),

                                        ft.Divider(height=25),

                                        # CARDS CENTRALIZADOS
                                        ft.ResponsiveRow([
                                            *[
                                                ft.Container(
                                                    alignment=ft.alignment.center,  # Centraliza todo o card
                                                    padding=16,
                                                    bgcolor="#F8FAFC",
                                                    border_radius=16,
                                                    shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.BLACK12, offset=ft.Offset(0, 4)),
                                                    col={"xs": 12, "sm": 6, "md": 4},
                                                    content=ft.Column([
                                                        ft.Image(src="/images/remedio.png", width=100, height=100),
                                                        ft.Text(
                                                            "INTERFERON ALFA 2B\n3MUI INJ",
                                                            text_align=ft.TextAlign.CENTER,
                                                            size=13,
                                                            weight=ft.FontWeight.BOLD,
                                                            color="#1E3A8A"
                                                        ),
                                                        ft.ElevatedButton(
                                                            "ADICIONAR",
                                                            width=130,
                                                            bgcolor="#1E3A8A",
                                                            color=ft.colors.WHITE,
                                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                                                        )
                                                    ], spacing=12, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
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

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.bgcolor = "#EFF6FF"
    page.scroll = ft.ScrollMode.ADAPTIVE

    def route_change(route):
        page.views.clear()
        if page.route == "/usuario":
            page.views.append(tela_usuario(page))
        page.update()

    page.on_route_change = route_change
    page.go("/usuario")  # Página inicial de teste

ft.app(target=main)


