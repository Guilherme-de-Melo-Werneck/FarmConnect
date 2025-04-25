import flet as ft

def main(page: ft.Page):
    page.title = "InfoSysHub - Apresentação"
    page.bgcolor = "#E8F0FE"
    page.scroll = ft.ScrollMode.AUTO

    # Header
    header = ft.Row(
        [
            ft.Text("InfoSysHub", size=32, weight=ft.FontWeight.BOLD, color="#1A237E"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Subtítulo e descrição
    description = ft.Text(
        "Gerencie com facilidade os dados e relatórios do seu sistema de informação em uma única plataforma integrada.",
        size=18,
        text_align=ft.TextAlign.CENTER,
        color="#37474F",
    )

    # Campo de sugestão
    suggestion_input = ft.TextField(
        hint_text="Digite sua sugestão...",
        prefix_icon=ft.icons.SEARCH,
        expand=True,
        bgcolor="#ffffff",
        border_radius=10,
    )

    send_button = ft.ElevatedButton(
        text="Enviar", color="white", bgcolor="#1A237E"
    )

    suggestion_row = ft.Row(
        [suggestion_input, send_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Imagem ilustrativa de dispositivos
    illustration = ft.Image(
        src="https://cdn.pixabay.com/photo/2017/01/31/13/14/web-2025788_960_720.png",
        width=600,
        fit=ft.ImageFit.CONTAIN,
    )

    # Rodapé com ícones de redes sociais usando imagens
    footer = ft.Row(
        [
            ft.Text("Siga-nos nas redes sociais:", size=14),
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png", width=24, height=24),  # Instagram
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733547.png", width=24, height=24),  # Facebook
            ft.Image(src="https://cdn-icons-png.flaticon.com/512/733/733585.png", width=24, height=24),  # WhatsApp
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Organiza tudo na página
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    header,
                    description,
                    ft.Divider(height=10, color="transparent"),
                    suggestion_row,
                    ft.Divider(height=30, color="transparent"),
                    illustration,
                    ft.Divider(height=30, color="transparent"),
                    footer,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main)
