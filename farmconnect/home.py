import flet as ft


class HomeApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "FarmConnect"
        self.page.padding = 0
        self.page.bgcolor = ft.Colors.WHITE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.ADAPTIVE

        self.PRIMARY = ft.Colors.BLUE_600
        self.PRIMARY_DARK = ft.Colors.BLUE_900
        self.TEXT_PRIMARY = ft.Colors.BLACK87
        self.TEXT_SECONDARY = ft.Colors.GREY_700

        self.page.views.append(self.build())

    def section_spacing(self, content):
        return ft.Container(
            margin=ft.Margin(0, 0, 0, 50),
            content=content
        )

    def build_header(self):
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            content=ft.ResponsiveRow(
                columns=12,
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        col={"xs": 12, "md": 6},
                        alignment=ft.alignment.center_left,
                        content=ft.Row(
                            controls=[
                                ft.Image(src="home/img_home/logo.png", width=50, height=50),
                                ft.Text("FarmConnect", size=22, weight="bold", color=self.PRIMARY_DARK)
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START
                        )
                    ),
                    ft.Container(
                        col={"xs": 12, "md": 6},
                        alignment=ft.alignment.center_right,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            spacing=12,
                            controls=[
                                ft.ElevatedButton(
                                    "Baixe o app agora!",
                                    bgcolor=self.PRIMARY_DARK,
                                    color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(padding=15),
                                ),
                                ft.TextButton(
                                    "Entrar",
                                    on_click=lambda e: self.page.go("/escolha_usuario"),
                                    style=ft.ButtonStyle(padding=15, color=self.PRIMARY)
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def build_hero_section(self):
        title = ft.Text(
            "Facilite, conecte e organize a ",
            size=30,
            weight="bold",
            color=self.TEXT_PRIMARY,
            spans=[
                ft.TextSpan("retirada de medicamentos", ft.TextStyle(color=ft.Colors.BLUE_600, weight="bold"))
            ]
        )
        paragraph = ft.Text(
            "O FarmConnect transforma o agendamento e a retirada de medicamentos especializados, colocando o controle nas mãos dos pacientes. "
            "Garanta mais agilidade, organização e praticidade no acesso aos tratamentos, fortalecendo a conexão entre farmácias públicas e usuários.",
            size=15,
            color=self.TEXT_SECONDARY
        )

        left_column = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Column([title, paragraph], spacing=20, alignment=ft.MainAxisAlignment.START)
        )

        illustration = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Image(
                src="home/img_home/inicio.png",
                width=600,
                height=500,
                fit=ft.ImageFit.CONTAIN
            )
        )

        return ft.Container(
                padding=40,
                content=ft.ResponsiveRow(
                    columns=12,
                    spacing=20,
                    run_spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[left_column, illustration]
                )
            )


    def build_about_section(self):
        about_title = ft.Text("Sobre nós", size=28, weight="bold", color=self.PRIMARY_DARK, text_align=ft.TextAlign.CENTER)
        about_text = ft.Text(
            "Bem-vindo à FarmConnect, sua aliada confiável na gestão de agendamentos e retirada de medicamentos especializados. "
            "Nosso compromisso é transformar a experiência de acesso a medicamentos de alto custo, proporcionando agilidade, organização e praticidade "
            "para pacientes e farmácias públicas.\n\n"
            "Nossa missão é facilitar o agendamento e reagendamento de medicamentos, garantindo que cada paciente tenha seu tratamento assegurado de forma rápida e eficiente. "
            "Acreditamos que o acesso a medicamentos especializados deve ser simples, sem filas, deslocamentos desnecessários ou complicações, e trabalhamos diariamente para tornar essa realidade possível.\n\n"
            "Buscamos fortalecer a relação entre pacientes e farmácias públicas, oferecendo uma plataforma intuitiva e moderna que otimiza o tempo de todos os envolvidos. "
            "Com o FarmConnect, os usuários podem acompanhar seus agendamentos, reagendar quando necessário e receber informações atualizadas sobre a disponibilidade dos medicamentos, "
            "tudo de forma transparente e acessível.\n\n"
            "Estamos comprometidos em continuar inovando, aprimorando nossos serviços e expandindo nossas funcionalidades para atender às necessidades de um sistema de saúde cada vez mais dinâmico. "
            "Acreditamos que a tecnologia pode ser uma ponte para garantir tratamentos mais rápidos e eficientes, melhorando a qualidade de vida de milhares de pessoas.\n\n"
            "Na FarmConnect, cada paciente é nossa prioridade. Junte-se a nós nessa jornada para tornar o acesso aos medicamentos mais humano, ágil e conectado.",
            size=15,
            color=self.TEXT_SECONDARY,
        )

        def benefit(texto):
            return ft.Row([
                ft.Icon(name=ft.Icons.CHECK_CIRCLE_OUTLINED, color=self.PRIMARY),
                ft.Container(
                    expand=True,
                    content=ft.Text(texto, size=13, weight="bold", color=self.TEXT_PRIMARY)
                )
            ], spacing=8)

        benefits_left = ["Agendamento facilitado", "Redução de filas e deslocamentos", "Maior controle sobre retiradas"]
        benefits_right = ["Conveniência para o paciente", "Economia de tempo", "Informações atualizadas em tempo real"]

        benefits_grid = ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Column([benefit(item) for item in benefits_left], spacing=10),
                    col={"xs": 12, "md": 6}
                ),
                ft.Container(
                    content=ft.Column([benefit(item) for item in benefits_right], spacing=10),
                    col={"xs": 12, "md": 6}
                )
            ],
            alignment=ft.MainAxisAlignment.START
        )

        about_image = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Image(
                src="home/img_home/sobre_nos.png",
                width=600,
                height=500,
                fit=ft.ImageFit.CONTAIN
            )
        )

        about_text_column = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Column([
                about_title,
                ft.Container(height=10),
                about_text,
                ft.Container(height=20),
                benefits_grid
            ], spacing=10)
        )

        return self.section_spacing(
            ft.Container(
                padding=40,
                content=ft.ResponsiveRow(
                    columns=12,
                    spacing=20,
                    run_spacing=20,
                    controls=[about_image, about_text_column]
                )
            )
        )


    def build_manage_section(self):
        title = ft.Text("Pacientes: Gerencie seus agendamentos", size=24, weight="bold", color=self.PRIMARY_DARK)
        description = ft.Text(
            "Com recursos como agendamento e reagendamento de retirada de medicamentos, controle de disponibilidade, "
            "e notificações automáticas para retirada. Reduza filas, evite deslocamentos desnecessários "
            "e torne o processo de retirada de medicamentos mais rápido e eficiente em um só lugar.",
            size=15,
            color=self.TEXT_SECONDARY
        )

        def card(icon_name, title_text, subtitle_text):
            return ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=20,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(0, 3),
                    blur_style=ft.ShadowBlurStyle.NORMAL
                ),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Icon(icon_name, size=40, color=self.PRIMARY),
                        ft.Container(height=3, bgcolor=self.PRIMARY, width=60),
                        ft.Text(title_text, size=14, weight="bold", color=self.TEXT_PRIMARY),
                        ft.Text(subtitle_text, size=12, color=self.TEXT_SECONDARY)
                    ]
                )
            )

        cards = [
            card(ft.Icons.PERSON_OUTLINE, "Pacientes", "Gerencie seus agendamentos"),
            card(ft.Icons.LOCAL_PHARMACY_OUTLINED, "Medicamentos", "Controle a disponibilidade"),
            card(ft.Icons.CALENDAR_MONTH_OUTLINED, "Agendar Retirada", "Marque a retirada do medicamento"),
            card(ft.Icons.CALENDAR_MONTH_OUTLINED, "Reagendar Retirada", "Altere a data com facilidade"),
            card(ft.Icons.CHECK_CIRCLE_OUTLINE, "Confirmação", "Confirme o agendamento realizado"),
        ]

        cards_row = ft.ResponsiveRow(
            columns=12,
            spacing=20,
            run_spacing=20,
            controls=[
                ft.Container(col={"xs": 12, "sm": 6, "md": 4}, content=c) for c in cards
            ]
        )

        image = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Image(
                src="home/img_home/paciente.png",
                width=600,
                height=500,
                fit=ft.ImageFit.CONTAIN
            )
        )

        text_column = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Column([title, description, ft.Container(height=20), cards_row], spacing=20)
        )

        return self.section_spacing(ft.Container(
            padding=40,
            content=ft.ResponsiveRow(
                columns=12,
                spacing=20,
                run_spacing=20,
                controls=[text_column, image]
            )
        ))


    def build_admin_section(self):
        title = ft.Text("Administradores: Gerencie agendamentos e estoques", size=24, weight="bold", color=self.PRIMARY_DARK)
        description = ft.Text(
            "Tenha controle completo para aprovar cadastros de pacientes, cadastrar medicamentos, gerenciar estoques, "
            "acompanhar agendamentos e manter o sistema de retirada organizado e eficiente. "
            "Tudo em uma plataforma moderna, prática e segura.",
            size=15,
            color=self.TEXT_SECONDARY
        )

        def admin_card(icon_name, title_text, subtitle_text):
            return ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=20,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.BLACK26,
                    offset=ft.Offset(0, 3),
                    blur_style=ft.ShadowBlurStyle.NORMAL
                ),
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Icon(icon_name, size=40, color=self.PRIMARY),
                        ft.Container(height=3, bgcolor=self.PRIMARY, width=60),
                        ft.Text(title_text, size=14, weight="bold", color=self.TEXT_PRIMARY, text_align=ft.TextAlign.START),
                        ft.Text(subtitle_text, size=12, color=self.TEXT_SECONDARY, text_align=ft.TextAlign.START),
                    ]
                )
            )

        cards = [
            admin_card(ft.Icons.ADD_BOX_OUTLINED, "Cadastrar Medicamentos", "Adicione medicamentos"),
            admin_card(ft.Icons.PERSON_ADD_ALT_1_OUTLINED, "Aprovar Pacientes", "Gerencie solicitações de cadastro"),
            admin_card(ft.Icons.INVENTORY_2_OUTLINED, "Gerenciar Estoque", "Disponibilidade dos medicamentos"),
            admin_card(ft.Icons.DESCRIPTION_OUTLINED, "Agendamentos", "Visualize agendamentos e reagendamentos"),
            admin_card(ft.Icons.NOTIFICATIONS_OUTLINED, "Notificações", "Envie alertas sobre retiradas e prazos"),
        ]

        cards_row = ft.ResponsiveRow(
            columns=12,
            spacing=20,
            run_spacing=20,
            controls=[
                ft.Container(col={"xs": 12, "sm": 6, "md": 4}, content=c) for c in cards
            ]
        )

        image = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Image(
                src="home/img_home/administrador.png",
                width=600,
                height=500,
                fit=ft.ImageFit.CONTAIN
            )
        )

        content_column = ft.Container(
            col={"xs": 12, "md": 6},
            content=ft.Column([title, description, ft.Container(height=20), cards_row], spacing=20)
        )

        return self.section_spacing(ft.Container(
            padding=40,
            content=ft.ResponsiveRow(
                columns=12,
                spacing=20,
                run_spacing=20,
                controls=[image, content_column]
            )
        ))


    def build_footer(self):
        return ft.Container(
            bgcolor=ft.Colors.BLUE_600,
            padding=40,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.ResponsiveRow(
                        columns=12,
                        spacing=10,
                        controls=[
                            ft.Container(
                                col={"xs": 12, "md": 12},
                                alignment=ft.alignment.center,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10,
                                    controls=[
                                        ft.Text("FarmConnect", size=20, weight="bold", color=ft.Colors.GREY_200),
                                        ft.Icon(ft.Icons.LOCAL_PHARMACY_OUTLINED, size=20, color=ft.Colors.GREY_200),
                                    ]
                                )
                            )
                        ]
                    ),
                    ft.Text(
                        "Simplificando o agendamento e retirada de medicamentos especializados.",
                        size=14,
                        color=ft.Colors.WHITE70,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=20, color=ft.Colors.WHITE70),
                    ft.ResponsiveRow(
                        columns=12,
                        spacing=30,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                col={"xs": 12, "md": 4},
                                alignment=ft.alignment.center,
                                content=ft.TextButton("Política de Privacidade", on_click=lambda e: self.page.go("/politica_privacidade")),

                            ),
                            ft.Container(
                                col={"xs": 12, "md": 4},
                                alignment=ft.alignment.center,
                                content=ft.TextButton("Termos de Uso", on_click=lambda e: self.page.go("/termos_uso")),
                            ),
                            ft.Container(
                                col={"xs": 12, "md": 4},
                                alignment=ft.alignment.center,
                                content=ft.TextButton("Contato", on_click=lambda e: self.page.go("/contato")),
                            ),
                        ]
                    ),
                    ft.Text(
                        "FarmConnect © 2025 - Todos os direitos reservados.",
                        size=12,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            )
        )
    
    def politica_privacidade_view(self):
        return ft.View(
            route="/politica_privacidade",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor="#F0F9FF",
                    padding=40,
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LOCK_OUTLINE, size=40, color=ft.Colors.BLUE_700),
                            ft.Text("Política de Privacidade", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ], spacing=10),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                        ft.Container(
                            padding=30,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                            content=ft.Column([

                                ft.Text("🔐 Coleta e Uso de Dados", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Seus dados pessoais (como nome, CPF, e-mail e telefone) são utilizados com responsabilidade para:\n"
                                    "• Agendar retiradas de medicamentos\n"
                                    "• Enviar notificações importantes\n"
                                    "• Garantir a segurança e rastreabilidade do processo",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📁 Compartilhamento", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Seus dados **nunca** são compartilhados com terceiros, salvo em casos de obrigação legal.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("🔄 Atualização e Exclusão", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Você pode solicitar a atualização ou exclusão de seus dados a qualquer momento através da equipe responsável.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📆 Atualizações da Política", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Esta política pode ser atualizada sempre que necessário para refletir melhorias na segurança e privacidade.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📨 Dúvidas ou contato", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Em caso de dúvidas, utilize a opção 'Contato' no rodapé ou envie um e-mail para suporte@farmconnect.com",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),

                                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                                ft.ElevatedButton(
                                    "Voltar para a Página Inicial",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda e: self.page.go("/"),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE_900,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(vertical=14, horizontal=26),
                                        shape=ft.RoundedRectangleBorder(radius=14),
                                        elevation=4
                                    )
                                )
                            ], spacing=18)
                        )
                    ], spacing=30)
                )
            ]
        )

    
    def termos_uso_view(self):
        return ft.View(
            route="/termos_uso",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor="#F0F9FF",
                    padding=40,
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION_OUTLINED, size=40, color=ft.Colors.BLUE_700),
                            ft.Text("Termos de Uso", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ], spacing=10),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                        ft.Container(
                            padding=30,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                            content=ft.Column([

                                ft.Text("✅ Uso da Plataforma", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "O FarmConnect é destinado a facilitar o agendamento e retirada de medicamentos especializados em farmácias públicas. "
                                    "Ao utilizá-lo, você concorda em seguir todas as regras e diretrizes aqui descritas.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("🔑 Cadastro de Usuário", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Para utilizar a plataforma, é necessário fornecer informações verdadeiras e atualizadas. "
                                    "O uso de dados falsos poderá resultar na suspensão ou exclusão da conta.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("🛡️ Segurança e Privacidade", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Seus dados são protegidos conforme nossa Política de Privacidade. "
                                    "Você é responsável por manter a confidencialidade de sua senha e dados de acesso.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("🚫 Condutas Proibidas", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "É proibido utilizar a plataforma para atividades ilegais, fraudes, spam ou manipulação indevida de agendamentos. "
                                    "Tais condutas podem resultar em bloqueio do acesso.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📆 Atualizações dos Termos", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Os termos podem ser modificados a qualquer momento, visando melhorar a experiência dos usuários. "
                                    "Recomenda-se a leitura periódica desta página.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📩 Suporte e Contato", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Em caso de dúvidas, você pode entrar em contato com nossa equipe pelo e-mail: suporte@farmconnect.com.br "
                                    "ou através do botão 'Contato' disponível no rodapé da página.",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),

                                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                                ft.ElevatedButton(
                                    "Voltar para a Página Inicial",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda e: self.page.go("/"),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE_900,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(vertical=14, horizontal=26),
                                        shape=ft.RoundedRectangleBorder(radius=14),
                                        elevation=4
                                    )
                                )
                            ], spacing=18)
                        )
                    ], spacing=30)
                )
            ]
        )

    def contato_view(self):
        return ft.View(
            route="/contato",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor="#F0F9FF",
                    padding=40,
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.CONTACT_PAGE_OUTLINED, size=40, color=ft.Colors.BLUE_700),
                            ft.Text("Fale Conosco", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ], spacing=10),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                        ft.Container(
                            padding=30,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                            content=ft.Column([

                                ft.Text("📨 E-mail de Suporte", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Caso tenha dúvidas, sugestões ou precise de ajuda, envie um e-mail para:\n"
                                    "✉️ suporte@farmconnect.com.br",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📍 Localização", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "FarmConnect - Central de Atendimento\n"
                                    "Rua da Saúde, 123 - Centro\n"
                                    "Rio de Janeiro - RJ, 20000-000",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                                ft.Text("📞 Telefones", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                ft.Text(
                                    "Atendimento: Segunda a Sexta, das 08h às 17h\n"
                                    "📱 (21) 99999-9999  |  ☎️ (21) 2222-2222",
                                    size=16,
                                    color=ft.Colors.GREY_800
                                ),

                                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                                ft.ElevatedButton(
                                    "Voltar para a Página Inicial",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda e: self.page.go("/"),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE_900,
                                        color=ft.Colors.WHITE,
                                        padding=ft.padding.symmetric(vertical=14, horizontal=26),
                                        shape=ft.RoundedRectangleBorder(radius=14),
                                        elevation=4
                                    )
                                )
                            ], spacing=18)
                        )
                    ], spacing=30)
                )
            ]
        )

    def build(self):
        return ft.View(
            route="/",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    content=ft.Column([
                        self.build_header(),
                        self.build_hero_section(),
                        self.build_about_section(),
                        self.build_manage_section(),
                        self.build_admin_section(),
                        self.build_footer()
                    ])
                )
            ]
        )
    
# Teste Local:
if __name__ == "__main__":
    def main(page: ft.Page):
        tela_home = HomeApp(page)
        page.views.append(tela_home.build())
        page.update()

    ft.app(target=main)