import flet as ft

def main(page: ft.Page):
    page.title = "+SuaVida - Agendamento de Consultas"
    page.padding = 0
    page.bgcolor = ft.colors.WHITE
    page.scroll = "auto"

    PRIMARY = ft.colors.BLUE_600
    PRIMARY_DARK = ft.colors.BLUE_900
    TEXT_PRIMARY = ft.colors.BLACK87
    TEXT_SECONDARY = ft.colors.GREY_700

    def section_spacing(content):
        return ft.Container(
            margin=ft.Margin(0, 0, 0, 50),
            content=content
        )

    def build_header():
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            padding=20,
            content=ft.Row(
                controls=[
                    ft.Image(src="https://i.imgur.com/7kKQyqA.png", width=60, height=60),
                    ft.Text("+SuaVida", size=24, weight="bold", color=PRIMARY_DARK),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Baixe o app agora!",
                        bgcolor=PRIMARY,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(padding=15),
                    ),
                    ft.TextButton(
                        "Entrar",
                        on_click=lambda _: print("Entrar clicado"),
                        style=ft.ButtonStyle(padding=15, color=PRIMARY)
                    )
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.START
            )
        )

    def build_hero_section():
        title = ft.Text(
            "Simplifique, organize e gerencie as ",
            size=30,
            weight="bold",
            color=TEXT_PRIMARY,
            spans=[
                ft.TextSpan("consultas", ft.TextStyle(color=ft.colors.BLUE_400, weight="bold"))
            ]
        )
        paragraph = ft.Text(
            "+SuaVida facilita o agendamento e gerenciamento de consultas médicas, colocando o controle nas suas mãos. "
            "Torne a experiência mais eficiente, acessível e moderna – tanto para pacientes quanto para clínicas.",
            size=13,
            color=TEXT_SECONDARY
        )
        left_column = ft.Column(
            [title, paragraph],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            width=500
        )
        illustration = ft.Image(
            src="https://i.imgur.com/FqvnEdF.png",
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        return section_spacing(ft.Container(
            padding=40,
            content=ft.Row(
                controls=[left_column, illustration],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ))

    def build_about_section():
        about_title = ft.Text("Sobre nós", size=28, weight="bold", color=PRIMARY_DARK, text_align=ft.TextAlign.CENTER)

        about_text = ft.Text(
            "Bem-vindo à +Sua Vida, sua parceira confiável em soluções de gerenciamento de clínica e cuidados médicos. "
            "Estamos comprometidos em transformar a experiência de saúde para empresas e pacientes, proporcionando eficiência, "
            "acessibilidade e conveniência.\n\n"
            "Nossa missão é simplificar o acesso a cuidados de saúde de qualidade. Acreditamos que todos merecem atendimento médico "
            "acessível e eficiente, e estamos dedicados a tornar essa visão uma realidade. Queremos fortalecer a relação entre clínicas "
            "e pacientes, oferecendo ferramentas inovadoras para facilitar a comunicação, agendamento de consultas e gestão de informações.\n\n"
            "Estamos empenhados em continuar aprimorando nossas soluções e expandir nossa oferta para melhor atender às necessidades "
            "em constante evolução do setor de saúde. Acreditamos que a tecnologia pode desempenhar um papel fundamental na melhoria "
            "do acesso aos cuidados médicos, e continuaremos a trabalhar incansavelmente para alcançar essa visão.\n\n"
            "Na +Sua Vida, valorizamos cada paciente e cada clínica que confia em nossos serviços. Junte-se a nós em nossa jornada para "
            "revolucionar a saúde e tornar o atendimento médico mais acessível e conveniente para todos.",
            size=13,
            color=TEXT_SECONDARY,
            text_align=ft.TextAlign.JUSTIFY
        )

        benefits_left = ["Análise de dados", "Redução de não conformâncias", "Maior acessibilidade"]
        benefits_right = ["Conveniência", "Economia de tempo", "Comunicação aprimorada"]

        def benefit(texto):
            return ft.Row([
                ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINED, color=PRIMARY),
                ft.Text(texto, size=13, weight="bold", color=TEXT_PRIMARY)
            ], spacing=8)

        benefits_grid = ft.Row(
            controls=[
                ft.Column([benefit(item) for item in benefits_left], spacing=10),
                ft.Column([benefit(item) for item in benefits_right], spacing=10)
            ],
            spacing=40,
            alignment=ft.MainAxisAlignment.START
        )

        about_image = ft.Image(
            src="https://i.imgur.com/bH7iFez.png",
            width=400,
            height=320,
            fit=ft.ImageFit.CONTAIN
        )

        return section_spacing(
            ft.Container(
                padding=40,
                content=ft.Row(
                    controls=[
                        about_image,
                        ft.Container(
                            width=500,
                            content=ft.Column([
                                about_title,
                                ft.Container(height=10),
                                about_text,
                                ft.Container(height=20),
                                benefits_grid
                            ], spacing=10)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            )
        )

    def build_manage_section():
        title = ft.Text("Pacientes: Gerencie suas consultas", size=24, weight="bold", color=PRIMARY_DARK)
        description = ft.Text(
            "Com recursos como armazenamento de informações do paciente, listagem de médicos, agendamento automatizado "
            "e avisos automáticos para o comparecimento de consultas. Reduza a carga de trabalho manual, economize tempo "
            "e melhore a eficiência de sua clínica em um só lugar.",
            size=13,
            color=TEXT_SECONDARY
        )

        def card(icon_name, title_text, subtitle_text):
            return ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=12,
                padding=20,
                width=200,
                height=160,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.GREY_200,
                    offset=ft.Offset(0, 3),
                    blur_style=ft.ShadowBlurStyle.NORMAL
                ),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Icon(icon_name, size=40, color=PRIMARY),
                        ft.Container(height=3, bgcolor=PRIMARY, width=60),
                        ft.Text(title_text, size=14, weight="bold", color=TEXT_PRIMARY),
                        ft.Text(subtitle_text, size=12, color=TEXT_SECONDARY)
                    ]
                )
            )

        cards_row = ft.Row(
            wrap=False,
            scroll="auto",
            spacing=20,
            controls=[
                card(ft.icons.PERSON_OUTLINE, "Pacientes", "Armazene as informações"),
                card(ft.icons.LOCAL_HOSPITAL_OUTLINED, "Médicos", "Liste todos médicos"),
                card(ft.icons.CALENDAR_MONTH_OUTLINED, "Agendamento", "Busque informações do paciente"),
                card(ft.icons.CALENDAR_MONTH_OUTLINED, "Reagendamento", "Reagende facilmente"),
                card(ft.icons.CHECK_BOX_OUTLINE_BLANK, "Confirmação", "Confirme data e horário")
            ]
        )

        image = ft.Image(
            src="https://i.imgur.com/y62xqjW.png",
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )

        return section_spacing(ft.Container(
            padding=40,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=500,
                        content=ft.Column([title, description, ft.Container(height=20), cards_row], spacing=20)
                    ),
                    image
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ))

    def build_admin_section():
        title = ft.Text("Administradores: Controle total na plataforma", size=24, weight="bold", color=PRIMARY_DARK)
        description = ft.Text(
            "Tenha acesso completo para aprovar cadastros de usuários, adicionar medicamentos, controlar estoques, "
            "visualizar registros e manter a organização geral do sistema. Uma plataforma eficiente para uma gestão moderna.",
            size=13,
            color=TEXT_SECONDARY
        )

        def admin_card(icon_name, title_text, subtitle_text):
            return ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=12,
                padding=20,
                width=200,
                height=160,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.colors.GREY_200,
                    offset=ft.Offset(0, 3),
                    blur_style=ft.ShadowBlurStyle.NORMAL
                ),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Icon(icon_name, size=40, color=PRIMARY),
                        ft.Container(height=3, bgcolor=PRIMARY, width=60),
                        ft.Text(title_text, size=14, weight="bold", color=TEXT_PRIMARY),
                        ft.Text(subtitle_text, size=12, color=TEXT_SECONDARY)
                    ]
                )
            )

        cards = ft.Row(
            wrap=False,
            scroll="auto",
            spacing=20,
            controls=[
                admin_card(ft.icons.ADD_BOX_OUTLINED, "Adicionar Medicamentos", "Cadastre novos remédios"),
                admin_card(ft.icons.CHECK_CIRCLE_OUTLINE, "Aprovar Usuários", "Gerencie os cadastros"),
                admin_card(ft.icons.INVENTORY_2_OUTLINED, "Estoque", "Controle a disponibilidade"),
                admin_card(ft.icons.DESCRIPTION_OUTLINED, "Registros", "Visualize o histórico"),
                admin_card(ft.icons.NOTIFICATIONS_OUTLINED, "Alertas", "Receba notificações automáticas")
            ]
        )

        image = ft.Image(
            src="https://i.imgur.com/gAklHPs.png",
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )

        return section_spacing(ft.Container(
            padding=40,
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=500,
                        content=ft.Column([title, description, ft.Container(height=20), cards], spacing=20)
                    ),
                    image
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ))

    def build_footer():
        return ft.Container(
            bgcolor=ft.colors.WHITE,
            padding=40,
            content=ft.Column([
                ft.Text("+SuaVida © 2025", size=12, color=TEXT_PRIMARY),
                ft.Text("Todos os direitos reservados.", size=12, color=TEXT_SECONDARY)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    page.add(
        build_header(),
        build_hero_section(),
        build_about_section(),
        build_manage_section(),
        build_admin_section(),
        build_footer()
    )

ft.app(target=main)

