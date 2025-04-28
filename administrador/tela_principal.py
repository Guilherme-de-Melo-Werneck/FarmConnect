import flet as ft

def main(page: ft.Page):
    page.title = "FarmConnect"
    page.bgcolor = "#F0FDF4"  # Fundo levemente verde-claro
    page.padding = 0
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    sidebar_open = True
    current_view = ft.Column(expand=True)

    def toggle_sidebar(e):
        nonlocal sidebar_open
        sidebar_open = not sidebar_open
        page.update()

    def menu_item(icon, text, on_click=None):
        item = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color="#059669", size=24),
                    ft.Text(text, size=14, visible=sidebar_open, color="#374151"),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
            ),
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

    def side_menu():
        return ft.Container(
            width=240 if sidebar_open else 80,
            bgcolor="#FFFFFF",
            border=ft.border.only(right=ft.BorderSide(1, "#E5E7EB")),
            padding=10,
            content=ft.Column(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK if sidebar_open else ft.icons.ARROW_FORWARD,
                        icon_color="#10B981",
                        on_click=toggle_sidebar,
                        tooltip="Expandir/Fechar Menu",
                    ),
                    ft.Divider(),
                    menu_item(ft.icons.HOME_OUTLINED, "Início", lambda e: load_dashboard()),
                    menu_item(ft.icons.CALENDAR_MONTH_OUTLINED, "Agendamentos"),
                    menu_item(ft.icons.PERSON_OUTLINED, "Pacientes"),
                    menu_item(ft.icons.LOCAL_HOSPITAL_OUTLINED, "Farmácias"),
                    menu_item(ft.icons.MEDICAL_SERVICES_OUTLINED, "Medicamentos", lambda e: load_medicamentos()),
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START,
            ),
        )

    def header():
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20),
            bgcolor="#34D399",
            height=65,
            border=ft.border.only(bottom=ft.BorderSide(1, "#E5E7EB")),
            content=ft.Row(
                [
                    ft.Container(expand=True),
                    ft.Text("FarmConnect - Painel Principal", size=22, weight="bold", color="#065F46"),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.IconButton(ft.icons.DARK_MODE_OUTLINED, icon_color="#065F46"),
                            ft.IconButton(ft.icons.SCHEDULE_OUTLINED, icon_color="#065F46"),
                            ft.Text("Bem-vindo!", size=12, color="#065F46"),
                            ft.Text("DESENVOLVIMENTO", size=12, weight="bold", color="#065F46"),
                            ft.IconButton(ft.icons.REFRESH, icon_color="#065F46"),
                        ],
                        spacing=10
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def graph_cards():
        return ft.Row(
            [
                ft.Container(
                    expand=1,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("Evolução dos Agendamentos", size=16, weight="bold", color="#065F46"),
                            ft.Container(
                                height=120,
                                bgcolor="#D1FAE5",
                                border_radius=10,
                                alignment=ft.alignment.center,
                                content=ft.Text("Gráfico aqui", size=14, color="#047857"),
                            )
                        ],
                        spacing=10,
                    ),
                ),
                ft.Container(
                    expand=1,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("Estoque de Medicamentos (%)", size=16, weight="bold", color="#065F46"),
                            ft.Container(
                                width=100,
                                height=100,
                                bgcolor="#A7F3D0",
                                border_radius=50,
                                alignment=ft.alignment.center,
                                content=ft.Text("80%", size=18, weight="bold", color="#047857")
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    expand=1,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("Medicamentos mais solicitados", size=16, weight="bold", color="#065F46"),
                            ft.Column(
                                [
                                    ft.Row([
                                        ft.Container(width=50, height=20, bgcolor="#047857", border_radius=5),
                                        ft.Text("Medicamento 1", size=13)
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Container(width=45, height=20, bgcolor="#059669", border_radius=5),
                                        ft.Text("Medicamento 2", size=13)
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Container(width=40, height=20, bgcolor="#10B981", border_radius=5),
                                        ft.Text("Medicamento 3", size=13)
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Container(width=35, height=20, bgcolor="#3B82F6", border_radius=5),
                                        ft.Text("Medicamento 4", size=13)
                                    ], spacing=8),
                                    ft.Row([
                                        ft.Container(width=30, height=20, bgcolor="#6366F1", border_radius=5),
                                        ft.Text("Medicamento 5", size=13)
                                    ], spacing=8),
                                ], spacing=6
                            )
                        ], spacing=10,
                    ),
                ),
            ], spacing=20
        )

    def metric_cards():
        return ft.Row(
            [
                ft.Container(
                    expand=1,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("Pacientes Cadastrados", size=14, weight="bold", color="#065F46"),
                            ft.Text("0", size=34, weight="bold", color="#111827"),
                            ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                            ft.OutlinedButton("+ Adicionar Paciente", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    expand=1,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("Agendamentos Hoje", size=14, weight="bold", color="#065F46"),
                            ft.Text("0", size=34, weight="bold", color="#111827"),
                            ft.Text("Valor dinâmico", size=12, color="#10B981"),
                            ft.OutlinedButton("+ Novo Agendamento", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    expand=1,
                    bgcolor="#FFFFFF",
                    border_radius=12,
                    shadow=ft.BoxShadow(blur_radius=8, color="#CBD5E1"),
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("Medicamentos Cadastrados", size=14, weight="bold", color="#065F46"),
                            ft.Text("0", size=34, weight="bold", color="#111827"),
                            ft.Text("Valor dinâmico", size=12, color="#6B7280"),
                            ft.OutlinedButton("+ Adicionar Medicamento", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))),
                        ], spacing=10, alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
            ], spacing=20
        )

    def load_dashboard():
        current_view.controls = [
            ft.Container(
                padding=20,
                content=ft.Column([
                    graph_cards(),
                    ft.Container(height=20),
                    metric_cards(),
                ], spacing=20, expand=True)
            )
        ]
        page.update()

    def load_medicamentos(e=None):
        current_view.controls.clear()
        current_view.controls.append(
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text(
                            "Gerenciamento de Medicamentos",
                            size=24,
                            weight="bold",
                            color="#065F46",
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            [
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
                                    on_click=load_cadastro_medicamento,  # TROQUEI AQUI
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            [
                                ft.Container(
                                    bgcolor="white",
                                    border_radius=10,
                                    padding=10,
                                    shadow=ft.BoxShadow(blur_radius=6, color="#CBD5E1"),
                                    expand=2,
                                    content=ft.Column(
                                        [
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
                                                                # suas linhas exemplo aqui
                                                            ],
                                                        )
                                                    ],
                                                    auto_scroll=True,
                                                ),
                                            ),
                                        ],
                                        spacing=10,
                                    ),
                                ),
                                ft.Container(width=20),
                                ft.Container(
                                    bgcolor="white",
                                    border_radius=10,
                                    padding=20,
                                    shadow=ft.BoxShadow(blur_radius=6, color="#CBD5E1"),
                                    expand=1,
                                    content=ft.Column(
                                        [
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
                                            ft.Row(
                                                [
                                                    ft.ElevatedButton(
                                                        "Salvar",
                                                        bgcolor="#059669",
                                                        color="white",
                                                        expand=True,
                                                    ),
                                                    ft.OutlinedButton(
                                                        "Limpar",
                                                        expand=True,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                        ],
                                        spacing=10,
                                    ),
                                ),
                            ],
                            spacing=20,
                        ),
                    ],
                    spacing=20,
                    expand=True,
                ),
            )
        )
        current_view.opacity = 0
        page.update()
        current_view.opacity = 1
        page.update()

    # 🟰🟰 AQUI ENTRA A NOVA TELA DE CADASTRO 🟰🟰
    def load_cadastro_medicamento(e=None):
        current_view.controls.clear()
        current_view.controls.append(
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
                                    ft.TextField(
                                        label="Categoria",
                                        border_radius=10,
                                        bgcolor="#F0FDF4",
                                    ),
                                    ft.TextField(
                                        label="Fabricante",
                                        border_radius=10,
                                        bgcolor="#F0FDF4",
                                    ),
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
                                            ),
                                            ft.OutlinedButton(
                                                "Cancelar",
                                                expand=True,
                                                height=50,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                                                on_click=lambda e: load_medicamentos(),
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
        current_view.opacity = 0
        page.update()
        current_view.opacity = 1
        page.update()

    # Adicionando os componentes principais
    page.add(
        ft.Row([
            side_menu(),
            ft.Column([header(), current_view], expand=True)
        ], expand=True)
    )

    load_dashboard()

ft.app(target=main)






