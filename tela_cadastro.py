import flet as ft

def tela_cadastro(page: ft.Page):
    def registrar_click(e):
        # Aqui pode adicionar validações mais tarde
        page.go("/tela_usuario")

    def cancelar_click(e):
        page.go("/")

    return ft.View(
        route="/tela_cadastro",
        controls=[
            ft.Container(
                bgcolor=ft.colors.GREEN_700,
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    width=950,  # largura fixa para centralizar o conteúdo
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                padding=30,
                                width=450,
                                content=ft.Column([
                                    ft.Text("CRIE SUA CONTA", size=25, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                    ft.TextField(label="Nome completo*", width=400),
                                    ft.TextField(label="CPF*", width=400),
                                    ft.TextField(label="E-mail*", width=400),
                                    ft.TextField(label="Verificar E-mail*", width=400),
                                    ft.TextField(label="Senha*", password=True, can_reveal_password=True, width=400),
                                    ft.TextField(label="Confirmar Senha*", password=True, can_reveal_password=True, width=400),
                                    ft.Row([
                                        ft.ElevatedButton("CANCELAR"),
                                        ft.ElevatedButton("REGISTRAR", on_click=registrar_click),
                                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
                                ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
                            ),
                            ft.Container(
                                width=400,
                                content=ft.Image(src="/images/register_banner.png", fit=ft.ImageFit.CONTAIN)
                            )
                        ]
                    )
                )
            )
        ]
    )
