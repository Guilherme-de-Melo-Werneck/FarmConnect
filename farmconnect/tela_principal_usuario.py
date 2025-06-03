import flet as ft


# Lista completa de medicamentos com dados diferentes
medicamentos_mock = [
    {"nome": "Interferon Alfa", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Teriflunomida 14 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Betainterferona 1A 12.000.000 UI", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Clozapina 100 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Donepezila 5 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Everolimo 0,75 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Gabapentina 300 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Leuprorrelina 45 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Memantina 10 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Miglustate 100 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Olanzapina 10 mg", "imagem": "/images/remedio.png", "descricao": "Tratamento de hepatite"},
    {"nome": "Pramipexol 0,25 mg", "imagem": "/images/remedio2.png", "descricao": "Imunossupressor"},
    {"nome": "Quetiapina 200 mg", "imagem": "/images/remedio2.png", "descricao": "Imunossupressor"},
    {"nome": "Sapropterina 100 mg", "imagem": "/images/remedio3.png", "descricao": "Artrite reumatoide"},
    {"nome": "Selegilina 5 mg", "imagem": "/images/remedio4.png", "descricao": "Inflamações crônicas"},
    {"nome": "Ziprasidona 40 mg", "imagem": "/images/remedio5.png", "descricao": "Uso hospitalar"},
]

medicamentos_por_pagina = 8

def tela_usuario(page: ft.Page):
    cards_container = ft.ResponsiveRow(run_spacing=20, spacing=20)
    pagina_atual = 1
    carrinho_count = ft.Ref[ft.Text]()

    contador = {"valor": 0}

    def adicionar_ao_carrinho(e):
        contador["valor"] += 1
        carrinho_count.current.value = str(contador["valor"])
        carrinho_count.current.visible = True
        carrinho_count.current.update()

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
                        ft.Text(med["nome"], text_align=ft.TextAlign.CENTER, size=13, weight=ft.FontWeight.BOLD, color="#111827"),
                        ft.Text(med["descricao"], size=11, text_align=ft.TextAlign.CENTER, color="#111827"),
                        ft.ElevatedButton(
                            "ADICIONAR",
                            width=130,
                            bgcolor=ft.Colors.BLUE_900,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=adicionar_ao_carrinho
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

    def icone_carrinho():
        return ft.Stack([
            ft.Icon(name=ft.icons.SHOPPING_BAG_OUTLINED, size=30, color="#1E3A8A"),
            ft.Container(
                ref=carrinho_count,
                content=ft.Text("0", size=10, color=ft.colors.WHITE),
                width=16,
                height=16,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.RED,
                border_radius=8,
                right=0,
                top=0,
                visible=False
            )
        ])

    def create_menu_item(icon, text, route):
        container = ft.Container(
            padding=ft.padding.symmetric(vertical=12, horizontal=10),
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.BLUE_600, size=24),
                ft.Text(text, size=16, color="#111827")
            ], spacing=15, alignment=ft.MainAxisAlignment.START),
            ink=True,
            border_radius=8,
            bgcolor="#FFFFFF",
            on_click=lambda e: page.go(route),
            animate=ft.Animation(200, "easeInOut"),
            margin=ft.margin.only(bottom=8)
        )

        def on_hover(e):
            container.bgcolor = "#d1eefa" if e.data == "true" else "#FFFFFF"
            container.update()

        container.on_hover = on_hover
        return container

    sidebar = ft.Container(
        width=280,
        bgcolor="#F9FAFB",
        border=ft.border.only(right=ft.BorderSide(1, "#E5E7EB")),
        padding=ft.padding.symmetric(vertical=20, horizontal=10),
        content=ft.Column([
            ft.Container(
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=10),
                content=ft.Image(src="logo.png", width=120, height=40)
            ),
            ft.Divider(thickness=1),
            create_menu_item(ft.Icons.PERSON_OUTLINED, "Meu Perfil", "/perfil"),
            create_menu_item(ft.Icons.MEDICAL_SERVICES_OUTLINED, "Histórico de Retiradas", "/medicamentos_retirados"),
            create_menu_item(ft.Icons.CALENDAR_MONTH_OUTLINED, "Meus Agendamentos", "/agendamentos"),
            create_menu_item(ft.Icons.DESCRIPTION_OUTLINED, "Documentos Requeridos", "/documentos"),
            ft.Container(expand=True),
            ft.Container(
                padding=ft.padding.symmetric(vertical=12, horizontal=10),
                content=ft.Row([
                    ft.Icon(ft.Icons.LOGOUT, color="#DC2626", size=24),
                    ft.Text("Sair", size=16, color="#DC2626"),
                ], spacing=15, alignment=ft.MainAxisAlignment.START),
                border_radius=8,
                bgcolor="#FEE2E2",
                ink=True,
                on_click=lambda e: page.go("/"),
                animate=ft.Animation(200, "easeInOut")
            )
        ], spacing=10, expand=True)
    )

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
                content=ft.Row([
                    sidebar,
                    ft.Container(
                        expand=True,
                        padding=20,
                        content=ft.Column([
                            ft.Container(
                                bgcolor="#F8FAFC",
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
                                        icone_carrinho(),
                                        ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                                        ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                                    ], spacing=10, alignment=ft.MainAxisAlignment.END, col={"xs": 12, "md": 4})
                                ])
                            ),
                            ft.Container(
                                alignment=ft.alignment.top_center,
                                padding=30,
                                content=ft.Column([
                                    ft.Text("MEDICAMENTOS DISPONÍVEIS", size=24, weight=ft.FontWeight.W_600, color="#111827"),
                                    ft.Row([
                                        ft.OutlinedButton("Mais Buscados"),
                                        ft.OutlinedButton("Meus Agendamentos"),
                                        ft.OutlinedButton("Feedback"),
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                                    ft.Divider(height=25),
                                    cards_container,
                                    ft.Divider(height=30),
                                    botoes_paginacao
                                ], spacing=30)
                            )
                        ], scroll=ft.ScrollMode.ADAPTIVE, spacing=20)
                    )
                ])
            )
        ]
    )



def tela_documentos(page: ft.Page):
    return ft.View(
        route="/documentos",
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#EFF6FF", "#DBEAFE"]
                ),
                padding=40,
                content=ft.Column([
                    # Título da Página
                    ft.Text(
                        "📄 DOCUMENTOS NECESSÁRIOS", 
                        size=30, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.BLUE_900,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    # Caixa de Documentos
                    ft.Container(
                        padding=30,
                        bgcolor=ft.colors.WHITE,
                        border_radius=20,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 10)),
                        content=ft.Column([
                            ft.Text(
                                "Para retirar medicamentos é necessário apresentar:",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900
                            ),
                            ft.Text(
                                "1. Documento com foto (RG, CNH, Passaporte)\n"
                                "2. Receita médica válida por até 3 meses\n\n"
                                "Se for um terceiro retirando o medicamento, é necessário:\n"
                                "- Documento com foto do responsável\n"
                                "- Documento com foto do paciente\n"
                                "- Autorização assinada pelo responsável.",
                                size=18,
                                color=ft.Colors.GREY_700,
                                selectable=True
                            ),
                        ], spacing=10)
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    # Botões de Ação
                    ft.Row([
                        ft.ElevatedButton(
                            "Baixar Documento de Autorização",
                            icon=ft.icons.FILE_DOWNLOAD,
                            bgcolor=ft.Colors.BLUE_900,
                            color=ft.colors.WHITE,
                            width=250,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.padding.symmetric(vertical=12)
                            ),
                            on_click=lambda e: print("Documento baixado")
                        ),
                        ft.ElevatedButton(
                            "Voltar",
                            icon=ft.icons.ARROW_BACK_IOS_NEW,
                            bgcolor=ft.Colors.GREY_500,
                            color=ft.colors.WHITE,
                            width=150,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.padding.symmetric(vertical=12)
                            ),
                            on_click=lambda e: page.go("/usuario")
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        ]
    )

import flet as ft

def tela_perfil_paciente(page: ft.Page):
    # Refs
    editando_nome = ft.Ref[bool]()
    editando_cpf = ft.Ref[bool]()
    editando_nasc = ft.Ref[bool]()
    editando_email = ft.Ref[bool]()
    editando_tel = ft.Ref[bool]()

    nome_field = ft.Ref[ft.TextField]()
    cpf_field = ft.Ref[ft.TextField]()
    nasc_field = ft.Ref[ft.TextField]()
    email_field = ft.Ref[ft.TextField]()
    tel_field = ft.Ref[ft.TextField]()

    # Inicializa edição como falso
    editando_nome.current = False
    editando_cpf.current = False
    editando_nasc.current = False
    editando_email.current = False
    editando_tel.current = False

    # Dados simulados
    dados_usuario = {
        "nome": "João Nascimento",
        "cpf": "123.456.789-00",
        "nasc": "01/01/1990",
        "email": "joao@gmail.com",
        "tel": "(11) 98765-4321"
    }

    # Alternar edição e focar
    def iniciar_edicao(ref_bool, input_ref):
        ref_bool.current = True
        page.update()
        input_ref.current.focus()

    # Salvar valor
    def salvar(ref_bool, campo, input_ref):
        dados_usuario[campo] = input_ref.current.value
        ref_bool.current = False
        page.snack_bar = ft.SnackBar(ft.Text(f"{campo.capitalize()} atualizado com sucesso!"), bgcolor=ft.colors.GREEN_100)
        page.snack_bar.open = True
        page.update()

    # Campo editável
    def campo_editavel(label, campo, ref_bool, input_ref):
        return ft.Column(
            spacing=2,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(label, size=16, color=ft.Colors.GREY_700),
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_color=ft.colors.BLUE,
                            tooltip="Editar",
                            on_click=lambda e: iniciar_edicao(ref_bool, input_ref)
                        )
                    ]
                ),
                ft.TextField(
                    ref=input_ref,
                    value=dados_usuario[campo],
                    read_only=not ref_bool.current,
                    filled=True,
                    dense=True,
                    border_radius=12,
                    content_padding=10,
                    text_size=16,
                    on_submit=lambda e: salvar(ref_bool, campo, input_ref)
                )
            ]
        )

    return ft.View(
        route="/perfil",
        controls=[
            ft.Container(
                expand=True,
                padding=30,
                alignment=ft.alignment.center,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#E0F2FE", "#F0F4FF"]
                ),
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        ft.Text("Perfil do Paciente", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.Container(
                            width=700,
                            padding=25,
                            bgcolor=ft.colors.WHITE,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=24, color=ft.colors.BLACK12, offset=ft.Offset(0, 12)),
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=30,
                                controls=[
                                    ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=10,
                                        controls=[
                                            ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=60),
                                            ft.Text(dados_usuario["nome"], size=24, weight=ft.FontWeight.BOLD),
                                            ft.Text("Paciente FarmConnect", size=16, color=ft.Colors.GREY_600)
                                        ]
                                    ),
                                    campo_editavel("Nome", "nome", editando_nome, nome_field),
                                    campo_editavel("CPF", "cpf", editando_cpf, cpf_field),
                                    campo_editavel("Data de Nascimento", "nasc", editando_nasc, nasc_field),
                                    campo_editavel("Email", "email", editando_email, email_field),
                                    campo_editavel("Telefone", "tel", editando_tel, tel_field),
                                ]
                            )
                        ),
                        ft.ElevatedButton(
                            "Voltar",
                            icon=ft.icons.ARROW_BACK,
                            bgcolor=ft.Colors.GREY_500,
                            color=ft.colors.WHITE,
                            width=160,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=16),
                                padding=ft.padding.symmetric(vertical=12),
                                elevation=4
                            ),
                            on_click=lambda e: page.go("/usuario")
                        )
                    ]
                )
            )
        ]
    )



# Lista simulada de medicamentos retirados
medicamentos_retirados_mock = [
    {"nome": "Interferon Alfa", "data_retirada": "10/05/2025", "quantidade": 2},
    {"nome": "Rituximabe", "data_retirada": "08/05/2025", "quantidade": 1},
    {"nome": "Adalimumabe", "data_retirada": "01/05/2025", "quantidade": 3},
    {"nome": "Trastuzumabe", "data_retirada": "28/04/2025", "quantidade": 1},
    {"nome": "Lenalidomida", "data_retirada": "25/04/2025", "quantidade": 2},
]

def tela_medicamentos_retirados(page: ft.Page):
    return ft.View(
        route="/medicamentos_retirados",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                padding=40,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#E0F2FE", "#F0F4FF"]
                ),
                content=ft.Column([
                    ft.Text(
                        "💊 MEDICAMENTOS RETIRADOS", 
                        size=32, 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.Colors.BLUE_900    ,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Container(
                        padding=30,
                        bgcolor="#FFFFFF",
                        border_radius=20,
                        shadow=ft.BoxShadow(blur_radius=30, color=ft.colors.BLACK12, offset=ft.Offset(0, 15)),
                        content=ft.Column([
                            ft.Row([
                                ft.TextField(label="🔍 Buscar Medicamento", expand=True, on_change=lambda e: print(e.control.value)),
                                ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.Colors.BLUE_900, on_click=lambda e: print("Buscar"))
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            ft.ListView(
                                expand=True,
                                controls=[
                                    ft.Container(
                                        padding=20,
                                        bgcolor="#F8FAFC",
                                        border_radius=16,
                                        margin=ft.margin.only(bottom=20),
                                        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12, offset=ft.Offset(0, 10)),
                                        content=ft.Column([
                                            ft.Text(med["nome"], size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                                            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                                            ft.Text(f"📅 Data de Retirada: {med['data_retirada']}", size=14, color="#374151"),
                                            ft.Text(f"📦 Quantidade: {med['quantidade']} unidades", size=14, color="#374151"),
                                            ft.ElevatedButton(
                                                "Ver Detalhes",
                                                icon=ft.icons.INFO_OUTLINE,
                                                bgcolor=ft.Colors.BLUE_900,
                                                color=ft.colors.WHITE,
                                                width=200,
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=12),
                                                    padding=ft.padding.symmetric(vertical=10)
                                                ),
                                                on_click=lambda e, med=med: print(f"Detalhes de {med['nome']}")
                                            )
                                        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                    )
                                    for med in medicamentos_retirados_mock
                                ]
                            )
                        ], spacing=20)
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    ft.ElevatedButton(
                        "Voltar",
                        icon=ft.icons.ARROW_BACK_IOS_NEW,
                        bgcolor=ft.Colors.GREY_500,
                        color=ft.colors.WHITE,
                        width=150,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.padding.symmetric(vertical=12)
                        ),
                        on_click=lambda e: page.go("/usuario")
                    )
                ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
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
        elif page.route == "/documentos":
            page.views.append(tela_documentos(page))
        elif page.route == "/perfil":
            page.views.append(tela_perfil_paciente(page))
        elif page.route == "/medicamentos_retirados":
            page.views.append(tela_medicamentos_retirados(page))
        page.update()



    page.on_route_change = route_change
    page.go("/usuario")

ft.app(target=main)


