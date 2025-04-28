import flet as ft
import asyncio

class TelaLoginAdmin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page_settings()
        self.page.on_view_pop = lambda _: self.start_typing_effect()

    def page_settings(self):
        self.page.title = "FarmConnect - Admin"
        self.page.bgcolor = "#ECFDF5"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.padding = 0

    async def start_typing_effect(self):
        full_text = "Administre com eficiência e segurança."
        self.typing_text.value = ""
        for char in full_text:
            self.typing_text.value += char
            await self.page.update_async()
            await asyncio.sleep(0.04)

    def build_tela(self):
        self.typing_text = ft.Text(
            "Gerencie agendamentos e estoques de medicamentos especializados",
            size=22,
            color="#065F46",
            weight="bold"
        )

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Image(src="administrador/img_adm/logo_verde.png", width=120, height=80),
                    ft.Text("FarmConnect Admin", size=20, weight="bold", color=ft.colors.WHITE)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.symmetric(horizontal=40, vertical=24),
            bgcolor="#10B981",
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK38, offset=ft.Offset(0, 8)),
            animate=ft.Animation(600, "easeInOut")
        )

        login_card = ft.Container(
            padding=30,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 6)),
            content=ft.Column([
                ft.Text("Login", size=24, weight="bold", color="#10B981"),
                ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.ElevatedButton("Entrar", bgcolor="#10B981", color="white",
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), overlay_color="#6EE7B7")),
                ft.TextButton(
                    "Esqueceu a senha?",
                    on_click=lambda _: print("Redirecionar para recuperação de senha"),
                    style=ft.ButtonStyle(color="#10B981", padding=ft.padding.only(top=10))
                )
            ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        )

        cadastro_card = ft.Container(
            padding=30,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 6)),
            content=ft.Column([
                ft.Text("Cadastro", size=24, weight="bold", color="#10B981"),
                ft.TextField(label="Nome completo", prefix_icon=ft.icons.PERSON, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK_OUTLINE, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.TextField(label="CNPJ da Farmácia", prefix_icon=ft.icons.BUSINESS, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.TextField(label="Nome da Farmácia", prefix_icon=ft.icons.LOCAL_PHARMACY, border_radius=10, filled=True, bgcolor=ft.colors.GREEN_50),
                ft.ElevatedButton("Registrar", bgcolor="#10B981", color="white",
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), overlay_color="#6EE7B7"))
            ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        )

        cards_section = ft.Container(
            padding=50,
            expand=True,
            content=ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(col={"sm": 12, "md": 6}, content=login_card, alignment=ft.alignment.center),
                    ft.Container(col={"sm": 12, "md": 6}, content=cadastro_card, alignment=ft.alignment.center)
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40
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
            shadow=ft.BoxShadow(blur_radius=16, color=ft.colors.BLACK26, offset=ft.Offset(0, -6))
        )

        return ft.View(
            route="/login_admin",
            controls=[
                ft.Column([header, cards_section, footer], spacing=0, expand=True)
            ]
        )

# Teste Local:
if __name__ == "__main__":
    def main(page: ft.Page):
        tela_admin = TelaLoginAdmin(page)
        page.views.append(tela_admin.build_tela())
        page.update()

    ft.app(target=main)