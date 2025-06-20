import flet as ft
from functools import partial
from database import listar_medicamentos, carregar_carrinho_usuario, adicionar_ao_carrinho_db, remover_do_carrinho_db, buscar_nome_usuario, diminuir_quantidade_db, aumentar_quantidade_db, buscar_dados_usuario

class TelaUsuarioDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.cards_container = ft.ResponsiveRow(run_spacing=20, spacing=20)
        self.pagina_atual = 1
        self.carrinho_count = ft.Ref[ft.Text]()
        self.busca_ref = ft.Ref[ft.TextField]()
        self.contador = {"valor": 0}
        self.carrinho = []
        self.botoes_paginacao = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.medicamentos = self.carregar_medicamentos()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            bgcolor=ft.Colors.RED_400,
            duration=3000
        )
        self.nome_usuario = self.page.session.get("usuario_nome") or "Paciente"
        self.email_usuario = self.page.session.get("usuario_email")
        self.usuario_id = self.get_usuario_id_por_email(self.email_usuario)
        self.nome_usuario = self.page.session.get("usuario_nome") or "Paciente"

        self.carrinho = carregar_carrinho_usuario(self.usuario_id)
        self.contador = {"valor": sum(item["quantidade"] for item in self.carrinho)}

        # Cria o drawer do carrinho
        self.carrinho_drawer = self.criar_carrinho_drawer()

    def get_usuario_id_por_email(self, email):
        import sqlite3
        conn = sqlite3.connect("farmconnect.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado[0] if resultado else None

    def atualizar_contador(self):
        total = sum(item["quantidade"] for item in self.carrinho)
        self.contador["valor"] = total
        self.carrinho_count.current.value = str(total)
        self.carrinho_count.current.update()

    def aumentar_quantidade(self, item):
        if item["quantidade"] < item["estoque"]:
            item["quantidade"] += 1
            aumentar_quantidade_db(self.usuario_id, item["id"])
        else:
            self.page.snack_bar.content.value = "Você já adicionou todas as unidades disponíveis."
            self.page.snack_bar.bgcolor = ft.Colors.RED_400
            self.page.snack_bar.open = True

        self.atualizar_contador()
        self.abrir_carrinho()

    def diminuir_quantidade(self, item):
        item["quantidade"] -= 1
        diminuir_quantidade_db(self.usuario_id, item["id"])

        if item["quantidade"] <= 0:
            self.carrinho.remove(item)

        self.atualizar_contador()
        self.abrir_carrinho()

    def carregar_medicamentos(self):
        dados = listar_medicamentos()
        return [
            {
                "id": m[0],
                "nome": m[1],
                "codigo": m[2],
                "descricao": m[3],
                "imagem": m[4],
                "estoque": m[5],
                "categoria": m[6],
                "fabricante": m[7],
            } for m in dados
        ]

    medicamentos_por_pagina = 8    
    def criar_carrinho_drawer(self):
        return ft.Container(
            width=360,
            bgcolor="#FFFFFF",
            padding=20,
            visible=False,
            animate=ft.Animation(300, "easeInOut"),
            border_radius=24,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 6)),
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
                            icon_color=ft.Colors.RED,
                            tooltip="Fechar",
                            icon_size=22,
                            on_click=lambda e: self.fechar_carrinho()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ),
                ft.Divider(thickness=1),
                ft.Column([], spacing=10, scroll=ft.ScrollMode.ALWAYS),  # <- index 2 usado em abrir_carrinho
                ft.Container(),
                ft.ElevatedButton(
                    "Confirmar",
                    icon=ft.icons.CHECK,
                    bgcolor="#16A34A",
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14)
                    ),
                    on_click=lambda e: self.page.go("/agendamento")
                )
            ], spacing=16)
        )

    def remover_do_carrinho(self, e=None, item=None):
        if item in self.carrinho:
            self.carrinho.remove(item)
            remover_do_carrinho_db(self.usuario_id, item["id"])
            self.atualizar_contador()
            self.abrir_carrinho()



    def adicionar_ao_carrinho(self, medicamento):
        # Verifica se já está no carrinho
        existente = next((item for item in self.carrinho if item["id"] == medicamento["id"]), None)

        if existente:
            if existente["quantidade"] < medicamento["estoque"]:
                existente["quantidade"] += 1
                adicionar_ao_carrinho_db(self.usuario_id, medicamento["id"])
            else:
                self.page.snack_bar.content.value = "Você já adicionou todas as unidades disponíveis."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return
        else:
            if medicamento["estoque"] > 0:
                novo = {**medicamento, "quantidade": 1}
                self.carrinho.append(novo)
                adicionar_ao_carrinho_db(self.usuario_id, medicamento["id"])
            else:
                self.page.snack_bar.content.value = "❗ Medicamento fora de estoque."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return

        self.atualizar_contador()
        self.abrir_carrinho()

    def abrir_detalhes_medicamento(self, e, med):
        self.page.client_storage.set("medicamento_detalhe", med)
        self.page.go("/detalhes_medicamento")


    def abrir_carrinho(self, e=None):
        itens_coluna = self.carrinho_drawer.content.controls[2]
        itens_coluna.controls.clear()

        if not self.carrinho:
            itens_coluna.controls.append(
                ft.Text("Carrinho vazio", size=14, color=ft.Colors.GREY_600)
            )
        else:
            for item in self.carrinho:
                itens_coluna.controls.append(
        ft.Container(
            padding=10,
            bgcolor="#FFFFFF",
            border_radius=8,
            content=ft.Row([
                ft.Column([
                    ft.Text(item["nome"], size=13, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.REMOVE,
                            icon_color=ft.Colors.BLUE_600,
                            tooltip="Diminuir",
                            on_click=lambda e, med=item: self.diminuir_quantidade(med)
                        ),
                        ft.Text(f"{item['quantidade']} un.", size=14, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.icons.ADD,
                            icon_color=ft.Colors.BLUE_600,
                            tooltip="Aumentar",
                            on_click=lambda e, med=item: self.aumentar_quantidade(med)
                        )
                    ], spacing=5)
                ], expand=True),
                ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.RED,
                    tooltip="Remover",
                    on_click=partial(self.remover_do_carrinho, item=item)
                )
            ])
        )
    )

        self.carrinho_drawer.visible = True
        self.page.update()

    def fechar_carrinho(self):
        self.carrinho_drawer.visible = False
        self.page.update()




    def gerar_cards(self, pagina=None):
        busca = self.busca_ref.current.value.lower() if self.busca_ref.current and self.busca_ref.current.value else ""
        self.pagina_atual = 1 if pagina is None else pagina
        self.cards_container.controls.clear()

        medicamentos_filtrados = [
            med for med in self.medicamentos
            if busca in med["nome"].lower() or busca in med["descricao"].lower()
        ]

        total_paginas = max(1, (len(medicamentos_filtrados) + self.medicamentos_por_pagina - 1) // self.medicamentos_por_pagina)

        self.botoes_paginacao.controls.clear()
        for i in range(1, total_paginas + 1):
            self.botoes_paginacao.controls.append(
                ft.ElevatedButton(str(i), on_click=lambda e, p=i: self.gerar_cards(p))
            )

        inicio = (self.pagina_atual - 1) * self.medicamentos_por_pagina
        fim = inicio + self.medicamentos_por_pagina
        medicamentos_exibidos = medicamentos_filtrados[inicio:fim]

        for med in medicamentos_exibidos:
            def handler_adicionar(e, med=med):
                self.adicionar_ao_carrinho(med)

            self.cards_container.controls.append(
                ft.Container(
                    on_click=lambda e, m=med: self.abrir_detalhes_medicamento(e, m),
                    alignment=ft.alignment.center,
                    padding=16,
                    bgcolor="#F8FAFC",
                    border_radius=16,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    content=ft.Column([
                        ft.Image(src=med["imagem"], width=100, height=100),
                        ft.Text(med["nome"], text_align=ft.TextAlign.CENTER, size=13, weight=ft.FontWeight.BOLD),
                        ft.Text(med["descricao"], size=11, text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "ADICIONAR",
                            width=130,
                            bgcolor=ft.Colors.BLUE_900,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=handler_adicionar
                        )
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )

        self.page.update()


    def icone_carrinho(self):
        return ft.Stack([
            ft.IconButton(
                icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                icon_size=30,
                icon_color="#1E3A8A",
                on_click=self.abrir_carrinho
            ),
            ft.Container(
                content=ft.Text("0", size=10, color=ft.Colors.WHITE, ref=self.carrinho_count),
                width=16,
                height=16,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.RED,
                border_radius=8,
                right=0,
                top=0,
                visible=True
            )
        ])


    def create_menu_item(self, icon, text, route):
        container = ft.Container(
            padding=ft.padding.symmetric(vertical=12, horizontal=10),
            content=ft.Row([
                ft.Icon(icon, color=ft.Colors.BLUE_600, size=24),
                ft.Text(text, size=16, color="#111827")
            ], spacing=15),
            ink=True,
            border_radius=8,
            bgcolor="#FFFFFF",
            on_click=lambda e: self.page.go(route),
            animate=ft.Animation(200, "easeInOut"),
            margin=ft.margin.only(bottom=8)
        )

        def on_hover(e):
            container.bgcolor = "#D1EEFA" if e.data == "true" else "#FFFFFF"
            container.update()

        container.on_hover = on_hover
        return container


    def build_tela(self):
        sidebar = ft.Container(
            width=280,
            bgcolor="#F8FAFC",
            border=ft.border.only(right=ft.BorderSide(1, "#E5E7EB")),
            padding=ft.padding.symmetric(vertical=20, horizontal=10),
            content=ft.Column([
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(vertical=10),
                    content=ft.Image(src="logo.png", width=120, height=40)
                ),
                ft.Divider(thickness=1),
                self.create_menu_item(ft.Icons.PERSON_OUTLINED, "Meu Perfil", "/perfil"),
                self.create_menu_item(ft.Icons.MEDICAL_SERVICES_OUTLINED, "Histórico de Retiradas", "/medicamentos_retirados"),
                self.create_menu_item(ft.Icons.CALENDAR_MONTH_OUTLINED, "Meus Agendamentos", "/agendamentos"),
                self.create_menu_item(ft.Icons.DESCRIPTION_OUTLINED, "Documentos Requeridos", "/documentos"),
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
                    on_click=lambda e: self.page.go("/"),
                    animate=ft.Animation(200, "easeInOut")
                )
            ], spacing=10, expand=True)
        )

        self.gerar_cards(self.pagina_atual)

        return ft.View(
            route="/usuario",
            controls=[
                self.page.snack_bar,
                ft.Container(
                    expand=True,
                    content=ft.Row([
                        sidebar,
                        self.carrinho_drawer,
                        ft.Container(
                            expand=True,
                            padding=20,
                            content=ft.Column([
                                ft.Container(
                                    bgcolor="#F8FAFC",
                                    border_radius=16,
                                    padding=ft.padding.symmetric(horizontal=20, vertical=18),
                                    shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.BLACK26, offset=ft.Offset(0, 3)),
                                    content=ft.ResponsiveRow([
                                        ft.Image(src="logo.png", width=110, col={"xs": 12, "md": 2}),
                                        ft.TextField(
                                            ref=self.busca_ref,
                                            hint_text="Buscar medicamentos...",
                                            prefix_icon=ft.icons.SEARCH,
                                            border_radius=12,
                                            bgcolor=ft.Colors.WHITE,
                                            height=45,
                                            col={"xs": 12, "md": 6},
                                            on_change=lambda e: self.gerar_cards(None)
                                        ),
                                        ft.Row([
                                            ft.Stack([
                                                ft.IconButton(
                                                    icon=ft.icons.SHOPPING_BAG_OUTLINED,
                                                    icon_size=30,
                                                    icon_color="#1E3A8A",
                                                    on_click=self.abrir_carrinho
                                                ),
                                                ft.Container(
                                                    content=ft.Text("0", size=10, color=ft.Colors.WHITE, ref=self.carrinho_count),
                                                    width=16,
                                                    height=16,
                                                    alignment=ft.alignment.center,
                                                    bgcolor=ft.Colors.RED,
                                                    border_radius=8,
                                                    right=0,
                                                    top=0,
                                                    visible=True
                                                )
                                            ]),
                                            ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                                            ft.Text(self.nome_usuario.upper(), size=13, weight=ft.FontWeight.BOLD)
                                        ], spacing=10, alignment=ft.MainAxisAlignment.END, col={"xs": 12, "md": 4})
                                    ])
                                ),
                                ft.Container(
                                    alignment=ft.alignment.top_center,
                                    padding=30,
                                    content=ft.Column([
                                        ft.Container(
                                            ft.Text("MEDICAMENTOS DISPONÍVEIS", size=24, weight="bold", color="#1E3A8A"),
                                            expand=True,
                                            alignment=ft.alignment.center
                                        ),
                                        ft.Row([
                                            ft.OutlinedButton("Mais Buscados"),
                                            ft.OutlinedButton("Meus Agendamentos"),
                                            ft.OutlinedButton("Feedback"),
                                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),
                                        ft.Divider(height=25),
                                        self.cards_container,
                                        ft.Divider(height=30),
                                        self.botoes_paginacao
                                    ], spacing=30)
                                )
                            ], scroll=ft.ScrollMode.ADAPTIVE, spacing=20)
                        )
                    ])
                )
            ]
        )

    def tela_documentos(self):
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
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        # Caixa de Documentos
                        ft.Container(
                            padding=30,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
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
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        # Botões de Ação
                        ft.Row([
                            ft.ElevatedButton(
                                "Baixar Documento de Autorização",
                                icon=ft.icons.FILE_DOWNLOAD,
                                bgcolor=ft.Colors.BLUE_900,
                                color=ft.Colors.WHITE,
                                width=260,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(vertical=12)
                                ),
                                on_click=lambda e: print("Documento baixado")
                            ),
                            ft.ElevatedButton(
                                "Voltar",
                                icon=ft.icons.ARROW_BACK_IOS_NEW,
                                bgcolor=ft.Colors.GREY_50,
                                width=150,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(vertical=12)
                                ),
                                on_click=lambda e: self.page.go("/usuario")
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]
        )


    def tela_perfil_paciente(self):
        # Refs e dados
        self.editando_nome = ft.Ref[bool]()
        self.editando_cpf = ft.Ref[bool]()
        self.editando_nasc = ft.Ref[bool]()
        self.editando_email = ft.Ref[bool]()
        self.editando_tel = ft.Ref[bool]()

        self.nome_field = ft.Ref[ft.TextField]()
        self.cpf_field = ft.Ref[ft.TextField]()
        self.nasc_field = ft.Ref[ft.TextField]()
        self.email_field = ft.Ref[ft.TextField]()
        self.tel_field = ft.Ref[ft.TextField]()

        self.editando_nome.current = False
        self.editando_cpf.current = False
        self.editando_nasc.current = False
        self.editando_email.current = False
        self.editando_tel.current = False

        self.dados_usuario = buscar_dados_usuario(self.email_usuario) or {
            "nome": "Desconhecido",
            "cpf": "",
            "nasc": "",
            "email": self.email_usuario,
            "tel": "(00) 00000-0000"
        }

        def iniciar_edicao(ref_bool, input_ref):
            ref_bool.current = True
            self.page.update()
            input_ref.current.focus()

        def salvar(ref_bool, campo, input_ref):
            self.dados_usuario[campo] = input_ref.current.value
            ref_bool.current = False
            self.page.snack_bar = ft.SnackBar(ft.Text(f"{campo.capitalize()} atualizado com sucesso!"), bgcolor=ft.Colors.GREEN_100)
            self.page.snack_bar.open = True
            self.page.update()

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
                                icon_color=ft.Colors.BLUE,
                                tooltip="Editar",
                                on_click=lambda e: iniciar_edicao(ref_bool, input_ref)
                            )
                        ]
                    ),
                    ft.TextField(
                        ref=input_ref,
                        value=self.dados_usuario[campo],
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
                            ft.Text("Perfil do Paciente", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Container(
                                width=700,
                                padding=25,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=20,
                                shadow=ft.BoxShadow(blur_radius=24, color=ft.Colors.BLACK26, offset=ft.Offset(0, 12)),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=30,
                                    controls=[
                                        ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10,
                                            controls=[
                                                ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=60),
                                                ft.Text(self.dados_usuario["nome"], size=24, weight=ft.FontWeight.BOLD),
                                                ft.Text("Paciente FarmConnect", size=16, color=ft.Colors.GREY_600)
                                            ]
                                        ),
                                        campo_editavel("Nome", "nome", self.editando_nome, self.nome_field,),
                                        campo_editavel("CPF", "cpf", self.editando_cpf, self.cpf_field),
                                        campo_editavel("Data de Nascimento", "nasc", self.editando_nasc, self.nasc_field),
                                        campo_editavel("Email", "email", self.editando_email, self.email_field),
                                        campo_editavel("Telefone", "tel", self.editando_tel, self.tel_field),
                                    ]
                                )
                            ),
                            ft.ElevatedButton(
                                "Voltar",
                                icon=ft.icons.ARROW_BACK,
                                bgcolor=ft.Colors.GREY_50,
                                width=160,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=16),
                                    padding=ft.padding.symmetric(vertical=12),
                                    elevation=4
                                ),
                                on_click=lambda e: self.page.go("/usuario")
                            )
                        ]
                    )
                )
            ]
        )



    def tela_medicamentos_retirados(self):
        self.medicamentos_retirados_mock = [
            {"nome": "Interferon Alfa", "data_retirada": "10/05/2025", "quantidade": 2},
            {"nome": "Rituximabe", "data_retirada": "08/05/2025", "quantidade": 1},
            {"nome": "Adalimumabe", "data_retirada": "01/05/2025", "quantidade": 3},
            {"nome": "Trastuzumabe", "data_retirada": "28/04/2025", "quantidade": 1},
            {"nome": "Lenalidomida", "data_retirada": "25/04/2025", "quantidade": 2},
        ]

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
                            color=ft.Colors.BLUE_900,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                        ft.Container(
                            padding=30,
                            bgcolor="#F8FAFC",
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 15)),
                            content=ft.Column([
                                ft.Row([
                                    ft.TextField(label="🔍 Buscar Medicamento", expand=True, border_radius=30, on_change=lambda e: print(e.control.value)),
                                    ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.Colors.BLUE_900, on_click=lambda e: print("Buscar"))
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                ft.ListView(
                                    expand=True,
                                    controls=[
                                        ft.Container(
                                            padding=20,
                                            bgcolor="#F8FAFC",
                                            border_radius=16,
                                            margin=ft.margin.only(bottom=20),
                                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK12, offset=ft.Offset(0, 10)),
                                            content=ft.Column([
                                                ft.Text(med["nome"], size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                                                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                                ft.Text(f"📅 Data de Retirada: {med['data_retirada']}", size=14, color="#374151"),
                                                ft.Text(f"📦 Quantidade: {med['quantidade']} unidades", size=14, color="#374151"),
                                                ft.ElevatedButton(
                                                    "Ver Detalhes",
                                                    icon=ft.icons.INFO_OUTLINE,
                                                    bgcolor=ft.Colors.BLUE_900,
                                                    color=ft.Colors.WHITE,
                                                    width=200,
                                                    style=ft.ButtonStyle(
                                                        shape=ft.RoundedRectangleBorder(radius=12),
                                                        padding=ft.padding.symmetric(vertical=10)
                                                    ),
                                                    on_click=lambda e, med=med: print(f"Detalhes de {med['nome']}")
                                                )
                                            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                                        )
                                        for med in self.medicamentos_retirados_mock
                                    ]
                                )
                            ], spacing=20)
                        ),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Voltar",
                            icon=ft.Icons.ARROW_BACK_IOS_NEW,
                            bgcolor=ft.Colors.GREY_50,
                            width=150,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.padding.symmetric(vertical=12)
                            ),
                            on_click=lambda e: self.page.go("/usuario")
                        )
                    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]
        )


    def tela_agendamento(self):
        import calendar
        import datetime
        import flet as ft

        hoje = datetime.date.today()
        self.mes_atual = hoje.month
        self.ano_atual = hoje.year
        self.data_escolhida = None
        self.horario_escolhido = None

        self.data_selecionada = ft.Text("📅 Nenhuma data selecionada", size=16, color=ft.Colors.GREY_700)
        self.hora_selecionada = ft.Text("⏰ Nenhum horário selecionado", size=16, color=ft.Colors.GREY_700)

        calendario_grid = ft.Ref[ft.Column]()
        self.mes_label = ft.Ref[ft.Text]()

        def atualizar_calendario():
            if not self.mes_label.current or not calendario_grid.current:
                return
            dias = []
            self.mes_label.current.value = f"{calendar.month_name[self.mes_atual]} {self.ano_atual}"
            cal = calendar.Calendar(firstweekday=6)
            for semana in cal.monthdatescalendar(self.ano_atual, self.mes_atual):
                linha = ft.Row(
                    spacing=4,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            text=str(dia.day),
                            width=32,
                            height=32,
                            disabled=dia < datetime.date.today() or dia.month != self.mes_atual,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12),
                                padding=0,
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor="#E0F2FE" if dia == self.data_escolhida else ft.Colors.WHITE,
                                color=ft.Colors.BLUE_900,
                            ),
                            on_click=lambda e, dia=dia: selecionar_data(dia)
                        ) if dia.month == self.mes_atual else ft.Container(width=40, height=40)
                        for dia in semana
                    ]
                )
                dias.append(linha)
            calendario_grid.current.controls = dias
            self.page.update()

        def selecionar_data(data):
            self.data_escolhida = data
            self.data_selecionada.value = f"📅 Data: {data.strftime('%d/%m/%Y')}"
            atualizar_calendario()

        def selecionar_hora_manual(hora):
            self.horario_escolhido = hora
            self.hora_selecionada.value = f"⏰ Horário: {hora}"
            self.page.update()

        def mudar_mes(direcao):
            if direcao == "anterior":
                if self.mes_atual == 1:
                    self.mes_atual = 12
                    self.ano_atual -= 1
                else:
                    self.mes_atual -= 1
            elif direcao == "proximo":
                if self.mes_atual == 12:
                    self.mes_atual = 1
                    self.ano_atual += 1
                else:
                    self.mes_atual += 1
            atualizar_calendario()

        def confirmar_agendamento(e):
            if not self.data_escolhida or not self.horario_escolhido:
                self.page.snack_bar = ft.SnackBar(ft.Text("Por favor, selecione data e horário."), bgcolor=ft.Colors.RED_400)
                self.page.snack_bar.open = True
                self.page.update()
                return

            # Aqui você pode salvar no banco se quiser...

            self.page.go("/agendamento_confirmado")

        def gerar_botoes_horarios():
            horarios = []
            hora = 8
            minuto = 0
            while hora < 18:
                texto = f"{hora:02d}:{minuto:02d}"
                btn = ft.ElevatedButton(
                    text=texto,
                    width=60,
                    height=32,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=12),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        bgcolor=ft.Colors.BLUE_100 if texto == self.horario_escolhido else ft.Colors.WHITE,
                        color=ft.Colors.BLUE_900,
                    ),
                    on_click=lambda e, h=texto: selecionar_hora_manual(h)
                )
                horarios.append(btn)
                minuto += 30
                if minuto == 60:
                    minuto = 0
                    hora += 1
            linhas = []
            for i in range(0, len(horarios), 4):
                linhas.append(ft.Row(horarios[i:i+4], spacing=10, alignment=ft.MainAxisAlignment.CENTER))
            return linhas

        atualizar_calendario()  # Garante que o calendário apareça assim que abrir a tela

        return ft.View(
            route="/agendamento",
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    alignment=ft.alignment.center,
                    padding=40,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            ft.Text("🗓️ Agendamento de Retirada", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Container(
                                width=700,
                                padding=30,
                                border_radius=24,
                                bgcolor="#F0F9FF",
                                shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK12, offset=ft.Offset(0, 10)),
                                content=ft.Column(
                                    spacing=25,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Escolha a data e o horário desejado:", size=18, color=ft.Colors.BLUE_900, text_align=ft.TextAlign.CENTER),

                                        ft.Text("⏰ Selecione o Horário:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                        ft.Column(gerar_botoes_horarios(), spacing=10),
                                        self.hora_selecionada,

                                        ft.Text("📅 Selecione a Data:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                        ft.Column([
                                            ft.Row([
                                                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: mudar_mes("anterior")),
                                                ft.Text("", ref=self.mes_label, size=16, weight="bold", color=ft.Colors.BLUE_900),
                                                ft.IconButton(ft.icons.ARROW_FORWARD, on_click=lambda e: mudar_mes("proximo")),
                                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.Divider(),
                                            ft.Column([], ref=calendario_grid)
                                        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                                        self.data_selecionada,

                                        ft.ElevatedButton(
                                            "Confirmar Agendamento",
                                            icon=ft.icons.CHECK_CIRCLE,
                                            on_click=confirmar_agendamento,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.GREEN_600,
                                                color=ft.Colors.WHITE,
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
                                on_click=lambda e: self.page.go("/usuario"),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.GREY_50,
                                    color=ft.Colors.WHITE,
                                    padding=ft.padding.symmetric(vertical=12, horizontal=24),
                                    shape=ft.RoundedRectangleBorder(radius=12)
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def tela_detalhes_medicamento(self):
        self.atualizar_contador()
        medicamento = self.page.client_storage.get("medicamento_detalhe")

        if not medicamento:
            return ft.View(
                route="/detalhes_medicamento",
                controls=[
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Text("❌ Nenhum medicamento selecionado.", size=20, color=ft.Colors.RED)
                    )
                ]
            )

        self.qtd_ref = ft.Ref[ft.TextField]()
        self.imagem_principal = ft.Ref[ft.Image]()
        self.carrinho_count = ft.Ref[ft.Text]()

        
        def adicionar_ao_carrinho(e):
            try:
                qtd = int(self.qtd_ref.current.value)
                if qtd <= 0:
                    raise ValueError
                carrinho = self.page.session.get("carrinho") or []
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
                self.page.session.set("carrinho", carrinho)
                self.atualizar_contador()
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ {qtd} unidade(s) adicionadas ao carrinho."),
                    bgcolor=ft.Colors.GREEN_400
                )
            except:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("❗ Quantidade inválida."),
                    bgcolor=ft.Colors.RED_400
                )
            self.page.snack_bar.open = True
            self.atualizar_contador()
            self.page.update()

        def trocar_imagem(nova_src):
            def handler(e):
                self.imagem_principal.current.src = nova_src
                self.imagem_principal.current.update()
            return handler

        return ft.View(
            route="/detalhes_medicamento",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row([
                    self.carrinho_drawer,  # <- Sacola lateral
                    ft.Container(
                        expand=True,
                        bgcolor="#F9FAFB",
                        padding=30,
                        content=ft.Column(
                            spacing=30,
                            controls=[
                                # Header com título e ícones
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.icons.ARROW_BACK,
                                        tooltip="Voltar",
                                        icon_color="#1E3A8A",
                                        on_click=lambda e: self.page.go("/usuario")
                                    ),
                                    ft.Text("Detalhes do Medicamento", size=28, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                                    ft.Container(expand=True),
                                    self.icone_carrinho(),
                                    ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                                    ft.Text("JOÃO NASCIMENTO", size=13, weight=ft.FontWeight.BOLD)
                                ]),

                                # Imagem e info do medicamento
                                ft.ResponsiveRow([

                                    ft.Container(
                                        col={"sm": 12, "md": 6},
                                        padding=20,
                                        bgcolor="white",
                                        border_radius=20,
                                        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12, offset=ft.Offset(0, 10)),
                                        content=ft.Column([

                                            ft.Image(ref=self.imagem_principal, src=medicamento["imagem"], width=300, height=300),
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
                                            ft.Text("Tipo: Uso controlado", size=14, color=ft.Colors.GREY_700),
                                            ft.Text("Marca: Genérico", size=14, color=ft.Colors.GREY_700),
                                            ft.Text("Quantidade: 1 unidade", size=14, color=ft.Colors.GREY_700),
                                            ft.Divider(height=20),
                                            ft.Row([
                                                ft.TextField(
                                                    ref=self.qtd_ref,
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
                                                        color=ft.Colors.WHITE,
                                                        padding=ft.padding.symmetric(vertical=14, horizontal=20),
                                                        shape=ft.RoundedRectangleBorder(radius=12)
                                                    ),
                                                    on_click=adicionar_ao_carrinho
                                                )
                                            ], spacing=20)
                                        ], spacing=10)
                                    )
                                ], run_spacing=30, spacing=30),

                                # Informações detalhadas
                                ft.ResponsiveRow([
                                    ft.Container(
                                        col={"sm": 12, "md": 8},
                                        padding=20,
                                        bgcolor="white",
                                        border_radius=16,
                                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 8)),
                                        content=ft.Column([
                                            ft.Text("📘 Descrição", size=20, weight=ft.FontWeight.BOLD),
                                            ft.Text(medicamento["descricao"], size=15),
                                            ft.Divider(height=20),
                                            ft.Text("📌 Instruções de Uso", size=18, weight=ft.FontWeight.BOLD),
                                            ft.Text("Aplicar conforme orientação médica.", size=14),
                                            ft.Divider(height=20),
                                            ft.Text("⚠️ Advertências", size=18, weight=ft.FontWeight.BOLD),
                                            ft.Text("- Uso externo\n- Evite contato com os olhos\n- Mantenha fora do alcance de crianças", size=14)
                                        ], spacing=10)
                                    ),
                                    ft.Container(
                                        col={"sm": 12, "md": 4},
                                        padding=20,
                                        bgcolor="white",
                                        border_radius=16,
                                        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12, offset=ft.Offset(0, 8)),
                                        content=ft.Column([
                                            ft.Text("📦 Características", size=20, weight=ft.FontWeight.BOLD),
                                            ft.Divider(),
                                            ft.Row([ft.Text("Código:", expand=True), ft.Text("1275221")]),
                                            ft.Row([ft.Text("Peso:", expand=True), ft.Text("1g")]),
                                            ft.Row([ft.Text("Marca:", expand=True), ft.Text("Genérico")])
                                        ], spacing=8)
                                    )
                                ], run_spacing=20, spacing=30)
                            ]
                        )
                    )
                ])
            ]
        )
    
    def tela_meus_agendamentos(self):
        agendamentos_mock = [
            {
                "medicamento": "Adalimumabe 40mg",
                "farmacia": "Farmácia Central - RJ",
                "codigo": "ABC123456",
                "data": "22/06/2025",
                "horario": "09:30",
                "status": "Confirmado",
                "criado_em": "15/06/2025"
            },
            {
                "medicamento": "Interferon Beta",
                "farmacia": "Unidade Zona Sul",
                "codigo": "XYZ789012",
                "data": "25/06/2025",
                "horario": "14:00",
                "status": "Pendente",
                "criado_em": "16/06/2025"
            },
            {
                "medicamento": "Trastuzumabe",
                "farmacia": "Farmácia Norte",
                "codigo": "RET564738",
                "data": "28/06/2025",
                "horario": "11:15",
                "status": "Cancelado",
                "criado_em": "17/06/2025"
            }
        ]

        def status_badge(status):
            cores = {
                "Pendente": (ft.Colors.AMBER_700, ft.Colors.AMBER_100),
                "Confirmado": (ft.Colors.GREEN_600, ft.Colors.GREEN_100),
                "Cancelado": (ft.Colors.RED_600, ft.Colors.RED_100),
            }
            cor_texto, cor_bg = cores.get(status, (ft.Colors.GREY, ft.Colors.GREY_200))
            icone = (
                ft.icons.CHECK_CIRCLE_OUTLINE if status == "Confirmado"
                else ft.icons.HOURGLASS_EMPTY if status == "Pendente"
                else ft.icons.CANCEL
            )
            return ft.Container(
                bgcolor=cor_bg,
                border_radius=20,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                content=ft.Row([
                    ft.Icon(icone, color=cor_texto, size=18),
                    ft.Text(status.upper(), size=12, weight="bold", color=cor_texto)
                ], spacing=6)
            )

        cards = []
        for ag in agendamentos_mock:
            badge = status_badge(ag["status"])

            acoes = ft.Row([
                ft.ElevatedButton(
                    "Reagendar",
                    icon=ft.icons.UPDATE,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=14, vertical=8),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        bgcolor=ft.Colors.INDIGO_100,
                        color=ft.Colors.INDIGO_900
                    ),
                    on_click=lambda e, med=ag["medicamento"]: print(f"Reagendando: {med}")
                )
            ], spacing=10)

            cards.append(
                ft.AnimatedSwitcher(
                    transition=ft.Animation(600, "easeInOut"),
                    content=ft.Container(
                        scale=1.0,
                        opacity=1.0,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=16,
                        padding=20,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                        animate=ft.Animation(400, "easeInOut"),
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"💊 {ag['medicamento']}", size=18, weight="bold", color="#1E3A8A"),
                                ft.Container(expand=True),
                                badge
                            ]),
                            ft.Divider(thickness=1),
                            ft.Text(f"🏥 Farmácia: {ag['farmacia']}", size=14),
                            ft.Text(f"🗓️ Data: {ag['data']} às {ag['horario']}", size=14),
                            ft.Text(f"🔐 Código: {ag['codigo']}", size=14),
                            ft.Text(f"📆 Criado em: {ag['criado_em']}", size=12, color=ft.Colors.GREY_600),
                            ft.Divider(height=10),
                            acoes
                        ], spacing=8)
                    )
                )
            )

        conteudo = (
            ft.Column(cards, spacing=20)
            if cards else
            ft.Container(
                content=ft.Column([
                    ft.Text("📭 Nenhum agendamento encontrado", size=20, color=ft.Colors.GREY_600),
                    ft.Text("Você ainda não possui agendamentos realizados.", size=14, color=ft.Colors.GREY_500),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=60,
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=12, color="#CBD5E1")
            )
        )

        return ft.View(
            route="/agendamentos",
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Stack([
                    ft.Container(
                        expand=True,
                        padding=40,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=["#E0F2FE", "#F0F4FF"]
                        ),
                        content=ft.Column([
                            ft.Container(
                                alignment=ft.alignment.top_right,
                                content=ft.IconButton(
                                    icon=ft.icons.DESCRIPTION,
                                    tooltip="Ver documentos necessários",
                                    icon_color=ft.Colors.BLUE_700,
                                    on_click=lambda e: self.page.go("/documentos")
                                )
                            ),
                            ft.Column([
                                ft.Icon(name=ft.icons.CALENDAR_MONTH, color=ft.Colors.BLUE_900, size=32),
                                ft.Text("Meus Agendamentos", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            conteudo,
                            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                            ft.ElevatedButton(
                                "Exportar",
                                icon=ft.icons.PICTURE_AS_PDF,
                                icon_color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    padding=ft.padding.symmetric(horizontal=20, vertical=14),
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE
                                ),
                                on_click=lambda e: print("Exportar todos os agendamentos")
                            ),
                            ft.ElevatedButton(
                                "Voltar",
                                icon=ft.icons.ARROW_BACK_IOS_NEW,
                                bgcolor=ft.Colors.GREY_50,
                                width=160,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=16),
                                    padding=ft.padding.symmetric(vertical=14)
                                ),
                                on_click=lambda e: self.page.go("/usuario")
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30)
                    ),
                ])
            ]
        )
    
    def tela_agendamento_confirmado(self):
        return ft.View(
            route="/agendamento_confirmado",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    padding=40,
                    bgcolor="#F0F9FF",
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                        controls=[
                            ft.Icon(ft.icons.CHECK_CIRCLE, size=80, color=ft.Colors.GREEN_600),
                            ft.Text("Agendamento Confirmado!", size=30, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                            ft.Text(
                                "Você tem até 10 dias para retirar seu medicamento na farmácia selecionada.",
                                size=18,
                                color=ft.Colors.GREY_800,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.ElevatedButton(
                                "Ver Meus Agendamentos",
                                icon=ft.icons.CALENDAR_MONTH,
                                on_click=lambda e: self.page.go("/agendamentos"),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE,
                                    padding=ft.padding.symmetric(horizontal=24, vertical=14),
                                    shape=ft.RoundedRectangleBorder(radius=12)
                                )
                            ),
                            ft.TextButton(
                                "Voltar para a Página Inicial",
                                on_click=lambda e: self.page.go("/usuario"),
                                style=ft.ButtonStyle(
                                    color=ft.Colors.BLUE_700,
                                    padding=ft.padding.symmetric(horizontal=24, vertical=10)
                                )
                            )
                        ]
                    )
                )
            ]
        )



from tela_principal_usuario import TelaUsuarioDashboard  # certifique-se que o nome do arquivo esteja correto

if __name__ == "__main__":
    def main(page: ft.Page):
        page.session.set("carrinho", [])
        page.title = "FarmConnect"
        page.bgcolor = "#EFF6FF"
        page.scroll = ft.ScrollMode.ADAPTIVE

        dashboard = TelaUsuarioDashboard(page)

        def route_change(route):
            page.views.clear()
            if page.route == "/usuario":
                page.views.append(dashboard.build_tela())
            elif page.route == "/documentos":
                page.views.append(dashboard.tela_documentos())
            elif page.route == "/perfil":
                page.views.append(dashboard.tela_perfil_paciente())
            elif page.route == "/medicamentos_retirados":
                page.views.append(dashboard.tela_medicamentos_retirados())
            elif page.route == "/agendamento":
                page.views.append(dashboard.tela_agendamento())
            elif page.route == "/detalhes_medicamento":
                page.views.append(dashboard.tela_detalhes_medicamento())
            elif page.route == "/agendamentos":
                page.views.append(dashboard.tela_meus_agendamentos())
            elif page.route == "/agendamento_confirmado":
                page.views.append(dashboard.tela_agendamento_confirmado())


            if page.session.get("carrinho") is None:
                page.session.set("carrinho", [])

            page.update()

        page.on_route_change = route_change
        page.go("/usuario")

    ft.app(target=main)



