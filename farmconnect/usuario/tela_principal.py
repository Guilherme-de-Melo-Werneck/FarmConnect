import flet as ft

# Lista completa de medicamentos com dados diferentes
medicamentos_mock = [
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Rituximabe", "imagem": "/images/remedio2.png", "descricao": "Imunossupressor"},
    {"nome": "Rituximabe", "imagem": "/images/remedio2.png", "descricao": "Imunossupressor"},
    {"nome": "Etanercepte", "imagem": "/images/remedio3.png", "descricao": "Artrite reumatoide"},
    {"nome": "Adalimumabe", "imagem": "/images/remedio4.png", "descricao": "Inflamações crônicas"},
    {"nome": "Tocilizumabe", "imagem": "/images/remedio5.png", "descricao": "Uso hospitalar"},
    {"nome": "Somatropina", "imagem": "/images/remedio6.png", "descricao": "Deficiência de crescimento"},
    {"nome": "Bevacizumabe", "imagem": "/images/remedio7.png", "descricao": "Tratamento oncológico"},
    {"nome": "Trastuzumabe", "imagem": "/images/remedio8.png", "descricao": "Câncer de mama"},
    {"nome": "Infliximabe", "imagem": "/images/remedio9.png", "descricao": "Doença de Crohn"},
    {"nome": "Lenalidomida", "imagem": "/images/remedio10.png", "descricao": "Mieloma múltiplo"},
    {"nome": "Imatinibe", "imagem": "/images/remedio11.png", "descricao": "Leucemia mieloide crônica"},
    {"nome": "Eculizumabe", "imagem": "/images/remedio12.png", "descricao": "Síndromes raras"},
    {"nome": "Nusinersen", "imagem": "/images/remedio13.png", "descricao": "Atrofia muscular espinhal"},
    {"nome": "Canakinumabe", "imagem": "/images/remedio14.png", "descricao": "Inflamações genéticas"},
    {"nome": "Fingolimode", "imagem": "/images/remedio15.png", "descricao": "Esclerose múltipla"},
    {"nome": "Everolimo", "imagem": "/images/remedio16.png", "descricao": "Antineoplásico"},
    {"nome": "Belimumabe", "imagem": "/images/remedio17.png", "descricao": "Lúpus eritematoso"},
    {"nome": "Cerliponase Alfa", "imagem": "/images/remedio18.png", "descricao": "Lipofuscinose ceroid"},
    {"nome": "Vimizim", "imagem": "/images/remedio19.png", "descricao": "Síndrome de Morquio"},
    {"nome": "Spinraza", "imagem": "/images/remedio20.png", "descricao": "Atrofia muscular"},
    {"nome": "Zolgensma", "imagem": "/images/remedio21.png", "descricao": "Terapia gênica"},
    {"nome": "Onasemnogene", "imagem": "/images/remedio22.png", "descricao": "Trata mutações genéticas"},
    {"nome": "Alglucosidase Alfa", "imagem": "/images/remedio23.png", "descricao": "Doença de Pompe"},
    {"nome": "Cerdelga", "imagem": "/images/remedio24.png", "descricao": "Doença de Gaucher"},
]

medicamentos_por_pagina = 8

def tela_usuario(page: ft.Page):
    cards_container = ft.ResponsiveRow(run_spacing=20, spacing=20)
    pagina_atual = 1

    def gerar_cards(pagina):
        inicio = (pagina - 1) * medicamentos_por_pagina
        fim = inicio + medicamentos_por_pagina
        cards_container.controls.clear()
        for med in medicamentos_mock[inicio:fim]:
            cards_container.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=16,
                    bgcolor="#F8FAFC",
                    border_radius=16,
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    content=ft.Column([
                        ft.Image(src=med["imagem"], width=100, height=100),
                        ft.Text(
                            med["nome"],
                            text_align=ft.TextAlign.CENTER,
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color="#111827",
                        ),
                        ft.Text(
                            med["descricao"],
                            size=11,
                            text_align=ft.TextAlign.CENTER,
                            color="#111827",
                        ),
                        ft.ElevatedButton(
                            "ADICIONAR",
                            width=130,
                            bgcolor=ft.Colors.BLUE_900,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        )
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )
        page.update()

    def mudar_pagina(e):
        nonlocal pagina_atual
        pagina_atual = int(e.control.text)
        gerar_cards(pagina_atual)

    botoes_paginacao = ft.Row(
        controls=[
            ft.ElevatedButton(str(i), on_click=mudar_pagina)
            for i in range(1, (len(medicamentos_mock) // medicamentos_por_pagina) + 1)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    gerar_cards(pagina_atual)

    return ft.View(
        route="/usuario",
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#EFF6FF", "#DBEAFE"]
                ),
                content=ft.ResponsiveRow([
                    # SIDEBAR
                    ft.Container(
                        width=260,
                        padding=20,
                        bgcolor=ft.Colors.BLUE_600,
                        border_radius=16,
                        col={"xs": 12, "md": 3, "lg": 2},
                        content=ft.Column([
                            ft.Image(src="logo.png", width=120, height=40),
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            *[
                                ft.ElevatedButton(
                                    text,
                                    width=220,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.WHITE,
                                        color="#111827",
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        padding=ft.padding.symmetric(vertical=12),
                                    )
                                ) for text in [
                                    "Ver Perfil", "Medicamentos Retirados", "Agendamentos",
                                    "Documentos Necessários", "Editar Dados"
                                ]
                            ],
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                "Sair",
                                width=220,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.RED_400,
                                    color=ft.colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(vertical=12),
                                ),
                                on_click=lambda e: page.go("/")
                            ),
                        ], spacing=16, alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),

                    # CONTEÚDO PRINCIPAL COM SCROLL
                    ft.Container(
                        expand=True,
                        padding=20,
                        col={"xs": 12, "md": 9, "lg": 10},
                        content=ft.Column(
                            scroll=ft.ScrollMode.ADAPTIVE,
                            controls=[
                                # TOPO
                                ft.Container(
                                    bgcolor=ft.Colors.BLUE_600,
                                    border_radius=16,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=18),
                                    shadow=ft.BoxShadow(blur_radius=12, color=ft.colors.BLACK12, offset=ft.Offset(0, 3)),
                                    content=ft.ResponsiveRow([
                                        ft.Image(src="logo.png", width=110, col={"xs": 12, "md": 2}),
                                        ft.TextField(
                                            hint_text="Buscar medicamentos...",
                                            prefix_icon=ft.icons.SEARCH,
                                            border_radius=12,
                                            bgcolor=ft.colors.WHITE,
                                            height=45,
                                            col={"xs": 12, "md": 6}
                                        ),
                                        ft.Row([
                                            ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                                            ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                        ], spacing=10, alignment=ft.MainAxisAlignment.END, col={"xs": 12, "md": 4})
                                    ])
                                ),

                                # CONTEÚDO DOS MEDICAMENTOS
                                ft.Container(
                                    alignment=ft.alignment.top_center,
                                    padding=30,
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Text(
                                                "MEDICAMENTOS DISPONÍVEIS",
                                                size=24,
                                                weight=ft.FontWeight.W_600,
                                                color="#111827",
                                            )
                                        ], alignment=ft.MainAxisAlignment.CENTER),

                                        ft.Row([
                                            ft.OutlinedButton(
                                                "Mais Buscados",
                                                style=ft.ButtonStyle(
                                                    color="#111827",
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                                )
                                            ),
                                            ft.OutlinedButton(
                                                "Meus Agendamentos",
                                                style=ft.ButtonStyle(
                                                    color="#111827",
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                                )
                                            ),
                                            ft.OutlinedButton(
                                                "Feedback",
                                                style=ft.ButtonStyle(
                                                    color="#111827",
                                                    shape=ft.RoundedRectangleBorder(radius=8),
                                                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                                                )
                                            ),
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                                        
                                        ft.Divider(height=25),
                                        cards_container,
                                        ft.Divider(height=30),
                                        botoes_paginacao
                                    ], spacing=30)
                                )
                            ],
                            spacing=20
                        )
                    )
                ])
            )
        ]
    )

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.bgcolor = "#EFF6FF"
    page.scroll = ft.ScrollMode.ADAPTIVE

    def route_change(route):
        page.views.clear()
        if page.route == "/usuario":
            page.views.append(tela_usuario(page))
        page.update()

    page.on_route_change = route_change
    page.go("/usuario")

ft.app(target=main)


