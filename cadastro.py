import flet as ft

def main(page: ft.Page):
    page.title = "FarmConnect - Cadastro"
    page.bgcolor = "#7B8CFF"
    page.scroll = ft.ScrollMode.AUTO

    # Botões no topo
    top_buttons = ft.Row([
        ft.ElevatedButton("Registrar", bgcolor="#ffffff", color="green", width=100),
        ft.ElevatedButton("Entrar", bgcolor="#ffffff", color="green", width=100),
    ], alignment=ft.MainAxisAlignment.END)

    # Formulário
    form = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.TextField(label="Nome Completo *", width=400),
                ft.TextField(label="Endereço", width=400),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.TextField(label="CPF *", width=400),
                ft.TextField(label="Telefone *", width=400),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.TextField(label="E-mail *", width=400),
                ft.TextField(label="Verificar E-mail *", width=400),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.TextField(label="Senha (para futuras compras) *", password=True, width=400),
                ft.TextField(label="Confirmar Senha *", password=True, width=400),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("* Campos Obrigatórios", size=10, color="red")
        ], spacing=15),
        padding=20,
        bgcolor="white",
        border_radius=10,
        margin=20
    )

    # Botões CADASTRAR e CANCELAR
    form_buttons = ft.Row([
        ft.ElevatedButton("CADASTRAR", bgcolor="white", color="black", width=150),
        ft.ElevatedButton("CANCELAR", bgcolor="white", color="black", width=150),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=50)

    # Rodapé com imagens e redes sociais
    footer = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Image(src="https://i.ibb.co/nb1GjNF/site-blindado.png", width=120),
                ft.Image(src="https://i.ibb.co/yR9VZzt/google-safe.png", width=120),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=40),
            ft.Text("Siga-nos", size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Row([
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png", width=30),  # Instagram
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733547.png", width=30),  # Facebook
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733585.png", width=30),  # WhatsApp
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        padding=20
    )

    page.add(top_buttons, form, form_buttons, footer)

ft.app(target=main)