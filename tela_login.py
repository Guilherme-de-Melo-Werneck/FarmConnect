import flet as ft

def tela_login(page: ft.Page):
    def login_click(e):
        # Simula login (aqui você pode validar com banco depois)
        if email.value.strip() and senha.value.strip():
            page.go("/tela_usuario")
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
                expand=True,
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
                    ]
                )
            )
        ]
    )
