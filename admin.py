import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "FarmConnect - Admin"
    page.bgcolor = "#3A936C"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0

    def tela_inicial():
        def on_login(e):
            page.go("/login")

        def on_register(e):
            page.go("/cadastro")

        typing_text = ft.Text("Gerencie agendamentos e estoques de medicamentos especializados", size=20, color=ft.colors.BLACK87)

        async def start_typing_effect():
            full_text = "Administre com eficiência e segurança."
            typing_text.value = ""
            for char in full_text:
                typing_text.value += char
                await page.update_async()
                await asyncio.sleep(0.05)

        page.on_view_pop = lambda _: start_typing_effect()

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src="logo.png", width=110, height=40),
                    ft.Row(
                        [
                            ft.TextButton("Painel", style=ft.ButtonStyle(color=ft.colors.WHITE70)),
                            ft.TextButton("Suporte", style=ft.ButtonStyle(color=ft.colors.WHITE70)),
                            ft.ElevatedButton(
                                content=ft.Row([ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS), ft.Text("Registrar ADM")]),
                                on_click=on_register,
                                style=ft.ButtonStyle(
                                    bgcolor="white",
                                    color="#14532D",
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                                    overlay_color="#BBF7D0"
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
                                    overlay_color="#86EFAC"
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
            bgcolor="#14532D",
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK38, offset=ft.Offset(0, 6)),
            animate=ft.Animation(600, "easeInOut")
        )

        left_card = ft.Container(
            padding=40,
            bgcolor="white",
            border_radius=30,
            shadow=ft.BoxShadow(blur_radius=35, color=ft.colors.BLACK12, offset=ft.Offset(0, 10)),
            content=ft.Column(
                [
                    ft.Text("Painel Administrativo", size=48, weight=ft.FontWeight.BOLD, color="#14532D"),
                    typing_text,
                    ft.Container(
                        margin=ft.margin.only(top=30),
                        content=ft.Row([
                            ft.Icon(ft.icons.SEARCH, color="#14532D"),
                            ft.TextField(
                                hint_text="Digite sua sugestão...",
                                expand=True,
                                border_color="#14532D",
                                border_radius=12
                            ),
                            ft.ElevatedButton(
                                "Enviar",
                                bgcolor="#14532D",
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                    overlay_color="#22C55E"
                                )
                            )
                        ], spacing=10),
                        border_radius=12,
                        padding=16,
                        bgcolor=ft.colors.GREEN_50
                    )
                ],
                spacing=28
            ),
            animate_opacity=400,
            animate_scale=ft.Animation(500, "easeInOut")
        )

        phone_image = ft.Container(
            content=ft.Image(src="img/admin_dashboard.png", width=750, height=800),
            rotate=ft.Rotate(angle=0.00),
            shadow=ft.BoxShadow(blur_radius=28, color=ft.colors.BLACK26, offset=ft.Offset(8, 12)),
            animate_rotation=ft.Animation(800, "easeInOut"),
            animate_opacity=ft.Animation(600, "easeInOut")
        )

        main_section = ft.Container(
            padding=60,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#F0FDF4", "#DCFCE7"]
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

        footer = ft.Container(
            content=ft.Column(
                [
                    ft.Text("FarmConnect Admin", size=16, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Soluções para gestão de medicamentos", size=12, color=ft.colors.WHITE70),
                    ft.Row([
                        ft.Icon(ft.icons.LOCAL_HOSPITAL, color=ft.colors.WHITE),
                        ft.Icon(ft.icons.HEALTH_AND_SAFETY, color=ft.colors.WHITE),
                        ft.Icon(ft.icons.GROUP, color=ft.colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6
            ),
            padding=20,
            bgcolor="#14532D",
            border_radius=0,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK26, offset=ft.Offset(0, -4))
        )

        return ft.View(
            route="/",
            controls=[
                ft.Column([header, main_section, footer], spacing=0, expand=True)
            ]
        )

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(tela_inicial())
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
