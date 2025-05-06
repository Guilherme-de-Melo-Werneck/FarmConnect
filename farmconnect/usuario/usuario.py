import flet as ft
import asyncio

# ---------------------- Funções de validação e formatação ----------------------
def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    def calc_digito(cpf, peso):
        soma = sum(int(cpf[i]) * (peso - i) for i in range(peso - 1))
        resto = (soma * 10) % 11
        return 0 if resto == 10 else resto
    d1 = calc_digito(cpf, 10)
    d2 = calc_digito(cpf[:9] + str(d1), 11)
    return cpf[-2:] == f"{d1}{d2}"

def formatar_cpf(texto: str) -> str:
    numeros = ''.join(filter(str.isdigit, texto))[:11]
    if len(numeros) <= 3:
        return numeros
    elif len(numeros) <= 6:
        return f"{numeros[:3]}.{numeros[3:]}"
    elif len(numeros) <= 9:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}"
    else:
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

def formatar_data_nascimento(texto: str) -> str:
    numeros = ''.join(filter(str.isdigit, texto))[:8]
    if not numeros:
        return ""
    partes = []
    if len(numeros) >= 2:
        dia = min(max(int(numeros[:2]), 1), 31)
        partes.append(f"{dia:02d}")
    elif len(numeros) > 0:
        partes.append(numeros[:2])

    if len(numeros) >= 4:
        mes = min(max(int(numeros[2:4]), 1), 12)
        partes.append(f"{mes:02d}")
    elif len(numeros) > 2:
        partes.append(numeros[2:4])

    if len(numeros) > 4:
        partes.append(numeros[4:])

    return "/".join(partes)

# ---------------------- App ----------------------
def main(page: ft.Page):
    page.title = "FarmConnect - Usuário"
    page.bgcolor = "#E0F2FE"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0

    page.snack_bar = ft.SnackBar(content=ft.Text(""), bgcolor=ft.colors.RED_400, duration=3000)

    def cpf_change(e):
        valor_formatado = formatar_cpf(cadastro_cpf.value)
        if cadastro_cpf.value != valor_formatado:
            cadastro_cpf.value = valor_formatado
            cadastro_cpf.update()

    def nascimento_change(e):
        valor_formatado = formatar_data_nascimento(cadastro_nascimento.value)
        if cadastro_nascimento.value != valor_formatado:
            cadastro_nascimento.value = valor_formatado
            cadastro_nascimento.update()

    login_email = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50)
    login_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50)

    cadastro_nome = ft.TextField(label="Nome completo", prefix_icon=ft.icons.PERSON, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50)
    cadastro_email = ft.TextField(label="Email", prefix_icon=ft.icons.EMAIL, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50)
    cadastro_cpf = ft.TextField(label="CPF", prefix_icon=ft.icons.BADGE, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50, keyboard_type=ft.KeyboardType.NUMBER, on_change=cpf_change)
    cadastro_nascimento = ft.TextField(label="Data de nascimento", hint_text="DD/MM/AAAA", prefix_icon=ft.icons.CALENDAR_MONTH, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50, on_change=nascimento_change)
    cadastro_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50)
    cadastro_confirmar_senha = ft.TextField(label="Confirmar senha", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK_OUTLINE, border_radius=10, filled=True, bgcolor=ft.colors.BLUE_50)

    def login_click(e):
        if login_email.value.strip() and login_senha.value.strip():
            page.go("/usuario_dashboard")
        else:
            page.snack_bar.content.value = "Preencha todos os campos do login."
            page.snack_bar.open = True
            page.update()

    def registrar_click(e):
        campos = [cadastro_nome, cadastro_email, cadastro_cpf, cadastro_nascimento, cadastro_senha, cadastro_confirmar_senha]
        if all(c.value.strip() for c in campos):
            if not validar_cpf(cadastro_cpf.value):
                page.snack_bar.content.value = "CPF inválido."
                page.snack_bar.bgcolor = ft.colors.RED_400
            elif cadastro_senha.value != cadastro_confirmar_senha.value:
                page.snack_bar.content.value = "As senhas não coincidem."
                page.snack_bar.bgcolor = ft.colors.RED_400
            else:
                page.snack_bar.content.value = "Cadastro realizado com sucesso!"
                page.snack_bar.bgcolor = ft.colors.GREEN
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar.content.value = "Preencha todos os campos do cadastro."
            page.snack_bar.open = True
            page.update()

    login_card = ft.Container(
        padding=30,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 6)),
        content=ft.Column([
            ft.Text("Login", size=24, weight="bold", color="#1E3A8A"),
            login_email,
            login_senha,
            ft.ElevatedButton("Entrar", bgcolor="#1E3A8A", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=login_click),
        ], spacing=20)
    )

    cadastro_card = ft.Container(
        padding=30,
        bgcolor="white",
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 6)),
        content=ft.Column([
            ft.Text("Cadastro", size=24, weight="bold", color="#1E3A8A"),
            cadastro_nome,
            cadastro_email,
            cadastro_cpf,
            cadastro_nascimento,
            cadastro_senha,
            cadastro_confirmar_senha,
            ft.ElevatedButton("Registrar", bgcolor="#1E3A8A", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=registrar_click)
        ], spacing=16)
    )

    cards = ft.Container(
        expand=True,
        padding=20,
        content=ft.ResponsiveRow(
            columns=12,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(col={"sm": 12, "md": 6}, content=login_card),
                ft.Container(col={"sm": 12, "md": 6}, content=cadastro_card),
            ],
            spacing=40,
            run_spacing=30
        )
    )

    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.LOCAL_HOSPITAL, color="white", size=30),
            ft.Text("FarmConnect Usuário", size=20, weight="bold", color=ft.colors.WHITE)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=40, vertical=24),
        bgcolor="#1E3A8A",
        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK38, offset=ft.Offset(0, 8))
    )

    footer = ft.Container(
        bgcolor="#1E3A8A",
        padding=10,
        content=ft.Column(
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("FarmConnect", size=16, weight="bold", color="white"),
                ft.Text("Facilitando sua saúde pública", size=12, color=ft.colors.WHITE70),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        ft.IconButton(icon=ft.icons.HOME, icon_color="white", tooltip="Início"),
                        ft.IconButton(icon=ft.icons.HELP_OUTLINE, icon_color="white", tooltip="Ajuda"),
                        ft.IconButton(icon=ft.icons.EMAIL, icon_color="white", tooltip="Contato"),
                    ]
                ),
            ]
        ),
        shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.BLACK26, offset=ft.Offset(0, -4))
    )

    def route_change(route):
        page.views.clear()
        if page.route == "/login_usuario":
            page.views.append(ft.View(route="/login_usuario", scroll=ft.ScrollMode.AUTO, controls=[page.snack_bar, ft.Column([header, cards, footer], expand=True)]))
        elif page.route == "/usuario_dashboard":
            page.views.append(ft.View(route="/usuario_dashboard", controls=[ft.Container(content=ft.Text("Bem-vindo ao painel do usuário!", size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center, expand=True)]))
        page.update()

    page.on_route_change = route_change
    page.go("/login_usuario")

ft.app(target=main)