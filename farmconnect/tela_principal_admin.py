import flet as ft
from database import listar_medicamentos, editar_medicamento, adicionar_medicamento, listar_categorias, listar_fabricantes, desativar_medicamento, adicionar_farmacia, listar_farmacias, deletar_farmacia, editar_farmacia, listar_usuarios, registrar_usuario, aprovar_usuario, recusar_usuario, listar_agendamentos, adicionar_agendamento, reativar_medicamento, adicionar_estoque
from datetime import datetime
from collections import Counter
import calendar

class TelaAdminDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page_settings()
        self.sidebar_open = True
        self.current_view = ft.Column(expand=True)
        self.load_dashboard()  
        self.tabela_agendamentos_ref = ft.Ref[ft.DataTable]()
        self.tabela_pacientes_ref = ft.Ref[ft.DataTable]()
        self.tabela_medicamentos_ref = ft.Ref[ft.DataTable]()
        self.tabela_farmacias_ref = ft.Ref[ft.DataTable]()

    def page_settings(self):
        self.page.title = "FarmConnect - Painel Admin"
        self.page.bgcolor = "#EFF6FF"
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def toggle_sidebar(self, e):
        self.sidebar_open = not self.sidebar_open
        self.page.update()

    def count_agendamentos_do_dia(self):
        hoje = datetime.now().date()
        agendamentos = listar_agendamentos()
        total_hoje = sum(1 for a in agendamentos if a[5] == hoje.strftime("%Y-%m-%d"))
        return total_hoje
    
    def desativar_medicamento(self, id):
        desativar_medicamento(id)
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Medicamento desativado."), bgcolor="red")
        self.page.snack_bar.open = True
        self.page.update()
        self.load_medicamentos()

    def reativar_medicamento(self, id):
        reativar_medicamento(id)
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Medicamento reativado."), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()
        self.load_medicamentos()
    
    def card_estoque_medicamentos(self):
        medicamentos = listar_medicamentos(include_inativos=False)
        total_estoque = sum([m[5] or 0 for m in medicamentos]) # m[5] = estoque
        abaixo_limite = [(m[1], m[5] or 0) for m in medicamentos if (m[5] or 0) < 5]  # m[1] = nome

        if not medicamentos: # Nenhum medicamento ativo no banco
            return ft.Container(
                col={"sm": 12, "md": 4},
                bgcolor="#FFFFFF",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                padding=20,
                content=ft.Column([
                    ft.Text("Estoque de Medicamentos", size=16, weight="bold", color="#111827"),
                    ft.Text("Nenhum medicamento ativo.", size=14, color=ft.Colors.RED_700),
                ], spacing=10)
            )

        lista_criticos = ft.Column(
            controls=[
                ft.Text(f"- {nome} ({qtd} un.)", size=12, color=ft.Colors.RED_700)
                for nome, qtd in abaixo_limite
            ],
            spacing=4
        ) if abaixo_limite else ft.Text("✔️ Estoque suficiente", size=12, color=ft.Colors.GREEN_700) 

        return ft.Container(
            col={"sm": 12, "md": 4},
            bgcolor="#FFFFFF",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
            padding=20,
            content=ft.Column([
                ft.Text("Estoque de Medicamentos", size=16, weight="bold", color="#111827"),
                ft.Text(f"Total em estoque: {total_estoque} unidades", size=14, weight="bold", color="#1E3A8A"),
                ft.Text("Medicamentos críticos (< 5 un.):", size=13, color="#6B7280"),
                lista_criticos
            ], spacing=10)
        )

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
            item.bgcolor = "#d1eefa" if e.data == "true" else "#FFFFFF"
            item.update()
        item.on_hover = on_hover
        return item

    def side_menu(self):
        def create_menu_item(icon, text, on_click=None):
            container = ft.Container(
                padding=ft.padding.symmetric(vertical=12, horizontal=10),
                content=ft.Row(
                    [
                        ft.Icon(icon, color=ft.Colors.BLUE_600, size=24),
                        ft.Text(text, size=16, visible=self.sidebar_open, color="#111827"),
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
                container.bgcolor = "#d1eefa" if e.data == "true" else "#FFFFFF"
                container.update()

            container.on_hover = on_hover
            return container

        # Itens do menu
        menu_items = [
            create_menu_item(ft.Icons.HOME_OUTLINED, "Início", self.load_dashboard),
            create_menu_item(ft.Icons.CALENDAR_MONTH_OUTLINED, "Agendamentos", self.load_agendamentos),  # <- AQUI
            create_menu_item(ft.Icons.LOCAL_HOSPITAL_OUTLINED, "Farmácias", self.load_farmacias),
            create_menu_item(ft.Icons.MEDICAL_SERVICES_OUTLINED, "Medicamentos", self.load_medicamentos),
            create_menu_item(ft.Icons.PERSON_OUTLINED, "Pacientes", self.load_pacientes),
        ]

        # Botão de sair
        botao_sair = ft.Container(
            padding=ft.padding.symmetric(vertical=12, horizontal=10),
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGOUT, color="#DC2626", size=24),
                    ft.Text("Sair", size=16, visible=self.sidebar_open, color="#DC2626"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
            ),
            border_radius=8,
            bgcolor="#FEE2E2",
            ink=True,
            on_click=lambda e: self.page.go("/escolha_usuario"),
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
                                    icon=ft.Icons.ARROW_BACK_IOS_NEW if self.sidebar_open else ft.Icons.ARROW_FORWARD_IOS,
                                    icon_color=ft.Colors.BLUE_600,
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
            padding=ft.padding.symmetric(horizontal=20, vertical=14),
            bgcolor="white",
            border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")),
            content=ft.ResponsiveRow(
                columns=12,
                spacing=10,
                run_spacing=10,
                controls=[
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        alignment=ft.alignment.center_left,
                        content=ft.Text(
                            "FarmConnect - Painel de Controle",
                            size=22,
                            weight="bold",
                            color=ft.Colors.BLUE_900,
                            text_align=ft.TextAlign.START
                        )
                    ),
                    ft.Container(
                        col={"sm": 12, "md": 6},
                        alignment=ft.alignment.center_right,
                        content=ft.Column([
                            ft.Row(
                                wrap=True,
                                spacing=10,
                                controls=[
                                    ft.IconButton(ft.Icons.DARK_MODE_OUTLINED, icon_color=ft.Colors.BLUE_900),
                                    ft.IconButton(ft.Icons.SCHEDULE_OUTLINED, icon_color=ft.Colors.BLUE_900),
                                    ft.Text("Bem-vindo!", size=12, color=ft.Colors.BLUE_900),
                                    ft.Text("DESENVOLVIMENTO", size=12, weight="bold", color=ft.Colors.BLUE_900),
                                    ft.IconButton(ft.Icons.REFRESH, icon_color=ft.Colors.BLUE_900),
                                ]
                            )
                        ])
                    )
                ]
            )
        )

    def graph_cards(self):
        return ft.ResponsiveRow(
            columns=12,
            spacing=20,
            controls=[

                # Card do gráfico com botão de atualizar
                ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                    padding=20,
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Evolução dos Agendamentos", size=16, weight="bold", color="#111827"),
                            ft.Container(expand=True),
                            ft.IconButton(
                                icon=ft.Icons.REFRESH,
                                tooltip="Atualizar Gráfico",
                                icon_color=ft.Colors.BLUE_600,
                                on_click=lambda e: self.load_dashboard()
                            )
                        ]),
                        self.gerar_grafico_agendamentos_semanais()
                    ], spacing=10)
                ),

                self.card_estoque_medicamentos(),

                ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                    padding=20,
                    content=ft.Column([
                        ft.Text("Medicamentos mais solicitados", size=16, weight="bold", color="#111827"),
                        ft.Column([
                            ft.Row([ft.Container(width=50, height=20, bgcolor="#047857", border_radius=5), ft.Text("Medicamento 1", size=13)], spacing=8),
                            ft.Row([ft.Container(width=45, height=20, bgcolor="#059669", border_radius=5), ft.Text("Medicamento 2", size=13)], spacing=8),
                            ft.Row([ft.Container(width=40, height=20, bgcolor="#10B981", border_radius=5), ft.Text("Medicamento 3", size=13)], spacing=8),
                            ft.Row([ft.Container(width=35, height=20, bgcolor="#3B82F6", border_radius=5), ft.Text("Medicamento 4", size=13)], spacing=8),
                            ft.Row([ft.Container(width=30, height=20, bgcolor="#6366F1", border_radius=5), ft.Text("Medicamento 5", size=13)], spacing=8)
                        ], spacing=6)
                    ], spacing=10)
                )
            ]
        )

    def metric_cards(self):
        return ft.ResponsiveRow(
            columns=12,
            spacing=20,
            controls=[
                ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                    padding=20,
                    content=ft.Column([
                        ft.Text("Pacientes Cadastrados", size=14, weight="bold", color="#111827"),
                        ft.Text(len(listar_usuarios()), size=34, weight="bold", color="#111827"),
                        ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                        ft.OutlinedButton("+ Adicionar Paciente", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=self.load_cadastro_paciente)
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                ),
                ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                    padding=20,
                    content=ft.Column([
                        ft.Text("Agendamentos Hoje", size=14, weight="bold"),
                        ft.Text(str(self.count_agendamentos_do_dia()), size=34, weight="bold", color="#111827"),
                        ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                        ft.OutlinedButton(
                            "+ Novo Agendamento",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=self.load_cadastro_agendamento  # <- Aqui você adiciona a função
                        )
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                ),
                ft.Container(
                    col={"sm": 12, "md": 4},
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26),
                    padding=20,
                    content=ft.Column([
                        ft.Text("Medicamentos Cadastrados", size=14, weight="bold", color="#111827"),
                        ft.Text(len(listar_medicamentos()), size=34, weight="bold", color="#111827"),
                        ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                        ft.OutlinedButton(
                            "+ Adicionar Medicamento",
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                            on_click=self.load_cadastro_medicamento  # <- Aqui você adiciona a função
                        )
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                )
            ]
        )

    def load_dashboard(self, e=None):
        self.current_view.controls = [
            ft.Container(
                padding=20,
                content=ft.Column([
                    self.graph_cards(),
                    ft.Container(height=20),
                    self.metric_cards(),
                    ft.Container(height=40),

                    # Botão no final da página
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=20,
                        content=ft.ElevatedButton(
                            text="Baixar Relatório",
                            icon=ft.Icons.DOWNLOAD,
                            bgcolor=ft.Colors.BLUE_300,
                            color=ft.Colors.WHITE,
                            height=55,
                            width=260,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=14),
                                padding=ft.padding.symmetric(vertical=12),
                                elevation=6
                            ),
                            on_click=lambda e: print("Botão de relatório clicado")
                        )
                    )
                ], spacing=20)
            )
        ]
        self.page.update()

    def gerar_rows_medicamentos(self, lista):
        rows = []
        for med in lista:
            inativo = med[8] == 0  # Supondo que a posição 8 indica ativo/inativo
            cor = "red" if inativo else None

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(med[0]), color=cor)),  # ID
                        ft.DataCell(ft.Text(med[1], color=cor)),       # Nome
                        ft.DataCell(ft.Text(med[2] or "-", color=cor)),# Código
                        ft.DataCell(ft.Text(med[6] or "-", color=cor)),# Categoria
                        ft.DataCell(ft.Text(med[7] or "-", color=cor)),# Fabricante
                        ft.DataCell(ft.Text(med[8] or "-", color=cor)),# Farmácia
                        ft.DataCell(ft.Text(str(med[5] or 0), color=cor)),  # Estoque
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.LOCK_OPEN if inativo else ft.Icons.CANCEL_OUTLINED,
                                icon_color=ft.Colors.GREEN_400 if inativo else ft.Colors.RED,
                                tooltip="Reativar" if inativo else "Desativar",
                                icon_size=22,
                                style=ft.ButtonStyle(padding=0),
                                on_click=lambda e, id=med[0]: (
                                    self.reativar_medicamento(id) if inativo else self.desativar_medicamento(id)
                                )
                            )
                        )
                    ]
                )
            )
        return rows

    def load_medicamentos(self, e=None, medicamento=None):

        self.current_view.controls.clear()
        self.editando_medicamento = medicamento is not None

        if not hasattr(self, "cancelados"):
            self.cancelados = set()

        categorias = listar_categorias()
        fabricantes = listar_fabricantes()

        if medicamento:
            self.medicamento_atual = medicamento

        medicamentos = listar_medicamentos()

        self.campo_busca_medicamento = ft.TextField(
                                        hint_text="Buscar medicamento...",
                                        prefix_icon=ft.Icons.SEARCH,
                                        border_radius=30,
                                        bgcolor="#F9FAFB",
                                        height=50,
                                        on_change=self.filtrar_medicamentos,
                                    )

        self.tabela_medicamentos = ft.DataTable(
            ref=self.tabela_medicamentos_ref,
            heading_row_color="#F9FAFB",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Categoria")),
                ft.DataColumn(ft.Text("Fabricante")),
                ft.DataColumn(ft.Text("Farmácia")),
                ft.DataColumn(ft.Text("Estoque")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=self.gerar_rows_medicamentos(medicamentos)
        )

        # Painel lateral opcional (se estiver editando)
        self.campo_nome = ft.TextField(label="Nome do Medicamento", value=medicamento.get("nome") if medicamento else "")
        self.campo_codigo = ft.TextField(label="Código do Medicamento", value=medicamento.get("codigo") if medicamento else "")
        self.dropdown_fabricante = ft.Dropdown(
            label="Fabricante",
            border_radius=10,
            bgcolor="#F0FDF4",
            options=[ft.dropdown.Option(str(f[0]), f[1]) for f in fabricantes],
            value=str(medicamento.get("fabricante_id")) if medicamento else None,
            expand=True
        )
        self.dropdown_categoria = ft.Dropdown(
            label="Categoria",
            border_radius=10,
            bgcolor="#F0FDF4",
            options=[ft.dropdown.Option(str(c[0]), c[1]) for c in categorias],
            value=str(medicamento.get("categoria_id")) if medicamento else None,
            expand=True
        )
        self.campo_descricao = ft.TextField(label="Descrição", value=medicamento.get("descricao") if medicamento else "")
        self.campo_imagem = ft.TextField(label="URL da Imagem", value=medicamento.get("imagem") if medicamento else "", border_radius=10)
        self.campo_estoque = ft.TextField(label="Estoque Atual", keyboard_type=ft.KeyboardType.NUMBER, value=str(medicamento.get("estoque")) if medicamento else "")

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
                self.campo_codigo,
                self.dropdown_fabricante,
                self.dropdown_categoria,
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

        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.Icons.LOCAL_PHARMACY, size=40, color=ft.Colors.BLUE_600),
                        ft.Text("Gerenciamento de Medicamentos", size=32, weight="bold", color=ft.Colors.BLUE_900),
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text(
                        "Adicione, edite ou remova medicamentos disponíveis no sistema.",
                        size=14,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(height=30),

                    ft.Container(
                        bgcolor="#FFFFFF",
                        border_radius=20,
                        padding=25,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📋 Lista de Medicamentos", size=20, weight="bold", color="#111827"),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    tooltip="Atualizar",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=self.load_medicamentos
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    tooltip="Adicionar novo medicamento",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=self.load_cadastro_medicamento
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(),
                            ft.Row([
                                ft.Container(
                                    expand=True,
                                    content=self.campo_busca_medicamento
                                    )
                            ]),
                            ft.Container(height=20),

                            ft.ResponsiveRow(
                                
                                columns=12,
                                spacing=20,
                                run_spacing=20,
                                controls=[
                                    ft.Container(
                                        col={"sm": 12, "md": 12},
                                        expand=True,
                                        content=ft.Row(
                                            scroll=ft.ScrollMode.ALWAYS,
                                            controls = [
                                                ft.Container(
                                                    content=self.tabela_medicamentos,
                                                    width=1000
                                                )
                                            ],
                                        )
                                    ),
                                    ft.Container(
                                        col={"sm": 12, "md": 4},
                                        content=detalhes_medicamento
                                    )
                                ]
                            )
                        ], spacing=20)
                    )
                ], spacing=20)
            )
        )

        self.page.update()

    def filtrar_medicamentos(self, e):
        termo = self.campo_busca_medicamento.value.strip().lower()
        medicamentos = listar_medicamentos()
        resultado = [
            m for m in medicamentos
            if termo in (m[1] or "").lower() or termo in (m[2] or "").lower()
        ]

        self.tabela_medicamentos_ref.current.rows = self.gerar_rows_medicamentos(resultado)
        self.tabela_medicamentos_ref.current.update()

    def salvar_medicamento(self, e=None):
        nome = self.campo_nome.value.strip()
        codigo = self.campo_codigo.value.strip()
        descricao = self.campo_descricao.value.strip()
        imagem = self.campo_imagem.value.strip()
        estoque_str = self.campo_estoque.value.strip()
        
        categoria_id = int(self.dropdown_categoria.value) if self.dropdown_categoria.value else None
        fabricante_id = int(self.dropdown_fabricante.value) if self.dropdown_fabricante.value else None

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
                nome=nome,
                codigo=codigo,
                descricao=descricao,
                imagem=imagem,
                estoque=estoque,
                categoria_id=categoria_id,
                fabricante_id=fabricante_id
            )
        else:
            farmacia_id = int(self.dropdown_farmacia.value) if self.dropdown_farmacia.value else None

            if not farmacia_id:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Você deve selecionar uma farmácia."), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()
                return

            # 1. Cadastra o medicamento e pega o ID
            id_medicamento = adicionar_medicamento(
                nome=nome,
                codigo=codigo,
                descricao=descricao,
                imagem=imagem,
                estoque=estoque,
                categoria_id=categoria_id,
                fabricante_id=fabricante_id,
            )

            # 2. Relaciona ao estoque da farmácia
            adicionar_estoque(farmacia_id, id_medicamento, estoque)

        # Voltar para lista
        self.load_medicamentos()


    def load_cadastro_medicamento(self, e=None):
        self.editando_medicamento = False
        self.current_view.controls.clear()

        # Carregar categorias e fabricantes do banco
        categorias = listar_categorias()
        fabricantes = listar_fabricantes()
        farmacias = listar_farmacias()

        # Dropdowns salvos como atributos para uso posterior
        self.dropdown_categoria = ft.Dropdown(
            label="Categoria",
            border_radius=10,
            bgcolor="#F9FAFB",
            options=[ft.dropdown.Option(str(c[0]), c[1]) for c in categorias],
            expand=True
        )

        self.dropdown_fabricante = ft.Dropdown(
            label="Fabricante",
            border_radius=10,
            bgcolor="#F9FAFB",
            options=[ft.dropdown.Option(str(f[0]), f[1]) for f in fabricantes],
            expand=True
        )

        self.dropdown_farmacia = ft.Dropdown(
            label="Farmácia",
            options=[ft.dropdown.Option(str(f[0]), f[1]) for f in farmacias],
            border_radius=10,
            bgcolor="#F9FAFB",
            expand=True
        )

        self.campo_nome = ft.TextField(label="Nome do Medicamento", border_radius=10, bgcolor="#F9FAFB")
        self.campo_codigo = ft.TextField(label="Código do Medicamento", border_radius=10, bgcolor="#F9FAFB")
        self.campo_estoque = ft.TextField(label="Quantidade em Estoque", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10, bgcolor="#F9FAFB")
        self.campo_descricao = ft.TextField(label="Descrição do Medicamento", border_radius=10, bgcolor="#F9FAFB")
        self.campo_imagem = ft.TextField(label="URL da Imagem", border_radius=10, bgcolor="#F9FAFB")
        self.campo_observacoes = ft.TextField(label="Observações", multiline=True, min_lines=3, max_lines=5, border_radius=10, bgcolor="#F9FAFB")

        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Text("Cadastrar Novo Medicamento", size=28, weight="bold", color=ft.Colors.BLUE_900),
                        ft.Container(height=20),
                        ft.Container(
                            padding=30,
                            bgcolor="#FFFFFF",
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color="#CBD5E1", offset=ft.Offset(0, 8)),
                            content=ft.Column(
                                [
                                    self.campo_nome,
                                    self.campo_codigo,
                                    self.campo_descricao,
                                    ft.Row([
                                        self.dropdown_categoria,
                                        ft.IconButton(
                                            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                            tooltip="Cadastrar nova categoria",
                                            icon_color=ft.Colors.BLUE_900,
                                            on_click=self.load_cadastro_categoria
                                        )
                                    ], spacing=10),

                                    ft.Row([
                                        self.dropdown_fabricante,
                                        ft.IconButton(
                                            icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                                            tooltip="Cadastrar novo fabricante",
                                            icon_color=ft.Colors.BLUE_900,
                                            on_click=self.load_cadastro_fabricante
                                        )
                                    ], spacing=10),
                                    self.dropdown_farmacia,
                                    self.campo_estoque,
                                    self.campo_imagem,
                                    self.campo_observacoes,
                                    ft.Container(height=20),

                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Salvar Medicamento",
                                                bgcolor=ft.Colors.BLUE_600,
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
        from database import adicionar_categoria

        campo_nome_categoria = ft.TextField(label="Nome da Categoria", border_radius=10, bgcolor="#F9FAFB")

        def salvar(e):
            nome = campo_nome_categoria.value.strip()
            if nome:
                adicionar_categoria(nome)
                self.load_cadastro_medicamento()
            else:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Nome da categoria é obrigatório"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Cadastrar Nova Categoria", size=26, weight="bold", color=ft.Colors.BLUE_900),
                    ft.Container(height=20),
                    campo_nome_categoria,
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Salvar", bgcolor=ft.Colors.BLUE_600, color="white", on_click=salvar, expand=True),
                        ft.OutlinedButton("Cancelar", on_click=lambda e: self.load_cadastro_medicamento(), expand=True),
                    ], spacing=20)
                ], spacing=10)
            )
        )

        self.page.update()

    
    def load_cadastro_fabricante(self, e=None):
        from database import adicionar_fabricante

        campo_nome_fabricante = ft.TextField(label="Nome do Fabricante", border_radius=10, bgcolor="#F9FAFB")

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
                    ft.Text("Cadastrar Novo Fabricante", size=26, weight="bold", color=ft.Colors.BLUE_900),
                    ft.Container(height=20),
                    campo_nome_fabricante,
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Salvar", bgcolor=ft.Colors.BLUE_600, color="white", on_click=salvar, expand=True),
                        ft.OutlinedButton("Cancelar", on_click=lambda e: self.load_cadastro_medicamento(), expand=True),
                    ], spacing=20)
                ], spacing=10)
            )
        )

        self.page.update()

    
    def load_agendamentos(self, e=None, agendamento=None):
        self.current_view.controls.clear()
        self.editando_agendamento = agendamento is not None
        self.agendamento_atual = agendamento if agendamento else None

        # Buscar farmácias do banco de dados
        agendamentos_db = listar_agendamentos()
        print("Agendamentos encontrados:", agendamentos_db)
        
        # Campos de edição
        self.campo_busca_agendamentos = ft.TextField(
            hint_text="Buscar agendamentos...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=30,
            bgcolor="#F9FAFB",
            height=50,
            on_change=self.filtrar_agendamentos
        )
        
        self.current_view.controls.clear()

        # Campos do formulário
        self.campo_paciente = ft.TextField(label="Nome do Paciente", border_radius=10, bgcolor="#F9FAFB")
        self.campo_medicamento = ft.TextField(label="Nome do Medicamento", border_radius=10, bgcolor="#F9FAFB")
        self.campo_codigo = ft.TextField(label="Código do Medicamento", border_radius=10, bgcolor="#F9FAFB")
        self.campo_quantidade = ft.TextField(label="Quantidade", border_radius=10, bgcolor="#F9FAFB", keyboard_type=ft.KeyboardType.NUMBER)
        self.campo_data = ft.TextField(label="Data (AAAA-MM-DD)", border_radius=10, bgcolor="#F9FAFB")
        self.campo_horario = ft.TextField(label="Horário (HH:MM)", border_radius=10, bgcolor="#F9FAFB")

        # Painel lateral de edição
        self.painel_detalhes_agendamento = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            visible=self.editando_agendamento,
            animate_opacity=300,
            opacity=1.0 if self.editando_agendamento else 0.0,
            expand=1,
            content=ft.Column([
                ft.Text("🏥 Editar Agendamento", size=20, weight="bold", color=ft.Colors.BLUE_900),
                ft.Divider(),
                self.campo_paciente,
                self.campo_medicamento,
                self.campo_codigo,
                self.campo_quantidade,
                self.campo_data,
                self.campo_horario,
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        bgcolor=ft.Colors.BLUE_600,
                        color="white",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=self.salvar_agendamento  # Novo método para salvar
                    ),
                    ft.OutlinedButton(
                        "Cancelar",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=lambda e: self.load_agendamentos()
                    )
                ], spacing=10)
            ], spacing=12)
        )

        # Renderiza a tabela com farmácias do banco
        self.renderizar_tabela_agendamentos(agendamentos_db)

    def gerar_rows_agendamentos(self, lista):
        status_cores = {
            "Pendente": ("#D97706", "#FEF3C7"),
            "Confirmado": ("#15803D", "#D1FAE5"),
            "Cancelado": ("#DC2626", "#FEE2E2"),
            "Concluído": ("#047857", "#D1FAE5")
        }

        def status_badge(status):
            cor_texto, cor_fundo = status_cores.get(status, ("#6B7280", "#E5E7EB"))
            return ft.Row([
                ft.Container(width=8, height=8, bgcolor=cor_texto, border_radius=20),
                ft.Text(status, color=cor_texto, weight="bold")
            ], spacing=6, alignment=ft.MainAxisAlignment.CENTER)
        
        rows = []
        for a in lista:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(a[0]))),
                        ft.DataCell(ft.Text(a[1])),
                        ft.DataCell(ft.Text(a[2])),
                        ft.DataCell(ft.Text(a[3])),  
                        ft.DataCell(ft.Text(a[4])),
                        ft.DataCell(ft.Text(a[5])),
                        ft.DataCell(ft.Text(a[6])),
                        ft.DataCell(
                            ft.Container(
                                content=status_badge(a[7]),
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                bgcolor=status_cores.get(a[7], "#E5E7EB"),
                                border_radius=20,
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                width=100,
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                                            icon_color="#059669",
                                            tooltip="Confirmar Agendamento",
                                            icon_size=20,
                                            style=ft.ButtonStyle(
                                                padding=ft.padding.all(0),
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            )
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CANCEL_OUTLINED,
                                            icon_color="#DC2626",
                                            tooltip="Cancelar Agendamento",
                                            icon_size=20,
                                            style=ft.ButtonStyle(
                                                padding=ft.padding.all(0),
                                                shape=ft.RoundedRectangleBorder(radius=8),
                                            )
                                        )
                                    ],
                                    spacing=8,
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                            )
                        )
                    ]
                )
            )

        return rows


    def renderizar_tabela_agendamentos(self, lista):
        self.tabela_agendamentos = ft.DataTable(
            ref=self.tabela_agendamentos_ref,
            heading_row_color="#F9FAFB",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Paciente")),
                ft.DataColumn(ft.Text("Medicamento")),
                ft.DataColumn(ft.Text("Farmácia")),
                ft.DataColumn(ft.Text("Código")),
                ft.DataColumn(ft.Text("Data")),
                ft.DataColumn(ft.Text("Horário")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=self.gerar_rows_agendamentos(lista)
        )

        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.Icons.LOCAL_HOSPITAL, size=40, color=ft.Colors.BLUE_600),
                        ft.Text("Gerenciamento de Agendamentos", size=32, weight="bold", color=ft.Colors.BLUE_900)
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Adicione, edite ou gerencie os agendamentos cadastrados no sistema.",
                            size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30),

                   ft.Container(
                        bgcolor="#FFFFFF",
                        border_radius=20,
                        padding=25,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📋 Lista de Agendamentos", size=20, weight="bold", color="#111827"),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    tooltip="Atualizar",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=self.load_agendamentos
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    tooltip="Adicionar novo agendamento",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=self.load_cadastro_agendamento
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(),
                            ft.Row([
                                ft.Container(
                                    expand=True,
                                    content=self.campo_busca_agendamentos
                                )
                            ]),
                            ft.Container(height=20),
                            ft.Container(
                                content=self.tabela_agendamentos,
                                expand=True,
                                width=1200
                            )
                        ], spacing=20)
                    )
                ], spacing=20)
            )
        )

        self.page.update()

    def cnpj_change(self, e):
        texto_original = self.campo_cnpj.value
        numeros = ''.join(filter(str.isdigit, texto_original))[:14]

        if len(numeros) == 14:
            self.campo_cidade.focus()

    def cnpj_blur(self, e):
        texto_original = self.campo_cnpj.value
        numeros = ''.join(filter(str.isdigit, texto_original))[:14]
        formatado = ""

        if len(numeros) >= 2:
            formatado += numeros[:2] + "."
        if len(numeros) >= 5:
            formatado += numeros[2:5] + "."
        if len(numeros) >= 8:
            formatado += numeros[5:8] + "/"
        if len(numeros) >= 12:
            formatado += numeros[8:12] + "-"
        if len(numeros) > 12:
            formatado += numeros[12:]

        self.campo_cnpj.value = formatado
        self.campo_cnpj.update()
    
    def telefone_change(self, e):
        texto_original = self.campo_telefone.value
        numeros = ''.join(filter(str.isdigit, texto_original))[:13]

        if len(numeros) == 13:
            self.campo_telefone.focus()

    def telefone_blur(self, e):
        texto_original = self.campo_telefone.value
        numeros = ''.join(filter(str.isdigit, texto_original))[:11]
        formatado = ""

        if len(numeros) >= 1:
            formatado += "(" + numeros[:2] + ") "
        if len(numeros) >= 7:
            formatado += numeros[2:7] + "-"
        if len(numeros) > 7:
            formatado += numeros[7:]
        elif len(numeros) > 2:
            formatado += numeros[2:7]

        self.campo_telefone.value = formatado
        self.campo_telefone.update()

    def salvar_farmacia(self, e=None):
        nome = self.campo_nome_f.value.strip()
        cnpj = self.campo_cnpj.value.strip()
        endereco = self.campo_endereco.value.strip()
        cidade = self.campo_cidade.value.strip()
        estado = self.campo_estado.value.strip()
        telefone = self.campo_telefone.value.strip()

        if not all([nome, cnpj, endereco, cidade, estado, telefone]):
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Todos os campos são obrigatórios."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        if self.editando_farmacia and self.farmacia_atual:
            editar_farmacia(
                self.farmacia_atual["id"],
                nome=nome,
                endereco=endereco,
                cnpj=cnpj,
                cidade=cidade,
                estado=estado,
                telefone=telefone
            )
            mensagem = "Farmácia atualizada com sucesso."
        else:
            adicionar_farmacia(
                nome=nome,
                endereco=endereco,
                cnpj=cnpj,
                cidade=cidade,
                estado=estado,
                telefone=telefone
            )
            mensagem = "Farmácia adicionada com sucesso."

        self.page.snack_bar = ft.SnackBar(content=ft.Text(mensagem), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()
        self.load_farmacias()

    def load_farmacias(self, e=None, farmacia=None):
        self.current_view.controls.clear()
        self.editando_farmacia = farmacia is not None
        self.farmacia_atual = farmacia if farmacia else None

        # Buscar farmácias do banco de dados
        farmacias_db = listar_farmacias()
        
        # Campos de edição
        self.campo_busca_farmacia = ft.TextField(
            hint_text="Buscar farmácia...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=30,
            bgcolor="#F9FAFB",
            height=50,
            on_change=self.filtrar_farmacias
        )

        self.campo_nome_f = ft.TextField(label="Nome da Farmácia", value=farmacia["nome"] if farmacia else "")
        self.campo_endereco = ft.TextField(label="Endereço da Farmácia", value=farmacia["endereco"] if farmacia else "")
        self.campo_cnpj = ft.TextField(label="CNPJ", on_blur=self.cnpj_blur, on_change=self.cnpj_change, value=farmacia["cnpj"] if farmacia else "")
        self.campo_cidade = ft.TextField(label="Cidade", value=farmacia["cidade"] if farmacia else "")
        self.campo_estado = ft.Dropdown(
                            label="Estado",
                            options=[
                                ft.dropdown.Option("AC", "AC"),
                                ft.dropdown.Option("AL", "AL"),
                                ft.dropdown.Option("AP", "AP"),
                                ft.dropdown.Option("AM", "AM"),
                                ft.dropdown.Option("BA", "BA"),
                                ft.dropdown.Option("CE", "CE"),
                                ft.dropdown.Option("DF", "DF"),
                                ft.dropdown.Option("ES", "ES"),
                                ft.dropdown.Option("GO", "GO"),
                                ft.dropdown.Option("MA", "MA"),
                                ft.dropdown.Option("MT", "MT"),
                                ft.dropdown.Option("MS", "MS"),
                                ft.dropdown.Option("MG", "MG"),
                                ft.dropdown.Option("PA", "PA"),
                                ft.dropdown.Option("PB", "PB"),
                                ft.dropdown.Option("PR", "PR"),
                                ft.dropdown.Option("PE", "PE"),
                                ft.dropdown.Option("PI", "PI"),
                                ft.dropdown.Option("RJ", "RJ"),
                                ft.dropdown.Option("RN", "RN"),
                                ft.dropdown.Option("RS", "RS"),
                                ft.dropdown.Option("RO", "RO"),
                                ft.dropdown.Option("RR", "RR"),
                                ft.dropdown.Option("SC", "SC"),
                                ft.dropdown.Option("SP", "SP"),
                                ft.dropdown.Option("SE", "SE"),
                                ft.dropdown.Option("TO", "TO"),
                            ],
                            border_radius=10,
                            bgcolor="#F3F4F6",
                            expand=True
                        )
        self.campo_telefone = ft.TextField(label="Telefone", on_blur=self.telefone_blur, on_change = self.telefone_change, value=farmacia["telefone"] if farmacia else "")

        # Painel lateral de edição
        self.painel_detalhes_farmacia = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            visible=self.editando_farmacia,
            animate_opacity=300,
            opacity=1.0 if self.editando_farmacia else 0.0,
            expand=1,
            content=ft.Column([
                ft.Text("🏥 Editar Farmácia", size=20, weight="bold", color=ft.Colors.BLUE_900),
                ft.Divider(),
                self.campo_nome_f,
                self.campo_endereco,
                self.campo_cnpj,
                self.campo_cidade,
                self.campo_estado,
                self.campo_telefone,
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        bgcolor=ft.Colors.BLUE_600,
                        color="white",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=self.salvar_farmacia  # Novo método para salvar
                    ),
                    ft.OutlinedButton(
                        "Cancelar",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=lambda e: self.load_farmacias()
                    )
                ], spacing=10)
            ], spacing=12)
        )

        # Renderiza a tabela com farmácias do banco
        self.renderizar_tabela_farmacias(farmacias_db)

    def gerar_rows_farmacias(self, lista):
        rows = []
        for f in lista:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(f[0]))),
                        ft.DataCell(ft.Text(f[1])),
                        ft.DataCell(ft.Text(f[2])),
                        ft.DataCell(ft.Text(f[3])),
                        ft.DataCell(ft.Text(f[4])),
                        ft.DataCell(ft.Text(f[5])),
                        ft.DataCell(ft.Text(f[6])),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color="#10B981",
                                    tooltip="Editar",
                                    on_click=lambda e, f=f: (
                                        setattr(self, "farmacia_atual", {
                                            "id": f[0],
                                            "nome": f[1],
                                            "endereco": f[2],
                                            "cnpj": f[3],
                                            "cidade": f[4],
                                            "estado": f[5],
                                            "telefone": f[6]
                                        }),
                                        self.load_farmacias(farmacia=self.farmacia_atual)
                                    )
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="#DC2626",
                                    tooltip="Excluir",
                                    on_click=lambda e: print(f"Excluir {f[1]}")
                                )
                            ], spacing=6)
                        )
                    ]
                )
            )
        return rows

    def renderizar_tabela_farmacias(self, lista):
        self.tabela_farmacias = ft.DataTable(
            ref=self.tabela_farmacias_ref,
            heading_row_color="#F9FAFB",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Endereço")),
                ft.DataColumn(ft.Text("CNPJ")),
                ft.DataColumn(ft.Text("Cidade")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Telefone")),
                ft.DataColumn(ft.Text("Ações"))
            ],
            rows=self.gerar_rows_farmacias(lista)
        )

        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.Icons.LOCAL_HOSPITAL, size=40, color=ft.Colors.BLUE_600),
                        ft.Text("Gerenciamento de Farmácias", size=32, weight="bold", color=ft.Colors.BLUE_900)
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Adicione, edite ou gerencie as farmácias cadastradas no sistema.",
                            size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30),

                    ft.Container(
                        bgcolor="#FFFFFF",
                        border_radius=20,
                        padding=25,
                        expand=True,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📋 Lista de Farmácias", size=20, weight="bold", color="#111827"),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    tooltip="Atualizar Lista",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=self.load_farmacias
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    tooltip="Adicionar nova farmácia",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=lambda e: self.load_farmacias(farmacia={})
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(),

                            ft.Row([
                                ft.Container(
                                    expand=True,
                                    content=self.campo_busca_farmacia
                                )
                            ]),
                            ft.Container(height=20),

                            ft.Container(
                                expand=True,
                                content=ft.Stack(
                                    expand=True,
                                    controls=[
                                        ft.Container(
                                            expand=True,
                                            content=self.tabela_farmacias,
                                            width=1200,
                                        ),
                                        ft.AnimatedSwitcher(
                                            content=self.painel_detalhes_farmacia if self.editando_farmacia else ft.Container(),
                                            transition=ft.Animation(300, "easeInOut")
                                        )
                                    ]
                                )
                            )
                        ], spacing=20)
                    )
                ], spacing=20)
            )
        )

        self.page.update()

    def filtrar_farmacias(self, e):
        termo = self.campo_busca_farmacia.value.strip().lower()
        farmacias = listar_farmacias()
        resultado = [f for f in farmacias if termo in f[1].lower() or termo in f[3].lower() or termo in f[4].lower() or termo in f[5].lower()]

        self.tabela_farmacias_ref.current.rows = self.gerar_rows_farmacias(resultado)
        self.tabela_farmacias_ref.current.update()

    from database import listar_usuarios, aprovar_usuario, recusar_usuario

    def load_pacientes(self, e=None, paciente=None):
        self.current_view.controls.clear()
        self.editando_paciente = paciente is not None
        self.paciente_atual = paciente if paciente else None

        # Buscar farmácias do banco de dados
        pacientes_db = listar_usuarios()

        def cpf_blur(e):
            texto_original = self.campo_cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

            formatado = ""
            if len(numeros) >= 3:
                formatado += numeros[:3] + "."
            if len(numeros) >= 6:
                formatado += numeros[3:6] + "."
            if len(numeros) >= 9:
                formatado += numeros[6:9] + "-"
            if len(numeros) > 9:
                formatado += numeros[9:]
            elif len(numeros) > 6:
                formatado += numeros[6:9]
            elif len(numeros) > 3:
                formatado += numeros[3:6]
            elif len(numeros) > 0:
                formatado += numeros[0:3]

            self.campo_cpf.value = formatado
            self.campo_cpf.update()

        def cpf_change(e):
            texto_original = self.campo_cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

            if len(numeros) == 11:
                self.campo_nascimento.focus()

        def nascimento_change(e):
            texto_original = self.campo_nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:8]

            if len(numeros) == 8:
                pass

        def nascimento_blur(e):
            texto_original = self.campo_nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:8]
            formatado = ""
            if len(numeros) >= 2:
                formatado += numeros[:2] + "/"
            if len(numeros) >= 4:
                formatado += numeros[2:4] + "/"
            if len(numeros) > 4:
                formatado += numeros[4:]
            elif len(numeros) > 2:
                formatado += numeros[2:]
            self.campo_nascimento.value = formatado
            self.campo_nascimento.update()

        self.current_view.controls.clear()
        
        # Campos de edição
        self.campo_busca_pacientes = ft.TextField(
            hint_text="Buscar paciente...",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=30,
            bgcolor="#F9FAFB",
            height=50,
            on_change=self.filtrar_pacientes
        )

        self.campo_nome_paciente = ft.TextField(label="Nome do Paciente", border_radius=10, bgcolor="#F9FAFB")
        self.campo_cpf = ft.TextField(label="CPF", on_blur=cpf_blur, on_change=cpf_change, border_radius=10, bgcolor="#F9FAFB")
        self.campo_email = ft.TextField(label="Email", border_radius=10, bgcolor="#F9FAFB")
        self.campo_nascimento = ft.TextField(label="Data de Nascimento (DD/MM/AAAA)", on_blur=nascimento_blur, on_change=nascimento_change, border_radius=10, bgcolor="#F9FAFB")
        self.campo_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, border_radius=10, bgcolor="#F9FAFB")
        self.campo_confirmar_senha = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, border_radius=10, bgcolor="#F9FAFB")

        # Painel lateral de edição
        self.painel_detalhes_paciente = ft.Container(
            bgcolor="#FFFFFF",
            border_radius=20,
            padding=25,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
            visible=self.editando_paciente,
            animate_opacity=300,
            opacity=1.0 if self.editando_paciente else 0.0,
            expand=1,
            content=ft.Column([
                ft.Text("🏥 Adicionar Paciente", size=20, weight="bold", color=ft.Colors.BLUE_900),
                ft.Divider(),
                self.campo_nome_paciente,
                self.campo_email,
                self.campo_cpf,
                self.campo_nascimento,
                self.campo_senha,
                self.campo_confirmar_senha,
                ft.Container(height=20),
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        bgcolor=ft.Colors.BLUE_600,
                        color="white",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=self.salvar_paciente  # Novo método para salvar
                    ),
                    ft.OutlinedButton(
                        "Cancelar",
                        expand=True,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        on_click=lambda e: self.load_pacientes()
                    )
                ], spacing=10)
            ], spacing=12)
        )

        # Renderiza a tabela com farmácias do banco
        self.renderizar_tabela_pacientes(pacientes_db)

    def gerar_rows_pacientes(self, lista):
        status_cores = {
            "Pendente": ("#D97706", "#FEF3C7"),
            "Aprovado": ("#15803D", "#D1FAE5"),
            "Recusado": ("#DC2626", "#FEE2E2"),
        }

        def status_badge(status):
            cor_texto, cor_fundo = status_cores.get(status, ("#6B7280", "#E5E7EB"))
            return ft.Row(
                [
                    ft.Container(width=8, height=8, bgcolor=cor_texto, border_radius=20),
                    ft.Text(status, color=cor_texto, weight="bold")
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER
            )

        rows = []
        for p in lista:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(p[0]))),
                        ft.DataCell(ft.Text(p[1])),
                        ft.DataCell(ft.Text(p[3])),
                        ft.DataCell(ft.Text(p[4])),
                        ft.DataCell(ft.Text(p[5])),
                        ft.DataCell(
                            ft.Container(
                                content=status_badge(p[6]),
                                padding=ft.padding.symmetric(horizontal=4, vertical=4),
                                bgcolor=status_cores.get(p[6], "#E5E7EB")[1],
                                border_radius=20,
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                                        icon_color="#059669",
                                        tooltip="Aprovar paciente",
                                        on_click=lambda e, pid=p[0]: self.aprovar_usuario(pid)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.CANCEL_OUTLINED,
                                        icon_color="#DC2626",
                                        tooltip="Recusar paciente",
                                        on_click=lambda e, pid=p[0]: self.recusar_usuario(pid)
                                    ),
                                ],
                                spacing=8
                            )
                        )
                    ]
                )
            )
        return rows

    def renderizar_tabela_pacientes(self, lista):
        self.tabela_pacientes = ft.DataTable(
            ref=self.tabela_pacientes_ref,
            heading_row_color="#F9FAFB",
            border=ft.border.all(1, "#E5E7EB"),
            border_radius=12,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("CPF")),
                ft.DataColumn(ft.Text("Nascimento")),
                ft.DataColumn(ft.Text("Data de Criação")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows= self.gerar_rows_pacientes(lista)
        )
        #Teste
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Row([
                        ft.Icon(name=ft.Icons.LOCAL_HOSPITAL, size=40, color=ft.Colors.BLUE_600),
                        ft.Text("📋 Gerenciamento de Pacientes", size=32, weight="bold", color=ft.Colors.BLUE_900)
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Adicione, edite ou gerencie os pacientes cadastrados no sistema.",
                            size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30),

                    ft.Container(
                        bgcolor="#FFFFFF",
                        border_radius=20,
                        padding=25,
                        expand=True,
                        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                        content=ft.Column([
                            ft.Row([
                                ft.Text("📋 Lista de Pacientes", size=20, weight="bold", color="#111827"),
                                ft.Container(expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.REFRESH,
                                    tooltip="Atualizar Lista",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=self.load_pacientes
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    tooltip="Adicionar novo paciente",
                                    icon_color=ft.Colors.BLUE_600,
                                    on_click=lambda e: self.load_pacientes(paciente={})
                                )
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.Divider(),

                            ft.Row([
                                ft.Container(
                                    expand=True,
                                    content=self.campo_busca_pacientes
                                )
                            ]),
                            ft.Container(height=20),

                            ft.Container(
                                expand=True,
                                content=ft.Stack(
                                    expand=True,
                                    controls=[
                                        ft.Container(
                                            expand=True,
                                            content=self.tabela_pacientes,
                                            width=1200,
                                        ),
                                        ft.AnimatedSwitcher(
                                            content=self.painel_detalhes_paciente if self.editando_paciente else ft.Container(),
                                            transition=ft.Animation(300, "easeInOut")
                                        )
                                    ]
                                )
                            )
                        ], spacing=20)
                    )
                ], spacing=20)
            )
        )

        self.page.update()

    def filtrar_pacientes(self, e):
        termo = self.campo_busca_pacientes.value.strip().lower()
        pacientes = listar_usuarios()
        resultado = [p for p in pacientes if termo in p[1].lower() or termo in p[3].lower()]

        self.tabela_pacientes_ref.current.rows = self.gerar_rows_pacientes(resultado)
        self.tabela_pacientes_ref.current.update()

    # Funções para Aprovar e Recusar Pacientes
    def aprovar_usuario(self, paciente_id):
        aprovar_usuario(paciente_id)
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Paciente aprovado com sucesso!"), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()
        self.load_pacientes()

    def recusar_usuario(self, paciente_id):
        recusar_usuario(paciente_id)
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Paciente recusado com sucesso!"), bgcolor="red")
        self.page.snack_bar.open = True
        self.page.update()
        self.load_pacientes()

    def load_cadastro_paciente(self, e=None):
        def cpf_blur(e):
            texto_original = self.campo_cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

            formatado = ""
            if len(numeros) >= 3:
                formatado += numeros[:3] + "."
            if len(numeros) >= 6:
                formatado += numeros[3:6] + "."
            if len(numeros) >= 9:
                formatado += numeros[6:9] + "-"
            if len(numeros) > 9:
                formatado += numeros[9:]
            elif len(numeros) > 6:
                formatado += numeros[6:9]
            elif len(numeros) > 3:
                formatado += numeros[3:6]
            elif len(numeros) > 0:
                formatado += numeros[0:3]

            self.campo_cpf.value = formatado
            self.campo_cpf.update()

        def cpf_change_cadastro(e):
            texto_original = self.campo_cpf.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:11]

            if len(numeros) == 11:
                self.campo_nascimento.focus()

        def nascimento_change_cadastro(e):
            texto_original = self.campo_nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:8]

            if len(numeros) == 8:
                pass

        def nascimento_blur_cadastro(e):
            texto_original = self.campo_nascimento.value
            numeros = ''.join(filter(str.isdigit, texto_original))[:8]
            formatado = ""
            if len(numeros) >= 2:
                formatado += numeros[:2] + "/"
            if len(numeros) >= 4:
                formatado += numeros[2:4] + "/"
            if len(numeros) > 4:
                formatado += numeros[4:]
            elif len(numeros) > 2:
                formatado += numeros[2:]
            self.campo_nascimento.value = formatado
            self.campo_nascimento.update()

        self.current_view.controls.clear()

        # Campos do formulário
        self.campo_nome_paciente = ft.TextField(label="Nome do Paciente", border_radius=10, bgcolor="#F3F4F6")
        self.campo_cpf = ft.TextField(label="CPF", on_blur=cpf_blur, on_change=cpf_change_cadastro, border_radius=10, bgcolor="#F3F4F6")
        self.campo_email = ft.TextField(label="Email", border_radius=10, bgcolor="#F3F4F6")
        self.campo_nascimento = ft.TextField(label="Data de Nascimento (DD/MM/AAAA)", on_blur=nascimento_blur_cadastro, on_change=nascimento_change_cadastro, border_radius=10, bgcolor="#F3F4F6")
        self.campo_senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, border_radius=10, bgcolor="#F3F4F6")
        self.campo_confirmar_senha = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, border_radius=10, bgcolor="#F3F4F6")

        # Estrutura do formulário
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Text("Cadastrar Novo Paciente", size=28, weight="bold", color=ft.Colors.BLUE_900),
                        ft.Container(height=20),
                        ft.Container(
                            padding=30,
                            bgcolor="#FFFFFF",
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                            content=ft.Column(
                                [
                                    self.campo_nome_paciente,
                                    self.campo_cpf,
                                    self.campo_email,
                                    self.campo_nascimento,
                                    self.campo_senha,
                                    self.campo_confirmar_senha,
                                    ft.Container(height=20),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Salvar Paciente",
                                                bgcolor=ft.Colors.BLUE_600,
                                                color="white",
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                expand=True,
                                                on_click=self.salvar_paciente
                                            ),
                                            ft.OutlinedButton(
                                                "Cancelar",
                                                expand=True,
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                on_click=lambda e: self.load_pacientes(),
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

    def salvar_paciente(self, e):
        nome = self.campo_nome_paciente.value.strip()
        cpf = self.campo_cpf.value.strip()
        email = self.campo_email.value.strip()
        nascimento = self.campo_nascimento.value.strip()
        senha = self.campo_senha.value.strip()
        confirmar_senha = self.campo_confirmar_senha.value.strip()

        # Validação dos campos
        if not nome or not cpf or not email or not nascimento or not senha or not confirmar_senha:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Todos os campos são obrigatórios."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        if senha != confirmar_senha:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("As senhas não coincidem."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Formata a data de nascimento para o formato esperado no banco (DD/MM/AAAA para AAAA-MM-DD)
        try:
            dia, mes, ano = nascimento.split("/")
            nascimento_formatado = f"{ano}-{mes}-{dia}"
        except ValueError:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Data de nascimento inválida."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Tenta registrar o usuário no banco de dados
        sucesso = registrar_usuario(nome, email, cpf, nascimento_formatado, senha)
        
        if sucesso:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Paciente cadastrado com sucesso!"), bgcolor="green")
            self.page.snack_bar.open = True
            self.page.update()
            self.load_pacientes()  # Retorna para a lista de pacientes
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Erro: CPF ou email já cadastrado."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()

    def load_cadastro_agendamento(self, e=None):
        # Carregar dados do banco
        pacientes = listar_usuarios()
        medicamentos = listar_medicamentos()
        farmacias = listar_farmacias()

        self.dropdown_paciente = ft.Dropdown(
            label="Paciente",
            options=[ft.dropdown.Option(str(u[0]), u[1]) for u in pacientes],
            border_radius=10,
            bgcolor="#F9FAFB",
            expand=True
        )

        self.dropdown_medicamento = ft.Dropdown(
            label="Medicamento",
            options=[ft.dropdown.Option(str(m[0]), m[1]) for m in medicamentos],
            border_radius=10,
            bgcolor="#F9FAFB",
            expand=True
        )

        self.dropdown_farmacia = ft.Dropdown(
            label="Farmácia",
            options=[ft.dropdown.Option(str(f[0]), f[1]) for f in farmacias],
            border_radius=10,
            bgcolor="#F9FAFB",
            expand=True
        )

        self.campo_codigo = ft.TextField(label="Código do Medicamento", border_radius=10, bgcolor="#F9FAFB")
        self.campo_data = ft.TextField(label="Data (AAAA-MM-DD)", border_radius=10, bgcolor="#F9FAFB")
        self.campo_horario = ft.TextField(label="Horário (HH:MM)", border_radius=10, bgcolor="#F9FAFB")

        # Estrutura do formulário
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Text("Cadastrar Novo Agendamento", size=28, weight="bold", color=ft.Colors.BLUE_900),
                        ft.Container(height=20),
                        ft.Container(
                            padding=30,
                            bgcolor="#FFFFFF",
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, spread_radius=2, color="#CBD5E1", offset=ft.Offset(0, 8)),
                            content=ft.Column(
                                [
                                    self.dropdown_paciente,
                                    self.dropdown_medicamento,
                                    self.dropdown_farmacia,
                                    self.campo_codigo,
                                    self.campo_data,
                                    self.campo_horario,
                                    ft.Container(height=20),

                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Salvar Agendamento",
                                                bgcolor=ft.Colors.BLUE_600,
                                                color="white",
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                expand=True,
                                                on_click=self.salvar_agendamento
                                            ),
                                            ft.OutlinedButton(
                                                "Cancelar",
                                                expand=True,
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                on_click=lambda e: self.load_agendamentos(),
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

    def filtrar_agendamentos(self, e):
        termo = self.campo_busca_agendamentos.value.strip().lower()
        agendamentos = listar_agendamentos()

        resultado = [
            a for a in agendamentos
            if termo in a[1].lower() or termo in a[2].lower() or termo in a[3].lower()
        ]

        self.tabela_agendamentos_ref.current.rows = self.gerar_rows_agendamentos(resultado)
        self.tabela_agendamentos_ref.current.update()

    def salvar_agendamento(self, e=None):
        paciente_id = self.dropdown_paciente.value
        medicamento_id = self.dropdown_medicamento.value
        farmacia_id = self.dropdown_farmacia.value
        codigo_medicamento = self.campo_codigo.value.strip()
        data = self.campo_data.value.strip()
        horario = self.campo_horario.value.strip()

        # Validação básica
        if not all([paciente_id, medicamento_id, farmacia_id, codigo_medicamento, data, horario]):
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Todos os campos são obrigatórios."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Salva no banco de dados
        from database import adicionar_agendamento
        adicionar_agendamento(int(paciente_id), int(medicamento_id), int(farmacia_id), codigo_medicamento, data, horario, status="Pendente")

        # Mensagem de sucesso
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Agendamento cadastrado com sucesso."), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()

        # Voltar para a lista de agendamentos
        self.load_agendamentos()
       

    def gerar_grafico_agendamentos_semanais(self):
        from collections import Counter
        from datetime import datetime
        from database import listar_agendamentos

        agendamentos = listar_agendamentos()

        # Extrai o dia da semana de cada agendamento
        dias_semana = [datetime.strptime(a[5], "%Y-%m-%d").weekday() for a in agendamentos]

        # Contagem real por dia da semana
        contagem = Counter(dias_semana)

        dias_pt = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        maior_valor_real = max(contagem.values(), default=0)
        maior_valor_visual = max(maior_valor_real, 5) + 1

        cores_dias = [
            ft.colors.BLUE_600,
            ft.colors.INDIGO_600,
            ft.colors.CYAN_600,
            ft.colors.GREEN_600,
            ft.colors.AMBER_600,
            ft.colors.ORANGE_600,
            ft.colors.RED_600
        ]

        grupos = []
        for i in range(7):
            valor_real = contagem.get(i, 0)
            altura_barra = max(valor_real, 1)
            cor = cores_dias[i]

            if valor_real == maior_valor_real and valor_real > 0:
                cor = ft.colors.BLUE_ACCENT_700

            grupo = ft.Column([
                ft.Text(str(valor_real), size=11, color=ft.colors.BLACK, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=120,
                    width=30,
                    alignment=ft.alignment.bottom_center,
                    content=ft.BarChart(
                        bar_groups=[
                            ft.BarChartGroup(
                                x=0,
                                bar_rods=[
                                    ft.BarChartRod(
                                        to_y=altura_barra,
                                        width=24,
                                        color=cor,
                                        border_radius=6
                                    )
                                ]
                            )
                        ],
                        max_y=maior_valor_visual,
                        left_axis=None,
                        bottom_axis=None,
                        horizontal_grid_lines=None,
                        border=None,
                        expand=True
                    )
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            grupos.append(grupo)

        return ft.Container(
            bgcolor="#FFFFFF",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.colors.BLACK12),
            padding=16,
            content=ft.Column([
                ft.Text("📊 Agendamentos por Dia da Semana", size=15, weight="bold", color="#1E3A8A"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    controls=grupos
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[ft.Text(dias_pt[i][:3], size=11) for i in range(7)]
                )
            ], spacing=8)
        )





    def build_tela(self):
        return ft.View(
            route="/admin_dashboard",
            controls=[
                ft.ResponsiveRow(
                    columns=12,
                    controls=[
                        ft.Container(
                            col={"sm": 12, "md": 3},
                            content=self.side_menu(),
                            bgcolor="#F9FAFB"
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 9},
                            content=ft.Column([
                                self.header(),
                                self.current_view
                            ], expand=True)
                        )
                    ],
                    expand=True,
                    spacing=0,
                    run_spacing=0
                )
            ],
            scroll=ft.ScrollMode.AUTO
        )

if __name__ == "__main__":
    def main(page: ft.Page):
        app = TelaAdminDashboard(page)
        page.views.append(app.build_tela()) # app.build_tela()
        page.update()

    ft.app(target=main)  # Ensure the main function is passed as the target
