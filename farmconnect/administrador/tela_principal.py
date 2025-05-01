import flet as ft
from farmconnect.database import listar_medicamentos, editar_medicamento, adicionar_medicamento, listar_categorias, listar_fabricantes

class TelaAdminDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page_settings()
        self.sidebar_open = True
        self.current_view = ft.Column(expand=True)
        self.load_dashboard()  


    def page_settings(self):
        self.page.title = "FarmConnect - Painel Admin"
        self.page.bgcolor = "#F0FDF4"
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def toggle_sidebar(self, e):
        self.sidebar_open = not self.sidebar_open
        self.page.update()

    def menu_item(self, icon, text, on_click=None):
        item = ft.Container(
            content=ft.Row([
                ft.Icon(icon, color="#059669", size=24),
                ft.Text(text, size=14, visible=self.sidebar_open, color="#374151")
            ], spacing=10, alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(vertical=12, horizontal=12),
            bgcolor="#FFFFFF",
            border_radius=10,
            ink=True,
            animate=ft.Animation(200, "easeInOut"),
            on_click=on_click
        )
        def on_hover(e):
            item.bgcolor = "#D1FAE5" if e.data == "true" else "#FFFFFF"
            item.update()
        item.on_hover = on_hover
        return item

    def side_menu(self):
        def create_menu_item(icon, text, on_click=None):
            container = ft.Container(
                padding=ft.padding.symmetric(vertical=12, horizontal=10),
                content=ft.Row(
                    [
                        ft.Icon(icon, color="#059669", size=24),
                        ft.Text(text, size=16, visible=self.sidebar_open, color="#374151"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
                ink=True,
                border_radius=8,
                bgcolor="#FFFFFF",
                on_click=on_click,
                animate=ft.Animation(200, "easeInOut"),
                margin=ft.margin.only(bottom=8),
            )

            def on_hover(e):
                container.bgcolor = "#E0F2F1" if e.data == "true" else "#FFFFFF"
                container.update()

            container.on_hover = on_hover
            return container

        # Itens do menu
        menu_items = [
            create_menu_item(ft.icons.HOME_OUTLINED, "Início", self.load_dashboard),
            create_menu_item(ft.icons.CALENDAR_MONTH_OUTLINED, "Agendamentos", self.load_agendamentos),  # <- AQUI
            create_menu_item(ft.icons.PERSON_OUTLINED, "Pacientes"),
            create_menu_item(ft.icons.LOCAL_HOSPITAL_OUTLINED, "Farmácias"),
            create_menu_item(ft.icons.MEDICAL_SERVICES_OUTLINED, "Medicamentos", self.load_medicamentos),
        ]


        # Botão de sair
        botao_sair = ft.Container(
            padding=ft.padding.symmetric(vertical=12, horizontal=10),
            content=ft.Row(
                [
                    ft.Icon(ft.icons.LOGOUT, color="#DC2626", size=24),
                    ft.Text("Sair", size=16, visible=self.sidebar_open, color="#DC2626"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
            ),
            border_radius=8,
            bgcolor="#FEE2E2",
            ink=True,
            on_click=lambda e: print("Logout clicado!"),
            animate=ft.Animation(200, "easeInOut"),
        )

        def on_hover_sair(e):
            botao_sair.bgcolor = "#FCA5A5" if e.data == "true" else "#FEE2E2"
            botao_sair.update()

        botao_sair.on_hover = on_hover_sair

        # Sidebar final com botão "Sair" lá embaixo
        return ft.Container(
            width=240 if self.sidebar_open else 80,
            bgcolor="#F9FAFB",
            border=ft.border.only(right=ft.BorderSide(1, "#E5E7EB")),
            padding=ft.padding.symmetric(vertical=20, horizontal=10),
            content=ft.Column(
                controls=[
                    ft.Column(
                        [
                            ft.Container(
                                alignment=ft.alignment.center,
                                padding=ft.padding.symmetric(vertical=10),
                                content=ft.IconButton(
                                    icon=ft.icons.ARROW_BACK if self.sidebar_open else ft.icons.ARROW_FORWARD,
                                    icon_color="#10B981",
                                    on_click=self.toggle_sidebar,
                                    tooltip="Expandir/Recolher Menu",
                                )
                            ),
                            ft.Divider(thickness=1),
                            *menu_items,
                        ],
                        spacing=8,
                        expand=True  # <- ESSENCIAL para empurrar o sair pra baixo
                    ),
                    botao_sair  # <- agora fixo no final da sidebar
                ],
                expand=True,
                spacing=10,
            )
        )




    def header(self):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20),
            bgcolor="#34D399",
            height=65,
            border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")),
            content=ft.Row([
                ft.Container(expand=True),
                ft.Text("FarmConnect - Painel Principal", size=22, weight="bold", color="#065F46"),
                ft.Container(expand=True),
                ft.Row([
                    ft.IconButton(ft.icons.DARK_MODE_OUTLINED, icon_color="#065F46"),
                    ft.IconButton(ft.icons.SCHEDULE_OUTLINED, icon_color="#065F46"),
                    ft.Text("Bem-vindo!", size=12, color="#065F46"),
                    ft.Text("DESENVOLVIMENTO", size=12, weight="bold", color="#065F46"),
                    ft.IconButton(ft.icons.REFRESH, icon_color="#065F46"),
                ], spacing=10)
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def graph_cards(self):
        return ft.Row([
            ft.Container(
                expand=1,
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                padding=20,
                content=ft.Column([
                    ft.Text("Evolução dos Agendamentos", size=16, weight="bold", color="#065F46"),
                    ft.Container(
                        height=120,
                        bgcolor="#D1FAE5",
                        border_radius=10,
                        alignment=ft.alignment.center,
                        content=ft.Text("Gráfico aqui", size=14, color="#047857")
                    )
                ], spacing=10)
            ),
            ft.Container(
                expand=1,
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                padding=20,
                content=ft.Column([
                    ft.Text("Estoque de Medicamentos (%)", size=16, weight="bold", color="#065F46"),
                    ft.Container(
                        width=100,
                        height=100,
                        bgcolor="#A7F3D0",
                        border_radius=50,
                        alignment=ft.alignment.center,
                        content=ft.Text("80%", size=18, weight="bold", color="#047857")
                    )
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            ),
            ft.Container(
                expand=1,
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                padding=20,
                content=ft.Column([
                    ft.Text("Medicamentos mais solicitados", size=16, weight="bold", color="#065F46"),
                    ft.Column([
                        ft.Row([ft.Container(width=50, height=20, bgcolor="#047857", border_radius=5), ft.Text("Medicamento 1", size=13)], spacing=8),
                        ft.Row([ft.Container(width=45, height=20, bgcolor="#059669", border_radius=5), ft.Text("Medicamento 2", size=13)], spacing=8),
                        ft.Row([ft.Container(width=40, height=20, bgcolor="#10B981", border_radius=5), ft.Text("Medicamento 3", size=13)], spacing=8),
                        ft.Row([ft.Container(width=35, height=20, bgcolor="#3B82F6", border_radius=5), ft.Text("Medicamento 4", size=13)], spacing=8),
                        ft.Row([ft.Container(width=30, height=20, bgcolor="#6366F1", border_radius=5), ft.Text("Medicamento 5", size=13)], spacing=8)
                    ], spacing=6)
                ], spacing=10)
            )
        ], spacing=20)

    def metric_cards(self):
        return ft.Row([
            ft.Container(
                expand=1,
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                padding=20,
                content=ft.Column([
                    ft.Text("Pacientes Cadastrados", size=14, weight="bold", color="#065F46"),
                    ft.Text("0", size=34, weight="bold", color="#111827"),
                    ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                    ft.OutlinedButton("+ Adicionar Paciente", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            ),
            ft.Container(
                expand=1,
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                padding=20,
                content=ft.Column([
                    ft.Text("Agendamentos Hoje", size=14, weight="bold", color="#065F46"),
                    ft.Text("0", size=34, weight="bold", color="#111827"),
                    ft.Text("Valor dinâmico", size=12, color="#10B981"),
                    ft.OutlinedButton("+ Novo Agendamento", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            ),
            ft.Container(
                expand=1,
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                padding=20,
                content=ft.Column([
                    ft.Text("Medicamentos Cadastrados", size=14, weight="bold", color="#065F46"),
                    ft.Text("0", size=34, weight="bold", color="#111827"),
                    ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                    ft.OutlinedButton("+ Adicionar Medicamento", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            )
        ], spacing=20)

    def load_dashboard(self, e=None):
        self.current_view.controls = [
            ft.Container(
                padding=20,
                content=ft.Column([
                    self.graph_cards(),
                    ft.Container(height=20),
                    self.metric_cards()
                ], spacing=20)
            )
        ]
        self.page.update()

    def load_medicamentos(self, e=None, medicamento=None):
        from farmconnect.database import listar_medicamentos

        self.current_view.controls.clear()
        self.editando_medicamento = medicamento is not None

        if medicamento:
            self.medicamento_atual = medicamento

        medicamentos = listar_medicamentos()

        tabela_medicamentos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Fabricante")),
                ft.DataColumn(ft.Text("Estoque")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(med[0]))),  # ID
                        ft.DataCell(ft.Text(med[1])),       # Nome
                        ft.DataCell(ft.Text(med[5] or "-")),# Categoria
                        ft.DataCell(ft.Text(med[6] or "-")),# Fabricante
                        ft.DataCell(ft.Text(str(med[4]))),  # Estoque
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color="#10B981",
                                    tooltip="Editar",
                                    on_click=lambda e, m=med: (
                                        setattr(self, "medicamento_atual", {
                                            "id": m[0],
                                            "nome": m[1],
                                            "descricao": m[2] or "",
                                            "imagem": m[3] or "",
                                            "estoque": m[4],
                                            "categoria": m[5] or "",
                                            "fabricante": m[6] or ""
                                        }),
                                        self.load_medicamentos(medicamento=self.medicamento_atual)
                                    )
                                ),
                                ft.IconButton(icon=ft.icons.DELETE, icon_color="red", tooltip="Excluir")
                            ], spacing=5)
                        ),
                    ]
                ) for med in medicamentos
            ]
        )

        # Campos editáveis
        self.campo_nome = ft.TextField(label="Nome do Medicamento", value=medicamento.get("nome") if medicamento else "")
        self.campo_fabricante = ft.TextField(label="Fabricante", value=medicamento.get("fabricante") if medicamento else "")
        self.campo_categoria = ft.TextField(label="Categoria", value=medicamento.get("categoria") if medicamento else "")
        self.campo_descricao = ft.TextField(label="Descrição", value=medicamento.get("descricao") if medicamento else "")
        self.campo_imagem = ft.TextField(label="Imagem", value=medicamento.get("imagem") if medicamento else "")
        self.campo_estoque = ft.TextField(label="Estoque Atual", keyboard_type=ft.KeyboardType.NUMBER, value=str(medicamento.get("estoque")) if medicamento else "")

        # Painel lateral: Detalhes do medicamento (aparece só se estiver editando)
        detalhes_medicamento = ft.Container(
            bgcolor="white",
            border_radius=12,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=8, color="#E2E8F0"),
            expand=1,
            visible=self.editando_medicamento,
            animate_opacity=300,
            opacity=1.0 if self.editando_medicamento else 0.0,
            content=ft.Column([
                ft.Text("Detalhes do Medicamento", size=20, weight="bold", color="#059669"),
                ft.Divider(),
                self.campo_nome,
                self.campo_fabricante,
                self.campo_categoria,
                self.campo_descricao,
                self.campo_imagem,
                self.campo_estoque,
                ft.TextField(label="Observações", multiline=True, min_lines=3, max_lines=5),
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        bgcolor="#059669",
                        color="white",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=self.salvar_medicamento
                    ),
                    ft.OutlinedButton(
                        "Cancelar",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=lambda e: self.load_medicamentos(),
                    ),
                ], spacing=10),
            ], spacing=12)
        )

        # Interface completa
        self.current_view.controls.append(
            ft.Container(
                padding=25,
                content=ft.Column([
                    ft.Text("Gerenciamento de Medicamentos", size=24, weight="bold", color="#065F46"),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Container(
                            expand=True,
                            content=ft.TextField(
                                hint_text="Buscar medicamento...",
                                prefix_icon=ft.icons.SEARCH,
                                border_radius=30,
                                bgcolor="#FFFFFF",
                                height=50,
                            )
                        ),
                        ft.Container(width=10),
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            bgcolor="#059669",
                            tooltip="Adicionar novo medicamento",
                            on_click=self.load_cadastro_medicamento,
                        ),
                    ]),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Container(
                            expand=2 if not self.editando_medicamento else 1,
                            bgcolor="white",
                            border_radius=12,
                            padding=16,
                            shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                            content=ft.Container(
                                height=420,
                                content=ft.ListView(
                                    controls=[tabela_medicamentos],
                                    auto_scroll=True
                                )
                            )
                        ),
                        ft.Container(width=20),
                        detalhes_medicamento
                    ], spacing=20)
                ], spacing=20)
            )
        )

        self.page.update()

    def salvar_medicamento(self, e=None):
        nome = self.campo_nome.value.strip()
        descricao = self.campo_descricao.value.strip()
        imagem = self.campo_imagem.value.strip()
        estoque_str = self.campo_estoque.value.strip()
        categoria_id = self.campo_categoria.value.strip()
        fabricante_id = self.campo_fabricante.value.strip()

        # Validação
        if not nome:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("O nome do medicamento é obrigatório."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            estoque = int(estoque_str)
        except ValueError:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Estoque deve ser um número válido."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Edição ou adição
        if self.editando_medicamento and hasattr(self, "medicamento_atual"):
            editar_medicamento(
                self.medicamento_atual["id"],
                nome,
                fabricante_id,
                categoria_id,
                descricao,
                imagem,
                estoque
            )
        else:
            adicionar_medicamento(
                nome,
                fabricante_id,
                categoria_id,
                descricao,
                imagem,
                estoque
            )

        # Voltar para lista
        self.load_medicamentos()


    def load_cadastro_medicamento(self, e=None):
        self.current_view.controls.clear()

        # Carregar categorias e fabricantes do banco
        categorias = listar_categorias()
        fabricantes = listar_fabricantes()

        # Dropdowns salvos como atributos para uso posterior
        self.dropdown_categoria = ft.Dropdown(
            label="Categoria",
            border_radius=10,
            bgcolor="#F0FDF4",
            options=[ft.dropdown.Option(str(c[0]), c[1]) for c in categorias],
            expand=True
        )

        self.dropdown_fabricante = ft.Dropdown(
            label="Fabricante",
            border_radius=10,
            bgcolor="#F0FDF4",
            options=[ft.dropdown.Option(str(f[0]), f[1]) for f in fabricantes],
            expand=True
        )

        self.campo_nome = ft.TextField(label="Nome do Medicamento", border_radius=10, bgcolor="#F0FDF4")
        self.campo_estoque = ft.TextField(label="Quantidade em Estoque", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10, bgcolor="#F0FDF4")
        self.campo_observacoes = ft.TextField(label="Observações", multiline=True, min_lines=3, max_lines=5, border_radius=10, bgcolor="#F0FDF4")

        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Text("Cadastrar Novo Medicamento", size=28, weight="bold", color="#059669"),
                        ft.Container(height=20),
                        ft.Container(
                            padding=30,
                            bgcolor="#FFFFFF",
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color="#CBD5E1", offset=ft.Offset(0, 8)),
                            content=ft.Column(
                                [
                                    self.campo_nome,
                                    ft.Row([
                                        self.dropdown_categoria,
                                        ft.IconButton(
                                            icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                            tooltip="Cadastrar nova categoria",
                                            icon_color="#059669",
                                            on_click=self.load_cadastro_categoria
                                        )
                                    ], spacing=10),

                                    ft.Row([
                                        self.dropdown_fabricante,
                                        ft.IconButton(
                                            icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                            tooltip="Cadastrar novo fabricante",
                                            icon_color="#059669",
                                            on_click=self.load_cadastro_fabricante
                                        )
                                    ], spacing=10),

                                    self.campo_estoque,
                                    self.campo_observacoes,
                                    ft.Container(height=20),

                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Salvar Medicamento",
                                                bgcolor="#059669",
                                                color="white",
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                expand=True,
                                                on_click=self.salvar_medicamento  # deve usar a função real
                                            ),
                                            ft.OutlinedButton(
                                                "Cancelar",
                                                expand=True,
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                on_click=lambda e: self.load_medicamentos(),
                                            ),
                                        ],
                                        spacing=20,
                                    )
                                ],
                                spacing=15,
                            ),
                        )
                    ],
                    spacing=20,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        )

        self.page.update()


    def load_cadastro_categoria(self, e=None):
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Cadastrar Nova Categoria", size=26, weight="bold", color="#059669"),
                    ft.Container(height=20),
                    ft.TextField(label="Nome da Categoria", border_radius=10, bgcolor="#F0FDF4"),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Salvar", bgcolor="#059669", color="white", on_click=lambda e: print("Categoria salva!"), expand=True),
                        ft.OutlinedButton("Cancelar", on_click=lambda e: self.load_cadastro_medicamento(), expand=True),
                    ], spacing=20)
                ], spacing=10)
            )
        )
        self.page.update()
    
    def load_cadastro_fabricante(self, e=None):
        from farmconnect.database import adicionar_fabricante

        campo_nome_fabricante = ft.TextField(label="Nome do Fabricante", border_radius=10, bgcolor="#F0FDF4")

        def salvar(e):
            nome = campo_nome_fabricante.value.strip()
            if nome:
                adicionar_fabricante(nome)
                self.load_cadastro_medicamento()
            else:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Nome do fabricante é obrigatório."), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Cadastrar Novo Fabricante", size=26, weight="bold", color="#059669"),
                    ft.Container(height=20),
                    campo_nome_fabricante,
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Salvar", bgcolor="#059669", color="white", on_click=salvar, expand=True),
                        ft.OutlinedButton("Cancelar", on_click=lambda e: self.load_cadastro_medicamento(), expand=True),
                    ], spacing=20)
                ], spacing=10)
            )
        )

        self.page.update()

    
    def load_agendamentos(self, e=None):
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Text(
                            "📅 Agendamentos de Retirada",
                            size=30,
                            weight="bold",
                            color="#059669"
                        ),
                        ft.Text(
                            "Acompanhe os agendamentos feitos pelos pacientes",
                            size=14,
                            color="#6B7280"
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            padding=20,
                            bgcolor="#FFFFFF",
                            border_radius=16,
                            shadow=ft.BoxShadow(blur_radius=12, color="#CBD5E1", offset=ft.Offset(0, 6)),
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Lista de Agendamentos", size=20, weight="bold", color="#111827"),
                                    ft.Container(expand=True),
                                    ft.IconButton(icon=ft.icons.FILTER_LIST, tooltip="Filtrar", icon_color="#059669"),
                                    ft.IconButton(icon=ft.icons.REFRESH, tooltip="Atualizar", icon_color="#059669"),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Divider(height=30),
                                ft.Container(
                                    content=ft.DataTable(
                                        columns=[
                                            ft.DataColumn(ft.Text("ID")),
                                            ft.DataColumn(ft.Text("Paciente")),
                                            ft.DataColumn(ft.Text("Medicamento")),
                                            ft.DataColumn(ft.Text("Código")),
                                            ft.DataColumn(ft.Text("Quantidade")),
                                            ft.DataColumn(ft.Text("Data")),
                                            ft.DataColumn(ft.Text("Horário")),
                                            ft.DataColumn(ft.Text("Status")),
                                            ft.DataColumn(ft.Text("Ações")),
                                        ],
                                        rows=[
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("1")),
                                                    ft.DataCell(ft.Text("Maria da Silva")),
                                                    ft.DataCell(ft.Text("Losartana 50mg")),
                                                    ft.DataCell(ft.Text("MED123456")),
                                                    ft.DataCell(ft.Text("30")),
                                                    ft.DataCell(ft.Text("2025-05-10")),
                                                    ft.DataCell(ft.Text("08:00")),
                                                    ft.DataCell(
                                                        ft.Container(
                                                            content=ft.Text("Pendente", color="#D97706", weight="bold"),
                                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                            bgcolor="#FEF3C7",
                                                            border_radius=6,
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Row([
                                                            ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE, icon_color="#059669", tooltip="Confirmar"),
                                                            ft.IconButton(icon=ft.icons.CANCEL_OUTLINED, icon_color="#DC2626", tooltip="Cancelar")
                                                        ], spacing=4)
                                                    )
                                                ]
                                            ),
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("2")),
                                                    ft.DataCell(ft.Text("João Pereira")),
                                                    ft.DataCell(ft.Text("Paracetamol 500mg")),
                                                    ft.DataCell(ft.Text("MED654321")),
                                                    ft.DataCell(ft.Text("20")),
                                                    ft.DataCell(ft.Text("2025-05-11")),
                                                    ft.DataCell(ft.Text("09:00")),
                                                    ft.DataCell(
                                                        ft.Container(
                                                            content=ft.Text("Confirmado", color="#15803D", weight="bold"),
                                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                            bgcolor="#D1FAE5",
                                                            border_radius=6,
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Row([
                                                            ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE, icon_color="#059669", tooltip="Confirmar"),
                                                            ft.IconButton(icon=ft.icons.CANCEL_OUTLINED, icon_color="#DC2626", tooltip="Cancelar")
                                                        ], spacing=4)
                                                    )
                                                ]
                                            ),
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("3")),
                                                    ft.DataCell(ft.Text("Ana Clara")),
                                                    ft.DataCell(ft.Text("Ibuprofeno 400mg")),
                                                    ft.DataCell(ft.Text("MED789012")),
                                                    ft.DataCell(ft.Text("15")),
                                                    ft.DataCell(ft.Text("2025-05-12")),
                                                    ft.DataCell(ft.Text("10:00")),
                                                    ft.DataCell(
                                                        ft.Container(
                                                            content=ft.Text("Cancelado", color="#DC2626", weight="bold"),
                                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                            bgcolor="#FEE2E2",
                                                            border_radius=6,
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Row([
                                                            ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE, icon_color="#059669", tooltip="Confirmar"),
                                                            ft.IconButton(icon=ft.icons.CANCEL_OUTLINED, icon_color="#DC2626", tooltip="Cancelar")
                                                        ], spacing=4)
                                                    )
                                                ]
                                            ),
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("4")),
                                                    ft.DataCell(ft.Text("Lucas Martins")),
                                                    ft.DataCell(ft.Text("Amoxicilina 500mg")),
                                                    ft.DataCell(ft.Text("MED345678")),
                                                    ft.DataCell(ft.Text("25")),
                                                    ft.DataCell(ft.Text("2025-05-13")),
                                                    ft.DataCell(ft.Text("11:00")),
                                                    ft.DataCell(
                                                        ft.Container(
                                                            content=ft.Text("Concluído", color="#047857", weight="bold"),
                                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                            bgcolor="#D1FAE5",
                                                            border_radius=6,
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Row([
                                                            ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE, icon_color="#059669", tooltip="Confirmar"),
                                                            ft.IconButton(icon=ft.icons.CANCEL_OUTLINED, icon_color="#DC2626", tooltip="Cancelar")
                                                        ], spacing=4)
                                                    )
                                                ]
                                            ),
                                            ft.DataRow(
                                                cells=[
                                                    ft.DataCell(ft.Text("5")),
                                                    ft.DataCell(ft.Text("Fernanda Lima")),
                                                    ft.DataCell(ft.Text("Cetirizina 10mg")),
                                                    ft.DataCell(ft.Text("MED987654")),
                                                    ft.DataCell(ft.Text("50")),
                                                    ft.DataCell(ft.Text("2025-05-14")),
                                                    ft.DataCell(ft.Text("12:00")),
                                                    ft.DataCell(
                                                        ft.Container(
                                                            content=ft.Text("Pendente", color="#D97706", weight="bold"),
                                                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                                            bgcolor="#FEF3C7",
                                                            border_radius=6,
                                                        )
                                                    ),
                                                    ft.DataCell(
                                                        ft.Row([
                                                            ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE, icon_color="#059669", tooltip="Confirmar"),
                                                            ft.IconButton(icon=ft.icons.CANCEL_OUTLINED, icon_color="#DC2626", tooltip="Cancelar")
                                                        ], spacing=4)
                                                    )
                                                ]
                                            ),
                                        ],
                                        heading_row_color="#F9FAFB",
                                        border=ft.border.all(1, "#E5E7EB"),
                                        border_radius=8,
                                    ),
                                    expand=True
                                )
                            ], spacing=16)
                        )
                    ],
                    spacing=16
                )
            )
        )
        self.page.update()


    def build_tela(self):
        return ft.View(
        route="/admin_dashboard",
        controls=[
            ft.Row([
                self.side_menu(),
                ft.Column([
                    self.header(),
                    self.current_view
                ], expand=True)
            ], expand=True)
        ],
        scroll=ft.ScrollMode.ADAPTIVE
    )

if __name__ == "__main__":
    def main(page: ft.Page):
        app = TelaAdminDashboard(page)
        page.views.append(app.build_tela()) # app.build_tela()
        page.update()

    ft.app(target=main)
