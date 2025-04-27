import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "FarmConnect - Admin"
    page.bgcolor = "#ECFDF5"  # Fundo ainda mais claro e suave
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0

    def tela_inicial():
        def on_login(e):
            page.go("/login")

        def on_register(e):
            page.go("/cadastro")

        typing_text = ft.Text("Gerencie agendamentos e estoques de medicamentos especializados", size=22, color="#065F46", weight="bold")

        async def start_typing_effect():
            full_text = "Administre com eficiência e segurança."
            typing_text.value = ""
            for char in full_text:
                typing_text.value += char
                await page.update_async()
                await asyncio.sleep(0.04)

        page.on_view_pop = lambda _: start_typing_effect()

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src="logo.png", width=120, height=50),
                    ft.Row(
                        [
                            ft.TextButton("Painel", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                            ft.TextButton("Suporte", style=ft.ButtonStyle(color=ft.colors.WHITE)),
                            ft.ElevatedButton(
                                content=ft.Row([ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS), ft.Text("Registrar ADM")]),
                                on_click=on_register,
                                style=ft.ButtonStyle(
                                    bgcolor="white",
                                    color="#059669",
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    overlay_color="#6EE7B7"
                                )
                            ),
                            ft.OutlinedButton(
                                content=ft.Row([ft.Icon(ft.icons.LOGIN), ft.Text("Entrar")]),
                                on_click=on_login,
                                style=ft.ButtonStyle(
                                    side=ft.BorderSide(1, ft.colors.WHITE),
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    color=ft.colors.WHITE,
                                    overlay_color="#6EE7B7"
                                )
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=16
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.symmetric(horizontal=40, vertical=24),
            bgcolor="#10B981",
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK38, offset=ft.Offset(0, 8)),
            animate=ft.Animation(600, "easeInOut")
        )

        left_card = ft.Container(
            padding=40,
            bgcolor="white",
            border_radius=30,
            shadow=ft.BoxShadow(blur_radius=25, color=ft.colors.BLACK12, offset=ft.Offset(0, 8)),
            content=ft.Column(
                [
                    ft.Text("Painel Administrativo", size=42, weight=ft.FontWeight.BOLD, color="#10B981"),
                    typing_text,
                    ft.Container(
                        margin=ft.margin.only(top=30),
                        content=ft.Row([
                            ft.Icon(ft.icons.SEARCH, color="#10B981"),
                            ft.TextField(
                                hint_text="Digite sua sugestão...",
                                expand=True,
                                border_color="#10B981",
                                border_radius=12
                            ),
                            ft.ElevatedButton(
                                "Enviar",
                                bgcolor="#10B981",
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    overlay_color="#6EE7B7"
                                )
                            )
                        ], spacing=10),
                        border_radius=12,
                        padding=16,
                        bgcolor=ft.colors.GREEN_50
                    )
                ],
                spacing=32
            ),
            animate_opacity=500,
            animate_scale=ft.Animation(600, "easeInOut")
        )

        phone_image = ft.Container(
            content=ft.Image(src="administrador/img_adm/tela_adm.png", width=700, height=700),
            rotate=ft.Rotate(angle=0.00),
            shadow=ft.BoxShadow(blur_radius=24, color=ft.colors.BLACK26, offset=ft.Offset(6, 10)),
            animate_rotation=ft.Animation(700, "easeInOut"),
            animate_opacity=ft.Animation(500, "easeInOut")
        )

        main_section = ft.Container(
            padding=50,
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#D1FAE5", "#A7F3D0"]
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
                    ft.Text("FarmConnect Admin", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ft.Text("Soluções inteligentes para gestão de medicamentos.", size=14, color=ft.colors.WHITE70),
                    ft.Row([
                        ft.Icon(ft.icons.LOCAL_HOSPITAL, color=ft.colors.WHITE, size=26),
                        ft.Icon(ft.icons.HEALTH_AND_SAFETY, color=ft.colors.WHITE, size=26),
                        ft.Icon(ft.icons.GROUP, color=ft.colors.WHITE, size=26)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=14)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8
            ),
            padding=24,
            bgcolor="#10B981",
            border_radius=0,
            shadow=ft.BoxShadow(blur_radius=16, color=ft.colors.BLACK26, offset=ft.Offset(0, -6))
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
