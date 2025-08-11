import flet as ft
import asyncio
from database import registrar_admin, verificar_login_admin, buscar_nome_adm

class TelaLoginAdmin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page_settings()
        self.page.on_view_pop = lambda _: self.start_typing_effect()

    def page_settings(self):
        self.page.title = "FarmConnect - Admin"
        self.page.bgcolor = "#ECFDF5"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
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

        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.RED_400, duration=3000)

        # Campos de Login
        self.login_email = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.login_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)

        # Campos de Cadastro
        self.cadastro_nome = ft.TextField(label="Nome completo", prefix_icon=ft.Icons.PERSON, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.cadastro_email = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.cadastro_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.cadastro_confirmar_senha = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)

        def login_click(e):
            if self.login_email.value.strip() and self.login_senha.value.strip():
                valido = verificar_login_admin(self.login_email.value.strip(), self.login_senha.value.strip())
                if valido:
                    nome_admin = buscar_nome_adm(self.login_email.value.strip())
                    self.page.session.set("admin_nome", nome_admin)
                    self.page.go("/admin_dashboard")
                else:
                    self.page.snack_bar.content.value = "Email ou senha incorretos."
                    self.page.snack_bar.open = True
                    self.page.update()
            else:
                self.page.snack_bar.content.value = "Preencha todos os campos."
                self.page.snack_bar.open = True
                self.page.update()

        def registrar_click(e):
            if (self.cadastro_nome.value.strip() and self.cadastro_email.value.strip() and self.cadastro_senha.value.strip() and self.cadastro_confirmar_senha.value.strip()):
                if self.cadastro_senha.value.strip() != self.cadastro_confirmar_senha.value.strip():
                    self.page.snack_bar.content.value = "As senhas não coincidem."
                    self.page.snack_bar.open = True
                    self.page.update()
                else:
                    sucesso = registrar_admin(
                        self.cadastro_nome.value.strip(),
                        self.cadastro_email.value.strip(),
                        self.cadastro_senha.value.strip()
                    )
                    if sucesso:
                        self.page.snack_bar.content.value = "Cadastro realizado com sucesso!"
                        self.page.snack_bar.bgcolor = ft.Colors.GREEN
                        self.page.snack_bar.open = True

                        # 🔹 Limpa os campos de cadastro do admin
                        self.cadastro_nome.value = ""
                        self.cadastro_email.value = ""
                        self.cadastro_senha.value = ""
                        self.cadastro_confirmar_senha.value = ""

                        self.page.update()
                        self.page.go("/login_admin")

                    else:
                        self.page.snack_bar.content.value = "Erro: Email já cadastrado."
                        self.page.snack_bar.bgcolor = ft.Colors.RED
                        self.page.snack_bar.open = True
                        self.page.update()
            else:
                self.page.snack_bar.content.value = "Preencha todos os campos."
                self.page.snack_bar.open = True
                self.page.update()

        header = ft.Container(
            content=ft.Row([
                ft.Image(src="img/logo.png", width=100, height=100),
                ft.Text("FarmConnect Admin", size=20, weight="bold", color=ft.Colors.BLUE_900)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=40, vertical=24),
            bgcolor=ft.Colors.WHITE,
            animate=ft.Animation(600, "easeInOut")
        )

        login_card = ft.Container(
            padding=30,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            content=ft.Column([
                ft.Text("Login", size=24, weight="bold", color=ft.Colors.BLUE_900),
                self.login_email,
                self.login_senha,
                ft.Row([
                    ft.ElevatedButton("Entrar", bgcolor=ft.Colors.BLUE_900, color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), overlay_color=ft.Colors.BLUE_500),
                    on_click=login_click
                ),
                ft.ElevatedButton("Voltar", bgcolor=ft.Colors.GREY_50, color=ft.Colors.BLUE_900,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), overlay_color=ft.Colors.BLUE_500),
                    on_click=lambda e: self.page.go("/escolha_usuario")
                )
                ]),
                ft.TextButton(
                    "Esqueceu a senha?",
                    on_click=lambda _: print("Redirecionar para recuperação de senha"),
                    style=ft.ButtonStyle(color=ft.Colors.BLUE_600, padding=ft.padding.only(top=10))
                )
            ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        )

        cadastro_card = ft.Container(
            padding=30,
            bgcolor="white",
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            content=ft.Column([
                ft.Text("Cadastro", size=24, weight="bold", color=ft.Colors.BLUE_900),
                self.cadastro_nome,
                self.cadastro_email,
                self.cadastro_senha,
                self.cadastro_confirmar_senha,
                ft.Row([
                    ft.ElevatedButton("Registrar", bgcolor=ft.Colors.BLUE_900, color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), overlay_color=ft.Colors.BLUE_500),
                    on_click=registrar_click
                ),
                ft.ElevatedButton("Voltar", bgcolor=ft.Colors.GREY_50, color=ft.Colors.BLUE_900,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), overlay_color=ft.Colors.BLUE_500),
                    on_click=lambda e: self.page.go("/escolha_usuario")
                )
                ]),
            ], spacing=20, scroll=ft.ScrollMode.ADAPTIVE)
        )

        cards_section = ft.Container(
            padding=50,
            expand=True,
            content=ft.ResponsiveRow(
                columns=12,
                controls=[
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        alignment=ft.alignment.center,
                        content=login_card
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        alignment=ft.alignment.center,
                        content=cadastro_card
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
                run_spacing=30
            )
        )

        footer = ft.Container(
            content=ft.Column([
                ft.Text("FarmConnect Admin", size=18, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("Soluções inteligentes para gestão de medicamentos.", size=14, color=ft.Colors.WHITE70),
                ft.Row([
                    ft.Icon(ft.Icons.LOCAL_HOSPITAL, color=ft.Colors.WHITE, size=26),
                    ft.Icon(ft.Icons.HEALTH_AND_SAFETY, color=ft.Colors.WHITE, size=26),
                    ft.Icon(ft.Icons.GROUP, color=ft.Colors.WHITE, size=26)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=14)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            padding=24,
            bgcolor=ft.Colors.BLUE_600,
            shadow=ft.BoxShadow(blur_radius=16, color=ft.Colors.BLACK26, offset=ft.Offset(0, -6))
        )

        return ft.View(
            route="/login_admin",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.WHITE,
            controls=[
                self.page.snack_bar,
                ft.Column([header, cards_section, footer], spacing=0, expand=True)
            ]
        )

if __name__ == "__main__":
    def main(page: ft.Page):
        tela_admin = TelaLoginAdmin(page)
        page.views.append(tela_admin.build_tela())
        page.update()

    ft.app(target=main)
