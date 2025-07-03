import flet as ft
import asyncio
from database import registrar_usuario, verificar_login, buscar_nome_usuario, verificar_status_usuario

class TelaLoginUsuario:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page_settings()
        self.page.on_view_pop = lambda _: self.start_typing_effect()

    def page_settings(self):
        self.page.title = "FarmConnect - Usuário"
        self.page.bgcolor = "#EFF6FF"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.WHITE
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.padding = 0

    # async def start_typing_effect(self):
    #     full_text = "Administre com eficiência e segurança."
    #     self.typing_text.value = ""
    #     for char in full_text:
    #         self.typing_text.value += char
    #         await self.page.update_async()
    #         await asyncio.sleep(0.04)

    def build_tela(self):
        self.typing_text = ft.Text(
            "Teste",
            size=22,
            color="#065F46",
            weight="bold"
        )

        def cpf_change(e):
            texto_original = self.cadastro_cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

            if len(numeros) == 11:
                self.cadastro_nascimento.focus()

        def cpf_blur(e):
            texto_original = self.cadastro_cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

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

            self.cadastro_cpf.value = formatado
            self.cadastro_cpf.update()

        def nascimento_change(e):
            texto_original = self.cadastro_nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:8]

            if len(numeros) == 8:
                self.cadastro_telefone.focus()

        def nascimento_blur(e):
            texto_original = self.cadastro_nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:8]
            formatado = ""
            if len(numeros) >= 2:
                formatado += numeros[:2] + "/"
            if len(numeros) >= 4:
                formatado += numeros[2:4] + "/"
            if len(numeros) > 4:
                formatado += numeros[4:]
            elif len(numeros) > 2:
                formatado += numeros[2:]
            self.cadastro_nascimento.value = formatado
            self.cadastro_nascimento.update()

        def telefone_blur(e):
            texto_original = self.cadastro_telefone.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]
            
            if len(numeros) < 2:
                self.cadastro_telefone.value = numeros
            else:
                ddd = numeros[:2]
                parte1 = numeros[2:7] if len(numeros) > 6 else numeros[2:]
                parte2 = numeros[7:] if len(numeros) > 7 else ''
                self.cadastro_telefone.value = f"({ddd}) {parte1}-{parte2}" if parte1 else f"({ddd})"

            self.cadastro_telefone.update()

        def telefone_change(e):
            texto_original = self.cadastro_telefone.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

            if len(numeros) == 11:
                self.cadastro_senha.focus()

        self.page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.Colors.RED_400, duration=3000)

        # Campos de Login
        self.login_email = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.login_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)

        # Campos de Cadastro
        self.cadastro_nome = ft.TextField(label="Nome completo", prefix_icon=ft.Icons.PERSON, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.cadastro_email = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.cadastro_cpf = ft.TextField(label="CPF", prefix_icon=ft.Icons.BADGE, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50, on_blur=cpf_blur, on_change=cpf_change)
        self.cadastro_nascimento = ft.TextField(label="Nascimento", prefix_icon=ft.Icons.CALENDAR_MONTH, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50, on_blur=nascimento_blur, on_change=nascimento_change)
        self.cadastro_telefone = ft.TextField(label="Telefone", prefix_icon=ft.Icons.PHONE, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50, keyboard_type=ft.KeyboardType.PHONE, on_blur=telefone_blur, on_change=telefone_change)
        self.cadastro_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)
        self.cadastro_confirmar_senha = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK_OUTLINE, border_radius=10, filled=True, bgcolor=ft.Colors.GREY_50)

        def login_click(e):
            email = self.login_email.value.strip()
            senha = self.login_senha.value.strip()

            if email and senha:
                if verificar_login(email, senha):
                    status = verificar_status_usuario(email)

                    if status == "Aprovado":
                        nome_usuario = buscar_nome_usuario(email)
                        self.page.session.set("usuario_email", email)
                        self.page.session.set("usuario_nome", nome_usuario)
                        self.page.go("/usuario")
                    elif status == "Pendente":
                        self.page.snack_bar.content.value = "⚠️ Seu cadastro ainda está em análise. Aguarde a aprovação."
                        self.page.snack_bar.bgcolor = ft.Colors.AMBER_400
                        self.page.snack_bar.open = True
                        self.page.update()
                    elif status == "Recusado":
                        self.page.snack_bar.content.value = "❌ Seu cadastro foi recusado. Entre em contato com a administração."
                        self.page.snack_bar.bgcolor = ft.Colors.RED_400
                        self.page.snack_bar.open = True
                        self.page.update()
                    else:
                        self.page.snack_bar.content.value = "❗ Erro ao verificar status. Tente novamente mais tarde."
                        self.page.snack_bar.bgcolor = ft.Colors.RED_400
                        self.page.snack_bar.open = True
                        self.page.update()
                else:
                    self.page.snack_bar.content.value = "Email ou senha incorretos."
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
            else:
                self.page.snack_bar.content.value = "Preencha todos os campos."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()

        def registrar_click(e):
            nome = self.cadastro_nome.value.strip()
            email = self.cadastro_email.value.strip()
            cpf = self.cadastro_cpf.value.strip()
            nascimento = self.cadastro_nascimento.value.strip()
            telefone = self.cadastro_telefone.value.strip()
            senha = self.cadastro_senha.value.strip()
            confirmar_senha = self.cadastro_confirmar_senha.value.strip()

            if not all([nome, email, cpf, nascimento, telefone, senha, confirmar_senha]):
                self.page.snack_bar.content.value = "Preencha todos os campos."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return

            if senha != confirmar_senha:
                self.page.snack_bar.content.value = "As senhas não coincidem."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return

            # 🔍 Verifica duplicatas
            import sqlite3
            conn = sqlite3.connect("farmconnect.db")
            cursor = conn.cursor()
            cursor.execute("SELECT email, cpf, telefone FROM usuarios")
            usuarios = cursor.fetchall()
            conn.close()

            for u in usuarios:
                if email == u[0]:
                    self.page.snack_bar.content.value = "Email já cadastrado."
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                if cpf == u[1]:
                    self.page.snack_bar.content.value = "CPF já cadastrado."
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                if telefone == u[2]:
                    self.page.snack_bar.content.value = "Telefone já cadastrado."
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
                    return

            # ✅ Cadastro
            sucesso = registrar_usuario(nome, email, cpf, nascimento, telefone, senha)
            if sucesso:
                self.page.snack_bar.content.value = "Cadastro realizado com sucesso!"
                self.page.snack_bar.bgcolor = ft.Colors.GREEN
                self.page.snack_bar.open = True

                self.cadastro_nome.value = ""
                self.cadastro_email.value = ""
                self.cadastro_cpf.value = ""
                self.cadastro_nascimento.value = ""
                self.cadastro_telefone.value = ""
                self.cadastro_senha.value = ""
                self.cadastro_confirmar_senha.value = ""
                self.page.update()

                self.page.go("/login_usuario")
            else:
                self.page.snack_bar.content.value = "Erro ao cadastrar. Tente novamente."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()

        header = ft.Container(
            content=ft.Row([
                ft.Image(src="administrador/img_adm/logo.png", width=120, height=80),
                ft.Text("FarmConnect Usuário", size=20, weight="bold", color=ft.Colors.BLUE_900)
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
                self.cadastro_cpf,
                self.cadastro_nascimento,
                self.cadastro_telefone,
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
                ft.Text("FarmConnect Usuário", size=18, weight=ft.FontWeight.BOLD, color="white"),
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
            route="/login_usuario",
            scroll=ft.ScrollMode.AUTO,
            bgcolor=ft.Colors.WHITE,
            controls=[
                self.page.snack_bar,
                ft.Column([header, cards_section, footer], spacing=0, expand=True)
            ]
        )

if __name__ == "__main__":
    def main(page: ft.Page):
        tela_usuario = TelaLoginUsuario(page)
        page.views.append(tela_usuario.build_tela())
        page.update()

    ft.app(target=main)
