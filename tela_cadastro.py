import flet as ft

def tela_cadastro(page: ft.Page):
    def registrar_click(e):
        # Aqui pode adicionar validações mais tarde
        page.go("/tela_usuario")

    def cancelar_click(e):
        page.go("/")  # Redireciona para a página inicial

    return ft.View(
        route="/cadastro",
        controls=[
            ft.Container(
                bgcolor=ft.colors.GREEN_700,
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=900,
                    content=ft.Row([
                        ft.Container(
                            padding=30,
                            width=500,
                            content=ft.Column([
                                ft.Text("CRIE SUA CONTA", size=25, weight=ft.FontWeight.BOLD),
                                ft.TextField(label="Nome completo*", width=400),
                                ft.TextField(label="CPF*", width=400),
                                ft.TextField(label="E-mail*", width=400),
                                ft.TextField(label="Verificar E-mail*", width=400),
                                ft.TextField(label="Senha*", password=True, can_reveal_password=True, width=400),
                                ft.TextField(label="Confirmar Senha*", password=True, can_reveal_password=True, width=400),
                                ft.Row([
                                    ft.ElevatedButton("CANCELAR", on_click=cancelar_click),
                                    ft.ElevatedButton("REGISTRAR", on_click=registrar_click),
                                ], spacing=20)
                            ], spacing=20)
                        ),
                        ft.VerticalDivider(width=1, color=ft.colors.WHITE54),
                        ft.Container(
                            expand=True,
                            content=ft.Image(src="/images/register_banner.png", fit=ft.ImageFit.CONTAIN)
                        )
                    ])
                )
            )
        ]
    )
