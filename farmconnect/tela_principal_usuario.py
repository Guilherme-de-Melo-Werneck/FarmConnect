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
    medicamentos_por_pagina = 8
    cards_container = ft.ResponsiveRow(run_spacing=20, spacing=20)
    pagina_atual = 1
    carrinho_count = ft.Ref[ft.Text]()
    busca_ref = ft.Ref[ft.TextField]()
    contador = {"valor": 0}
    carrinho = []
    botoes_paginacao = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10)

    def remover_do_carrinho(e, item):
        carrinho.remove(item)
        contador["valor"] -= 1
        carrinho_count.current.value = str(contador["valor"])
        carrinho_count.current.update()
        abrir_carrinho(None)

    def adicionar_ao_carrinho(medicamento):
        contador["valor"] += 1
        carrinho_count.current.value = str(contador["valor"])
        carrinho_count.current.update()
        carrinho.append(medicamento)
        page.update()

    def abrir_detalhes_medicamento(e, med):
        page.client_storage.set("medicamento_detalhe", med)
        page.go("/detalhes_medicamento")

    def abrir_carrinho(e):
        itens_coluna = carrinho_drawer.content.controls[2]
        itens_coluna.controls.clear()
        for item in carrinho:
            itens_coluna.controls.append(
                ft.Container(
                    padding=10,
                    bgcolor="#FFFFFF",
                    border_radius=8,
                    content=ft.Row([
                        ft.Text(item["nome"], size=12, expand=True),
                        ft.IconButton(icon=ft.icons.DELETE_OUTLINE, icon_color=ft.colors.RED, tooltip="Remover", on_click=lambda e, med=item: remover_do_carrinho(e, med))
                    ])
                )
            )
        carrinho_drawer.visible = True
        page.update()

    def fechar_carrinho():
        carrinho_drawer.visible = False
        page.update()

    carrinho_drawer = ft.Container(
        width=360,
        bgcolor="#FFFFFF",
        padding=20,
        visible=False,
        animate=ft.Animation(300, "easeInOut"),
        border_radius=24,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK26, offset=ft.Offset(0, 6)),
        border=ft.border.all(1, color="#E2E8F0"),
        content=ft.Column([
            ft.Container(
                padding=10,
                border_radius=12,
                bgcolor="#F8FAFC",
                content=ft.Row([
                    ft.Icon(name=ft.icons.SHOPPING_CART_OUTLINED, size=26, color="#1D4ED8"),
                    ft.Text("Meu Carrinho", size=22, weight=ft.FontWeight.BOLD, color="#1D4ED8"),
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        icon_color=ft.colors.RED,
                        tooltip="Fechar",
                        icon_size=22,
                        on_click=lambda e: fechar_carrinho()
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ),
            ft.Divider(thickness=1),
            ft.Column([], spacing=10, scroll=ft.ScrollMode.ALWAYS),
            ft.Container(),
            ft.ElevatedButton(
                "Confirmar",
                icon=ft.icons.CHECK,
                bgcolor="#16A34A",
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.padding.symmetric(horizontal=20, vertical=14)
                ),
                on_click=lambda e: page.go("/agendamento")
            )
        ], spacing=16)
    )

    def gerar_cards(pagina):
        nonlocal pagina_atual
        busca = busca_ref.current.value.lower() if busca_ref.current and busca_ref.current.value else ""
        pagina_atual = 1 if pagina is None else pagina
        cards_container.controls.clear()

        medicamentos_filtrados = [
            med for med in medicamentos_mock
            if busca in med["nome"].lower() or busca in med["descricao"].lower()
        ]

        total_paginas = max(1, (len(medicamentos_filtrados) + medicamentos_por_pagina - 1) // medicamentos_por_pagina)

        botoes_paginacao.controls.clear()
        for i in range(1, total_paginas + 1):
            botoes_paginacao.controls.append(
                ft.ElevatedButton(str(i), on_click=lambda e, p=i: gerar_cards(p))
            )

        inicio = (pagina_atual - 1) * medicamentos_por_pagina
        fim = inicio + medicamentos_por_pagina
        medicamentos_exibidos = medicamentos_filtrados[inicio:fim]

        for med in medicamentos_exibidos:
            def handler_adicionar(e, med=med):
                adicionar_ao_carrinho(med)

            cards_container.controls.append(
                ft.Container(
                    on_click=lambda e, m=med: abrir_detalhes_medicamento(e, m),
                    alignment=ft.alignment.center,
                    padding=16,
                    bgcolor="#F8FAFC",
                    border_radius=16,
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    content=ft.Column([
                        ft.Image(src=med["imagem"], width=100, height=100),
                        ft.Text(med["nome"], text_align=ft.TextAlign.CENTER, size=13, weight=ft.FontWeight.BOLD),
                        ft.Text(med["descricao"], size=11, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "ADICIONAR",
                            width=130,
                            bgcolor=ft.Colors.BLUE_900,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=handler_adicionar
                        )
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )

        page.update()

    def icone_carrinho():
        return ft.Stack([
            ft.IconButton(
                icon=ft.icons.SHOPPING_BAG_OUTLINED,
                icon_size=30,
                icon_color="#1E3A8A",
                on_click=abrir_carrinho
            ),
            ft.Container(
                content=ft.Text("0", size=10, color=ft.colors.WHITE, ref=carrinho_count),
                width=16,
                height=16,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.RED,
                border_radius=8,
                right=0,
                top=0,
                visible=True
            )
        ])

    def create_menu_item(icon, text, route):
        container = ft.Container(
            padding=ft.padding.symmetric(vertical=12, horizontal=10),
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.BLUE_600, size=24),
                ft.Text(text, size=16, color="#111827")
            ], spacing=15),
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
                ], spacing=15),
                border_radius=8,
                bgcolor="#FEE2E2",
                ink=True,
                on_click=lambda e: page.go("/"),
                animate=ft.Animation(200, "easeInOut")
            )
        ], spacing=10, expand=True)
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
                content=ft.Row([
                    sidebar,
                    carrinho_drawer,
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
                                        ref=busca_ref,
                                        hint_text="Buscar medicamentos...",
                                        prefix_icon=ft.icons.SEARCH,
                                        border_radius=12,
                                        bgcolor=ft.colors.WHITE,
                                        height=45,
                                        col={"xs": 12, "md": 6},
                                        on_change=lambda e: gerar_cards(None)
                                    ),
                                    ft.Row([
                                        icone_carrinho(),
                                        ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                                        ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD),
                                    ], spacing=10, alignment=ft.MainAxisAlignment.END, col={"xs": 12, "md": 4})
                                ])
                            ),
                            ft.Container(
                                alignment=ft.alignment.top_center,
                                padding=30,
                                content=ft.Column([
                                    ft.Text("MEDICAMENTOS DISPONÍVEIS", size=24, weight=ft.FontWeight.W_600),
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

def tela_agendamento(page: ft.Page):
    # Refs
    data_picker = ft.DatePicker()
    hora_picker = ft.TimePicker()

    data_selecionada = ft.Text("Nenhuma data selecionada", size=16, color=ft.colors.GREY_700)
    hora_selecionada = ft.Text("Nenhum horário selecionado", size=16, color=ft.colors.GREY_700)

    def confirmar_agendamento(e):
        if "Nenhuma" in data_selecionada.value or "Nenhum" in hora_selecionada.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecione data e horário."), bgcolor=ft.colors.RED_400)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("✅ Agendamento realizado com sucesso!"), bgcolor=ft.colors.GREEN_500)
        page.snack_bar.open = True
        page.update()

    def selecionar_data(e):
        data_selecionada.value = f"📅 Data: {data_picker.value.strftime('%d/%m/%Y')}"
        page.update()

    def selecionar_hora(e):
        hora_selecionada.value = f"⏰ Horário: {hora_picker.value.strftime('%H:%M')}"
        page.update()

    # Eventos
    data_picker.on_change = selecionar_data
    hora_picker.on_change = selecionar_hora

    page.overlay.extend([data_picker, hora_picker])

    return ft.View(
        route="/agendamento",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.colors.WHITE,
                alignment=ft.alignment.center,
                padding=40,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        ft.Text("🗓️ Agendamento de Retirada", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.Container(
                            width=500,
                            padding=30,
                            border_radius=20,
                            bgcolor=ft.colors.BLUE_50,
                            shadow=ft.BoxShadow(blur_radius=25, color=ft.colors.BLACK12, offset=ft.Offset(0, 10)),
                            content=ft.Column(
                                spacing=25,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("Escolha a data e o horário desejado:", size=18, color=ft.colors.GREY_800, text_align=ft.TextAlign.CENTER),
                                    
                                    ft.ElevatedButton(
                                        "Selecionar Data",
                                        icon=ft.icons.DATE_RANGE,
                                        on_click=lambda e: data_picker.pick_date(),
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.BLUE_800,
                                            color=ft.colors.WHITE,
                                            padding=ft.padding.symmetric(vertical=12, horizontal=20),
                                            shape=ft.RoundedRectangleBorder(radius=12)
                                        )
                                    ),
                                    data_selecionada,

                                    ft.ElevatedButton(
                                        "Selecionar Horário",
                                        icon=ft.icons.ACCESS_TIME,
                                        on_click=lambda e: hora_picker.pick_time(),
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.BLUE_800,
                                            color=ft.colors.WHITE,
                                            padding=ft.padding.symmetric(vertical=12, horizontal=20),
                                            shape=ft.RoundedRectangleBorder(radius=12)
                                        )
                                    ),
                                    hora_selecionada,

                                    ft.ElevatedButton(
                                        "Confirmar Agendamento",
                                        icon=ft.icons.CHECK,
                                        on_click=confirmar_agendamento,
                                        style=ft.ButtonStyle(
                                            bgcolor=ft.colors.GREEN_600,
                                            color=ft.colors.WHITE,
                                            padding=ft.padding.symmetric(vertical=14),
                                            shape=ft.RoundedRectangleBorder(radius=16)
                                        )
                                    )
                                ]
                            )
                        ),
                        ft.ElevatedButton(
                            "Voltar",
                            icon=ft.icons.ARROW_BACK,
                            on_click=lambda e: page.go("/usuario"),
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.GREY_500,
                                color=ft.colors.WHITE,
                                padding=ft.padding.symmetric(vertical=12, horizontal=24),
                                shape=ft.RoundedRectangleBorder(radius=12)
                            )
                        )
                    ]
                )
            )
        ]
    )

def tela_detalhes_medicamento(page: ft.Page):
    medicamento = page.client_storage.get("medicamento_detalhe")

    if not medicamento:
        return ft.View(
            route="/detalhes_medicamento",
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Text("❌ Nenhum medicamento selecionado.", size=20, color=ft.colors.RED)
                )
            ]
        )

    qtd_ref = ft.Ref[ft.TextField]()
    imagem_principal = ft.Ref[ft.Image]()
    carrinho_count = ft.Ref[ft.Text]()

    def atualizar_contador():
        carrinho = page.session.get("carrinho") or []
        total = sum(item["quantidade"] for item in carrinho)
        carrinho_count.current.value = str(total)
        carrinho_count.current.update()

    def adicionar_ao_carrinho(e):
        try:
            qtd = int(qtd_ref.current.value)
            if qtd <= 0:
                raise ValueError

            carrinho = page.session.get("carrinho") or []

            for item in carrinho:
                if item["nome"] == medicamento["nome"]:
                    item["quantidade"] += qtd
                    break
            else:
                carrinho.append({
                    "nome": medicamento["nome"],
                    "imagem": medicamento["imagem"],
                    "descricao": medicamento["descricao"],
                    "quantidade": qtd
                })

            page.session.set("carrinho", carrinho)
            atualizar_contador()

            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ {qtd} unidade(s) adicionadas ao carrinho."),
                bgcolor=ft.colors.GREEN_400
            )
            page.snack_bar.open = True
            page.update()
        except:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("❗ Quantidade inválida."),
                bgcolor=ft.colors.RED_400
            )
            page.snack_bar.open = True
            page.update()

    def trocar_imagem(nova_src):
        def handler(e):
            imagem_principal.current.src = nova_src
            imagem_principal.current.update()
        return handler

    return ft.View(
        route="/detalhes_medicamento",
        controls=[
            ft.Container(
                expand=True,
                bgcolor=ft.colors.WHITE,
                padding=40,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    spacing=30,
                    controls=[
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                tooltip="Voltar",
                                icon_color=ft.colors.BLUE,
                                on_click=lambda e: page.go("/usuario")
                            ),
                            ft.Text("🔎 Detalhes do Medicamento", size=28, weight=ft.FontWeight.BOLD, color="#1E3A8A"),

                            ft.Container(expand=True),
                            ft.Stack([
                                ft.IconButton(
                                    icon=ft.icons.SHOPPING_CART_OUTLINED,
                                    icon_color="#1E3A8A",
                                    icon_size=30,
                                    on_click=lambda e: page.go("/usuario")
                                ),
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
                                    visible=True
                                )
                            ]),
                            ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                            ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                        ft.Divider(height=30),

                        ft.ResponsiveRow([
                            ft.Container(
                                col={"sm": 12, "md": 6},
                                padding=20,
                                bgcolor="#F9FAFB",
                                border_radius=20,
                                shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.BLACK12, offset=ft.Offset(0, 10)),
                                content=ft.Column([
                                    ft.Image(ref=imagem_principal, src=medicamento["imagem"], width=300, height=300),
                                    ft.Row([
                                        ft.GestureDetector(
                                            content=ft.Image(src=medicamento["imagem"], width=60, height=60),
                                            on_tap=trocar_imagem(medicamento["imagem"])
                                        ),
                                        ft.GestureDetector(
                                            content=ft.Image(src=medicamento["imagem"], width=60, height=60),
                                            on_tap=trocar_imagem(medicamento["imagem"])
                                        ),
                                        ft.GestureDetector(
                                            content=ft.Image(src=medicamento["imagem"], width=60, height=60),
                                            on_tap=trocar_imagem(medicamento["imagem"])
                                        )
                                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                                ], spacing=15)
                            ),
                            ft.Container(
                                col={"sm": 12, "md": 6},
                                padding=20,
                                content=ft.Column([
                                    ft.Text(medicamento["nome"], size=26, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                                    ft.Text("Tipo: Uso controlado", size=14, color=ft.colors.GREY_700),
                                    ft.Text("Marca: Genérico", size=14, color=ft.colors.GREY_700),
                                    ft.Text("Quantidade: 1 unidade", size=14, color=ft.colors.GREY_700),
                                    ft.Divider(height=20),
                                    ft.Row([
                                        ft.TextField(
                                            ref=qtd_ref,
                                            value="1",
                                            width=80,
                                            label="Qtd.",
                                            keyboard_type=ft.KeyboardType.NUMBER,
                                            border_radius=10,
                                            text_align=ft.TextAlign.CENTER
                                        ),
                                        ft.ElevatedButton(
                                            "Adicionar ao Carrinho",
                                            icon=ft.icons.ADD_SHOPPING_CART,
                                            style=ft.ButtonStyle(
                                                bgcolor="#1E3A8A",
                                                color=ft.colors.WHITE,
                                                padding=ft.padding.symmetric(vertical=14, horizontal=20),
                                                shape=ft.RoundedRectangleBorder(radius=12)
                                            ),
                                            on_click=adicionar_ao_carrinho
                                        )
                                    ], spacing=20)
                                ], spacing=10)
                            )
                        ], run_spacing=30, spacing=30),

                        ft.Divider(height=40),

                        ft.ResponsiveRow([
                            ft.Container(
                                col={"sm": 12, "md": 8},
                                padding=20,
                                bgcolor="#F9FAFB",
                                border_radius=16,
                                content=ft.Column([
                                    ft.Text("Detalhes do produto", size=20, weight=ft.FontWeight.BOLD),
                                    ft.Divider(height=10),
                                    ft.Text("Descrição do Produto:", weight=ft.FontWeight.BOLD),
                                    ft.Text("Este medicamento oferece alívio e cuidado conforme prescrição médica.", size=15),
                                    ft.Divider(height=10),
                                    ft.Text("Benefícios:", weight=ft.FontWeight.BOLD),
                                    ft.Text("- Hidratante\n- Hipoalergênico\n- Aplicação fácil", size=15),
                                    ft.Divider(height=10),
                                    ft.Text("Como usar:", weight=ft.FontWeight.BOLD),
                                    ft.Text("Aplicar conforme orientação médica, em área limpa e seca.", size=15),
                                    ft.Divider(height=10),
                                    ft.Text("Advertências:", weight=ft.FontWeight.BOLD),
                                    ft.Text("- Uso externo\n- Evitar contato com olhos\n- Manter fora do alcance de crianças", size=15)
                                ], spacing=10)
                            ),
                            ft.Container(
                                col={"sm": 12, "md": 4},
                                padding=20,
                                bgcolor="#F9FAFB",
                                border_radius=16,
                                content=ft.Column([
                                    ft.Text("Características", size=20, weight=ft.FontWeight.BOLD),
                                    ft.Divider(),
                                    ft.Row([ft.Text("Código:", expand=True), ft.Text("1275221")]),
                                    ft.Divider(),
                                    ft.Row([ft.Text("Quantidade:", expand=True), ft.Text("1g")]),
                                    ft.Divider(),
                                    ft.Row([ft.Text("Marca:", expand=True), ft.Text("Genérico")])
                                ], spacing=8)
                            )
                        ], run_spacing=20, spacing=30)
                    ]
                )
            )
        ]
    )




def main(page: ft.Page):
    page.session.set("carrinho", [])
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
        elif page.route == "/agendamento":
            page.views.append(tela_agendamento(page))
        elif page.route == "/detalhes_medicamento":
            page.views.append(tela_detalhes_medicamento(page))
        if page.session.get("carrinho") is None:
            page.session.set("carrinho", [])


        page.update()
       




    page.on_route_change = route_change
    page.go("/usuario")

ft.app(target=main)


