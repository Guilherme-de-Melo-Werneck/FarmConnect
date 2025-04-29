import flet as ft

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
            create_menu_item(ft.icons.CALENDAR_MONTH_OUTLINED, "Agendamentos"),
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

    def load_medicamentos(self, e=None):
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text(
                        "Gerenciamento de Medicamentos",
                        size=24,
                        weight="bold",
                        color="#065F46",
                    ),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Container(
                            content=ft.TextField(
                                hint_text="Buscar medicamento...",
                                prefix_icon=ft.icons.SEARCH,
                                border_radius=30,
                                bgcolor="#FFFFFF",
                                height=50,
                            ),
                            expand=True,
                        ),
                        ft.Container(width=10),
                        ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            bgcolor="#059669",
                            tooltip="Adicionar novo medicamento",
                            on_click=self.load_cadastro_medicamento,
                        ),

                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Container(
                            bgcolor="white",
                            border_radius=10,
                            padding=10,
                            shadow=ft.BoxShadow(blur_radius=6, color="#CBD5E1"),
                            expand=2,
                            content=ft.Column([
                                ft.Container(
                                    height=400,
                                    content=ft.ListView(
                                        controls=[
                                            ft.DataTable(
                                                columns=[
                                                    ft.DataColumn(ft.Text("ID")),
                                                    ft.DataColumn(ft.Text("Nome")),
                                                    ft.DataColumn(ft.Text("Categoria")),
                                                    ft.DataColumn(ft.Text("Fabricante")),
                                                    ft.DataColumn(ft.Text("Estoque")),
                                                    ft.DataColumn(ft.Text("Ações")),
                                                ],
                                                rows=[
                                                    # Exemplo de linha de medicamento:
                                                    ft.DataRow(
                                                        cells=[
                                                            ft.DataCell(ft.Text("1")),
                                                            ft.DataCell(ft.Text("Paracetamol")),
                                                            ft.DataCell(ft.Text("Analgésico")),
                                                            ft.DataCell(ft.Text("Farmacêutica XYZ")),
                                                            ft.DataCell(ft.Text("120")),
                                                            ft.DataCell(
                                                                ft.Row([
                                                                    ft.IconButton(icon=ft.icons.EDIT, icon_color="#10B981"),
                                                                    ft.IconButton(icon=ft.icons.DELETE, icon_color="red")
                                                                ], spacing=5)
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                            )
                                        ],
                                        auto_scroll=True,
                                    ),
                                ),
                            ], spacing=10),
                        ),
                        ft.Container(width=20),
                        ft.Container(
                            bgcolor="white",
                            border_radius=10,
                            padding=20,
                            shadow=ft.BoxShadow(blur_radius=6, color="#CBD5E1"),
                            expand=1,
                            content=ft.Column([
                                ft.Text(
                                    "Detalhes do Medicamento",
                                    size=20,
                                    weight="bold",
                                    color="#059669",
                                ),
                                ft.Divider(),
                                ft.TextField(label="Nome do Medicamento"),
                                ft.TextField(label="Categoria"),
                                ft.TextField(label="Fabricante"),
                                ft.TextField(label="Estoque Atual", keyboard_type=ft.KeyboardType.NUMBER),
                                ft.TextField(
                                    label="Observações",
                                    multiline=True,
                                    min_lines=3,
                                    max_lines=5,
                                ),
                                ft.Container(height=20),
                                ft.Row([
                                    ft.ElevatedButton(
                                        "Salvar",
                                        bgcolor="#059669",
                                        color="white",
                                        expand=True,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                        on_click=lambda e: print("Salvar medicamento"),
                                    ),
                                    ft.OutlinedButton(
                                        "Cancelar",
                                        expand=True,
                                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                        on_click=lambda e: self.load_medicamentos(),
                                    ),
                                ], spacing=10),
                            ], spacing=10),
                        ),
                    ], spacing=20),
                ], spacing=20),
            )
        )
        self.page.update()

    def load_cadastro_medicamento(self, e=None):
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column(
                    [
                        ft.Text(
                            "Cadastrar Novo Medicamento",
                            size=28,
                            weight="bold",
                            color="#059669",
                        ),
                        ft.Container(height=20),
                        ft.Container(
                            padding=30,
                            bgcolor="#FFFFFF",
                            border_radius=20,
                            shadow=ft.BoxShadow(
                                blur_radius=20,
                                spread_radius=2,
                                color="#CBD5E1",
                                offset=ft.Offset(0, 8),
                            ),
                            content=ft.Column(
                                [
                                    ft.TextField(
                                        label="Nome do Medicamento",
                                        border_radius=10,
                                        bgcolor="#F0FDF4",
                                    ),
                                    ft.Row([
                                        ft.Dropdown(
                                            label="Categoria",
                                            border_radius=10,
                                            bgcolor="#F0FDF4",
                                            options=[
                                                ft.dropdown.Option("Analgésico"),
                                                ft.dropdown.Option("Antibiótico"),
                                                ft.dropdown.Option("Anti-inflamatório")
                                            ],
                                            expand=True
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                            tooltip="Cadastrar nova categoria",
                                            icon_color="#059669",
                                            on_click=self.load_cadastro_categoria
                                        )
                                    ], spacing=10),

                                # Linha Fabricante
                                ft.Row([
                                    ft.Dropdown(
                                        label="Fabricante",
                                        border_radius=10,
                                        bgcolor="#F0FDF4",
                                        options=[
                                            ft.dropdown.Option("Farmacêutica XYZ"),
                                            ft.dropdown.Option("Laboratório ABC")
                                        ],
                                        expand=True
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.ADD_CIRCLE_OUTLINE,
                                        tooltip="Cadastrar novo fabricante",
                                        icon_color="#059669",
                                        on_click=self.load_cadastro_fabricante
                                    )
                                ], spacing=10),
                                    ft.TextField(
                                        label="Quantidade em Estoque",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        border_radius=10,
                                        bgcolor="#F0FDF4",
                                    ),
                                    ft.TextField(
                                        label="Observações",
                                        multiline=True,
                                        min_lines=3,
                                        max_lines=5,
                                        border_radius=10,
                                        bgcolor="#F0FDF4",
                                    ),
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
                                                on_click=lambda e: print("Medicamento salvo!"),
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
        self.current_view.controls.clear()
        self.current_view.controls.append(
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Cadastrar Novo Fabricante", size=26, weight="bold", color="#059669"),
                    ft.Container(height=20),
                    ft.TextField(label="Nome do Fabricante", border_radius=10, bgcolor="#F0FDF4"),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Salvar", bgcolor="#059669", color="white", on_click=lambda e: print("Fabricante salvo!"), expand=True),
                        ft.OutlinedButton("Cancelar", on_click=lambda e: self.load_cadastro_medicamento(), expand=True),
                    ], spacing=20)
                ], spacing=10)
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
        app.build_tela()
        page.update()

    ft.app(target=main)
