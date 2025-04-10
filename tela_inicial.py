import flet as ft

class FarmConnectApp(ft.Column):
    def __init__(self, on_login, on_register):
        super().__init__()

        self.header = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Image(src="logo.png", width=50, height=50),
                        ft.Text("FarmConnect", size=30, weight=ft.FontWeight.BOLD, color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("Sobre"),
                        ft.TextButton("Ajuda"),
                        ft.TextButton("Contato"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.TextButton("Entrar", on_click=on_login),
                        ft.TextButton("Registrar", on_click=on_register),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Facilitar seus agendamentos e busca para medicamentos especializados",
                    size=18,
                    color="white",
                ),
                ft.Row(
                    controls=[
                        ft.TextField(label="Digite um medicamento", expand=True),
                        ft.ElevatedButton("Enviar", bgcolor="#4CAF50", color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.footer = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Siga-nos: "),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.bottom_center,
            padding=10,
        )

        self.controls = [self.header, self.content, self.footer]
        self.expand = True


class LoginScreen(ft.Column):
    def __init__(self, on_success_login, on_back):
        super().__init__()
        self.controls = [
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Usuário"),
            ft.TextField(label="Senha", password=True),
            ft.ElevatedButton("Entrar", on_click=on_success_login),
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True


class RegisterScreen(ft.Column):
    def __init__(self, on_back):
        super().__init__()
        self.controls = [
            ft.Row([
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=on_back),
            ], alignment=ft.MainAxisAlignment.START),
            ft.Text("Cadastro", size=24, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Nome"),
            ft.TextField(label="Email"),
            ft.TextField(label="Senha", password=True),
            ft.ElevatedButton("Registrar", on_click=on_back),  # Simula login para simplificar
        ]
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True
