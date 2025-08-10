import flet as ft
from functools import partial
from database import listar_medicamentos, carregar_carrinho_usuario, adicionar_ao_carrinho_db, remover_do_carrinho_db, buscar_nome_usuario, diminuir_quantidade_db, aumentar_quantidade_db, buscar_dados_usuario, adicionar_agendamento, listar_agendamentos_usuario, reduzir_estoque_farmacia, consultar_estoque_farmacia, listar_farmacias, consultar_estoque_farmacia, adicionar_ao_carrinho_db, atualizar_dados_usuario, listar_medicamentos_retirados, verificar_agendamentos_vencidos, registrar_medicamento_reservado
from flet import DatePicker
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, grey
from datetime import datetime
from textwrap import wrap


class TelaUsuarioDashboard:
    def __init__(self, page: ft.Page):
        self.page = page
        self.cards_container = ft.ResponsiveRow(run_spacing=20, spacing=20)
        self.pagina_atual = 1
        self.busca_ref = ft.Ref[ft.TextField]()
        self.date_picker_ref = ft.Ref[ft.DatePicker]()
        self.data_escolhida = None
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

        self.carrinho = carregar_carrinho_usuario(self.usuario_id)
        self.contador = {"valor": 0}
        self.carrinho_count = ft.Ref[ft.Text]()
        self.sincronizar_carrinho()
        verificar_agendamentos_vencidos()

        # Cria o drawer do carrinho
        self.carrinho_drawer = self.criar_carrinho_drawer()

    def abrir_tela_reagendamento(self, registro):
        # registro é a tupla retornada por listar_agendamentos_usuario para um agendamento
        # guardamos no client_storage e vamos para a tela
        self.page.client_storage.set("agendamento_para_reagendar", registro)
        self.page.go("/reagendamento")

    def _resolver_agendamento_id(self, registro):
        """Tenta obter o ID do agendamento.
        registro[0] costuma ser o id. Se não for um int, buscamos por código + usuário."""
        try:
            ag_id = int(registro[0])
            return ag_id
        except Exception:
            pass
        try:
            import sqlite3
            codigo = registro[4]  # código do agendamento presente na listagem
            conn = sqlite3.connect("farmconnect.db")
            cur = conn.cursor()
            cur.execute("""
                SELECT id FROM agendamentos
                WHERE codigo = ? AND usuario_id = ?
                ORDER BY id DESC LIMIT 1
            """, (codigo, self.usuario_id))
            row = cur.fetchone()
            cur.close()
            conn.close()
            return row[0] if row else None
        except Exception:
            return None

    def reagendar_agendamento_db(self, agendamento_id, nova_data, novo_horario):
        """Atualiza data/horário e seta status para Pendente.
        Não mexe em estoque nem em medicamento/farmácia."""
        import sqlite3
        conn = sqlite3.connect("farmconnect.db")
        cur = conn.cursor()
        cur.execute("""
            UPDATE agendamentos
            SET data = ?, horario = ?, status = 'Pendente'
            WHERE id = ? AND usuario_id = ?
        """, (nova_data, novo_horario, agendamento_id, self.usuario_id))
        conn.commit()
        linhas = cur.rowcount
        cur.close()
        conn.close()
        return linhas > 0

    def tela_reagendamento(self):
        import datetime
        self.sincronizar_carrinho()

        registro = self.page.client_storage.get("agendamento_para_reagendar")
        if not registro:
            return ft.View(
                route="/reagendamento",
                controls=[
                    self.page.snack_bar,
                    ft.Container(expand=True, alignment=ft.alignment.center,
                                 content=ft.Text("❌ Nenhum agendamento selecionado.", size=18, color=ft.Colors.RED))
                ]
            )

        # Mapeamento do registro conforme listar_agendamentos_usuario
        # [0]=id, [1]=medicamento, [2]=farmacia, [3]=endereco, [4]=codigo, [5]=data, [6]=horario, [7]=status
        med_nome = registro[1]
        farmacia_nome = registro[2]
        endereco = registro[3]
        codigo = registro[4]
        data_atual_str = registro[5]
        horario_atual = registro[6]
        status_atual = registro[7]

        # DatePicker e Dropdown (pré-selecionados)
        horas_disponiveis = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30)]

        # Estado local
        self._reag_data_escolhida = None
        self._reag_data_label = ft.Text("Nenhuma data selecionada ➡️", size=14, color=ft.Colors.GREY_700)
        self._reag_horario_dd = ft.Dropdown(
            label="⏰ Novo horário",
            options=[ft.dropdown.Option(h) for h in horas_disponiveis],
            value=horario_atual if horario_atual in horas_disponiveis else None,
            width=400
        )

        def on_data_change(e):
            self._reag_data_escolhida = e.control.value
            data_formatada = e.control.value.strftime('%d/%m/%Y')
            self._reag_data_label.value = f"Data: {data_formatada}"
            self.page.update()

        # DatePicker
        self._reag_date_picker = ft.DatePicker(
            first_date=datetime.date.today(),
            last_date=datetime.date.today() + datetime.timedelta(days=365),
            on_change=on_data_change
        )
        # Pré-seleciona a data atual do agendamento (se existir)
        try:
            d = datetime.datetime.strptime(data_atual_str, "%Y-%m-%d").date()
            # Não “abre” automaticamente, só marcamos o estado para a label
            self._reag_data_escolhida = d
            self._reag_data_label.value = f"Data: {d.strftime('%d/%m/%Y')}"
        except Exception:
            pass

        if self._reag_date_picker not in self.page.overlay:
            self.page.overlay.append(self._reag_date_picker)

        def abrir_calendario(e):
            self._reag_date_picker.open = True
            self.page.update()

        def confirmar_reagendamento(e):
            # Validações
            if not self._reag_data_escolhida or not self._reag_horario_dd.value:
                self.page.snack_bar.content.value = "❗ Selecione data e horário para reagendar."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return

            ag_id = self._resolver_agendamento_id(registro)
            if not ag_id:
                self.page.snack_bar.content.value = "❌ Não foi possível identificar o agendamento."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return

            nova_data = self._reag_data_escolhida.strftime('%Y-%m-%d')
            novo_horario = self._reag_horario_dd.value

            ok = self.reagendar_agendamento_db(ag_id, nova_data, novo_horario)
            if ok:
                self.page.snack_bar.content.value = "✅ Agendamento reagendado com sucesso! Status voltou para Pendente."
                self.page.snack_bar.bgcolor = ft.Colors.GREEN_500
                self.page.snack_bar.open = True
                self.page.update()
                self.page.go("/agendamentos")
            else:
                self.page.snack_bar.content.value = "❌ Não foi possível reagendar. Tente novamente."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()

        # UI — espelha a tela de agendamento, com título diferente e apenas 1 item
        return ft.View(
            route="/reagendamento",
            controls=[
                self.page.snack_bar,
                self._reag_date_picker,
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
                            ft.Text("🗓️ Reagendamento de Retirada", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Container(
                                width=700,
                                alignment=ft.alignment.center,
                                padding=30,
                                border_radius=24,
                                bgcolor="#F0F9FF",
                                shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                                content=ft.Column(
                                    spacing=20,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Atualize a data e o horário do seu agendamento:", size=18, color=ft.Colors.BLUE_900, text_align=ft.TextAlign.CENTER),
                                        ft.Container(
                                            width=550,
                                            bgcolor="#E8F3FF",
                                            padding=16,
                                            border_radius=16,
                                            content=ft.Column([
                                                ft.Text(f"{med_nome}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                                                ft.Text(f"🏥 Farmácia: {farmacia_nome}", size=14, color=ft.Colors.BLUE_900),
                                                ft.Text(f"📍 Endereço: {endereco}", size=14, color=ft.Colors.BLUE_900),
                                                ft.Text(f"🆔 Código: {codigo}", size=13, color=ft.Colors.GREY_700),
                                                ft.Text(f"Status atual: {status_atual}", size=12, color=ft.Colors.GREY_700),
                                                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                                                self._reag_horario_dd,
                                                ft.Row([
                                                    self._reag_data_label,
                                                    ft.IconButton(
                                                        icon=ft.Icons.CALENDAR_MONTH,
                                                        icon_color=ft.Colors.BLUE_900,
                                                        on_click=abrir_calendario
                                                    )
                                                ])
                                            ], spacing=8)
                                        ),
                                        ft.ElevatedButton(
                                            "Confirmar Reagendamento",
                                            icon=ft.Icons.UPDATE,
                                            on_click=confirmar_reagendamento,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.INDIGO_600,
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
                                icon=ft.Icons.ARROW_BACK,
                                color=ft.Colors.BLUE_900,
                                on_click=lambda e: self.page.go("/agendamentos"),
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

        if self.carrinho_count and self.carrinho_count.current:
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
                "farmacia": m[8],
                "endereco": m[9]
            } for m in dados
        ]

    medicamentos_por_pagina = 8    
    def criar_carrinho_drawer(self):
        return ft.Container(
            width=480,
            height=self.page.height,  # ← ocupa toda a altura da janela
            bgcolor="#FFFFFF",
            padding=30,
            visible=False,
            animate=ft.Animation(300, "easeInOut"),
            border_radius=24,
            shadow=ft.BoxShadow(blur_radius=24, color=ft.Colors.BLACK26, offset=ft.Offset(0, 6)),
            border=ft.border.all(1, color="#E2E8F0"),
            content=ft.Column([
                # Cabeçalho
                ft.Row([
                    ft.Row([
                        ft.Icon(name=ft.Icons.SHOPPING_BAG, size=32, color="#1D4ED8"),
                        ft.Text("Meu Carrinho", size=24, weight=ft.FontWeight.BOLD, color="#1D4ED8")
                    ], spacing=12),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.RED,
                        tooltip="Fechar",
                        icon_size=22,
                        on_click=lambda e: self.fechar_carrinho()
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Divider(thickness=1, color="#CBD5E1"),

                # Conteúdo do carrinho (itens)
                ft.Column(
                    [],
                    spacing=12,
                    expand=True,  # ← ocupa todo o espaço vertical possível
                    scroll=ft.ScrollMode.ALWAYS  # ← scroll se muitos itens
                ),

                ft.Divider(thickness=1, color="#CBD5E1"),

                # Botão confirmar
                ft.ElevatedButton(
                    "Confirmar Retirada",
                    icon=ft.Icons.CHECK,
                    bgcolor="#16A34A",
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14)
                    ),
                    on_click=lambda e: self.page.go("/agendamento")
                )
            ], spacing=20)
        )



    def remover_do_carrinho(self, e=None, item=None):
        if item in self.carrinho:
            self.carrinho.remove(item)
            remover_do_carrinho_db(self.usuario_id, item["id"])
            self.atualizar_contador()
            self.abrir_carrinho()

    def adicionar_ao_carrinho(self, medicamento, quantidade=1):
        try:
            estoque = int(medicamento.get("estoque") or 0)
        except (TypeError, ValueError):
            estoque = 0

        existente = next((item for item in self.carrinho if item["id"] == medicamento["id"]), None)

        if existente:
            if existente["quantidade"] + quantidade <= estoque:
                existente["quantidade"] += quantidade
                for _ in range(quantidade):
                    adicionar_ao_carrinho_db(self.usuario_id, medicamento["id"])
            else:
                self.page.snack_bar.content.value = f"Estoque insuficiente. Disponível: {estoque - existente['quantidade']} unidade(s)."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return
        else:
            if estoque >= quantidade:
                novo = {**medicamento, "quantidade": quantidade}
                self.carrinho.append(novo)
                for _ in range(quantidade):
                    adicionar_ao_carrinho_db(self.usuario_id, medicamento["id"])
            else:
                self.page.snack_bar.content.value = "❗ Medicamento fora de estoque ou quantidade maior que o disponível."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400
                self.page.snack_bar.open = True
                self.page.update()
                return

        self.atualizar_contador()
        self.abrir_carrinho()

    def abrir_detalhes_medicamento(self, e, med):
        self.page.client_storage.set("medicamento_detalhe", med)
        self.page.go("/detalhes_medicamento")

    def abrir_calendario(med_id):
        def handler(self, e):
            self.date_pickers[med_id].open = True
            self.page.update()
        return handler
    
    def abrir_calendario_handler(self, med_id):
        return lambda e: (
            setattr(self.date_pickers[med_id], "open", True),
            self.page.update()
        )

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
                            icon=ft.Icons.REMOVE,
                            icon_color=ft.Colors.BLUE_600,
                            tooltip="Diminuir",
                            on_click=lambda e, med=item: self.diminuir_quantidade(med)
                        ),
                        ft.Text(f"{item['quantidade']} un.", size=14, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            icon_color=ft.Colors.BLUE_600,
                            tooltip="Aumentar",
                            on_click=lambda e, med=item: self.aumentar_quantidade(med)
                        )
                    ], spacing=5)
                ], expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
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

    def sincronizar_carrinho(self):
        self.carrinho = carregar_carrinho_usuario(self.usuario_id)
        self.atualizar_contador()

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
                        content=ft.Row(
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(name=ft.Icons.ADD_SHOPPING_CART, size=18, color=ft.Colors.WHITE),
                                ft.Text("Adicionar", size=14, weight=ft.FontWeight.BOLD)
                            ]
                        ),
                        width=160,
                        height=44,
                        bgcolor=ft.Colors.BLUE_900,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                            overlay_color=ft.Colors.BLUE_700,
                            elevation=6,
                            padding=ft.padding.symmetric(horizontal=16, vertical=10),
                        ),
                        on_click=handler_adicionar
                    )

                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )

        self.page.update()


    def icone_carrinho(self):
        texto = ft.Text(str(self.contador["valor"]), size=10, color=ft.Colors.WHITE, ref=self.carrinho_count)
        return ft.Stack([
            ft.IconButton(
                icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                icon_size=30,
                icon_color="#1E3A8A",
                on_click=self.abrir_carrinho
            ),
            ft.Container(
                content=texto,
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

        self.sincronizar_carrinho()
        self.gerar_cards(self.pagina_atual)
        self.atualizar_contador()

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
                                            prefix_icon=ft.Icons.SEARCH,
                                            border_radius=12,
                                            bgcolor=ft.Colors.WHITE,
                                            height=45,
                                            col={"xs": 12, "md": 6},
                                            on_change=lambda e: self.gerar_cards(None)
                                        ),
                                        ft.Row([
                                            ft.Stack([
                                                ft.IconButton(
                                                    icon=ft.Icons.SHOPPING_BAG_OUTLINED,
                                                    icon_size=30,
                                                    icon_color="#1E3A8A",
                                                    on_click=self.abrir_carrinho
                                                ),
                                                ft.Container(
                                                    content=ft.Text(str(self.contador["valor"]), size=10, color=ft.Colors.WHITE, ref=self.carrinho_count),
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
                                            ft.OutlinedButton("."),
                                            ft.OutlinedButton("."),
                                            ft.OutlinedButton("."),
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
        self.sincronizar_carrinho()
        return ft.View(
            route="/documentos",
            scroll=ft.ScrollMode.AUTO,
            bgcolor="#F0F9FF",
            controls=[
                self.page.snack_bar,
                ft.Container(
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
                                icon=ft.Icons.FILE_DOWNLOAD,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_900,
                                color=ft.Colors.WHITE,
                                width=260,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=12),
                                    padding=ft.padding.symmetric(vertical=12)
                                ),
                                on_click=lambda e: self.gerar_documento_autorizacao()
                            ),
                            ft.ElevatedButton(
                                "Voltar",
                                icon=ft.Icons.ARROW_BACK_IOS_NEW,
                                bgcolor=ft.Colors.GREY_50,
                                color=ft.Colors.BLUE_900,
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
        self.sincronizar_carrinho()

        self.campos = {
            "nome": ft.Ref[ft.TextField](),
            "cpf": ft.Ref[ft.TextField](),
            "nasc": ft.Ref[ft.TextField](),
            "email": ft.Ref[ft.TextField](),
            "tel": ft.Ref[ft.TextField](),
        }

        self.dados_usuario = buscar_dados_usuario(self.email_usuario) or {
            "nome": "Desconhecido",
            "cpf": "",
            "nasc": "",
            "email": self.email_usuario,
            "tel": "(00) 00000-0000"
        }

        def salvar_todos(e=None):
            for campo in self.campos:
                self.dados_usuario[campo] = self.campos[campo].current.value

            sucesso = atualizar_dados_usuario(
                self.email_usuario,
                self.dados_usuario["nome"],
                self.dados_usuario["cpf"],
                self.dados_usuario["nasc"],
                self.dados_usuario["email"],
                self.dados_usuario["tel"]
            )

            if sucesso:
                self.page.session.set("usuario_nome", self.dados_usuario["nome"])
                self.page.session.set("usuario_email", self.dados_usuario["email"])
                self.email_usuario = self.dados_usuario["email"]
                self.page.snack_bar.content.value = "Dados atualizados com sucesso!"
                self.page.snack_bar.bgcolor = ft.Colors.GREEN_500
            else:
                self.page.snack_bar.content.value = "Erro ao atualizar. Tente novamente."
                self.page.snack_bar.bgcolor = ft.Colors.RED_400

            self.page.snack_bar.open = True
            self.page.update()
        def campo_editavel(label, campo, icone):
            return ft.Column([
                ft.Row([
                    ft.Icon(icone, size=20, color=ft.Colors.BLUE_900),
                    ft.Text(label, size=14, weight="bold", color=ft.Colors.BLUE_900),
                    ft.Container(expand=True),
                    ft.IconButton(  # apenas visual
                        icon=ft.Icons.EDIT,
                        icon_color=ft.Colors.BLUE_700,
                        tooltip="Campo editável"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Container(
                        expand=True,
                        content=ft.TextField(
                            ref=self.campos[campo],
                            value=self.dados_usuario[campo],
                            border_radius=12,
                            filled=True,
                            bgcolor="#F3F4F6",
                            dense=True,
                            text_size=15,
                            content_padding=ft.padding.all(12),
                            border_color=ft.Colors.GREY_300,
                            on_submit=salvar_todos
                        )
                    )
                ])
            ], spacing=6)
            

        return ft.View(
            route="/perfil",
            scroll=ft.ScrollMode.AUTO,
            bgcolor="#F0F9FF",
            controls=[
                self.page.snack_bar,
                ft.Container(
                    expand=True,
                    padding=30,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text("👤 Perfil do Paciente", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    width=700,
                                    padding=30,
                                    bgcolor=ft.Colors.WHITE,
                                    border_radius=20,
                                    shadow=ft.BoxShadow(blur_radius=24, color=ft.Colors.BLACK26, offset=ft.Offset(0, 12)),
                                    content=ft.Column([
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Column(
                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                    spacing=8,
                                                    controls=[
                                                        ft.Text(self.dados_usuario["nome"], size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                                        ft.Text("Paciente FarmConnect", size=14, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                                                    ]
                                                )
                                            ]
                                        ),
                                        ft.Divider(height=30),
                                        campo_editavel("Nome completo", "nome", ft.Icons.PERSON),
                                        campo_editavel("CPF", "cpf", ft.Icons.BADGE),
                                        campo_editavel("Data de nascimento", "nasc", ft.Icons.CALENDAR_MONTH),
                                        campo_editavel("Email", "email", ft.Icons.EMAIL),
                                        campo_editavel("Telefone", "tel", ft.Icons.PHONE)
                                    ], spacing=25)
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    "Salvar",
                                    icon=ft.Icons.SAVE,
                                    icon_color = ft.Colors.WHITE,
                                    bgcolor=ft.Colors.BLUE_900,
                                    color=ft.Colors.WHITE,
                                    width=160,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=16),
                                        padding=ft.padding.symmetric(vertical=12),
                                        elevation=4
                                    ),
                                    on_click=salvar_todos
                                )
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton(
                                    "Voltar",
                                    icon=ft.Icons.ARROW_BACK,
                                    bgcolor=ft.Colors.GREY_50,
                                    color=ft.Colors.BLUE_900,
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
                    ], spacing=30, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]
        )


    def tela_medicamentos_retirados(self):
        import datetime
        self.sincronizar_carrinho()
        dados_retirados = listar_medicamentos_retirados(self.usuario_id)

        self.resultados_filtrados = dados_retirados

        def filtrar_medicamentos(e):
            termo = e.control.value.lower()
            self.resultados_filtrados = [
                item for item in dados_retirados
                if termo in item[0].lower()  # item[0] = nome do medicamento
            ]
            self.page.go("/medicamentos_retirados")

        medicamentos_exibidos = []
        for nome, data, horario, farmacia, endereco, quantidade in self.resultados_filtrados:
            data_formatada = datetime.datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y") if data else "-"
            medicamentos_exibidos.append(
                ft.Container(
                    padding=20,
                    bgcolor="#F8FAFC",
                    border_radius=16,
                    margin=ft.margin.only(bottom=20),
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                    content=ft.Column([
                        ft.Text(nome, size=20, weight=ft.FontWeight.BOLD, color="#111827"),
                        ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                        ft.Text(f"\U0001F3E5 Farmácia: {farmacia or 'Não disponível'}", size=14, color="#374151"),
                        ft.Text(f"📍 Endereço: {endereco or 'Não disponível'}", size=14, color="#374151"),
                        ft.Text(f"\U0001F4C5 Data de Retirada: {data_formatada}", size=14, color="#374151"),
                        ft.Text(f"⏰ Horário: {horario or 'Não informado'}", size=14, color="#374151"),
                        ft.Text(f"\U0001F4E6 Quantidade: {quantidade} unidades", size=14, color="#374151"),
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )

        return ft.View(
            route="/medicamentos_retirados",
            scroll=ft.ScrollMode.AUTO,
            bgcolor="#F0F9FF",
            controls=[
                self.page.snack_bar,
                ft.Container(
                    expand=True,
                    padding=40,
                    content=ft.Column([
                        ft.Text(
                            "MEDICAMENTOS RETIRADOS", 
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
                                    ft.TextField(
                                        label="🔍 Buscar Medicamento",
                                        expand=True,
                                        border_radius=30,
                                        on_change=filtrar_medicamentos
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.SEARCH,
                                        icon_color=ft.Colors.BLUE_900,
                                        on_click=lambda e: None
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                                ft.ListView(
                                    expand=True,
                                    controls=medicamentos_exibidos
                                )
                            ], spacing=20)
                        ),
                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                        ft.ElevatedButton(
                            "Voltar",
                            icon=ft.Icons.ARROW_BACK_IOS_NEW,
                            bgcolor=ft.Colors.GREY_50,
                            color=ft.Colors.BLUE_900,
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
        import datetime
        self.sincronizar_carrinho()

        farmacias = listar_farmacias()
        opcoes_farmacia = [ft.dropdown.Option(str(f[0]), f[1]) for f in farmacias]
        horas_disponiveis = [f"{h:02d}:{m:02d}" for h in range(8, 18) for m in (0, 30)]

        self.horarios_por_med = {}
        self.datas_escolhidas = {}
        self.datas_label_por_med = {}
        self.date_pickers = {}

        medicamento_inputs = []
        for item in self.carrinho:
            med_id = item["id"]

            self.horarios_por_med[med_id] = ft.Dropdown(
                label="⏰ Horário",
                options=[ft.dropdown.Option(h) for h in horas_disponiveis],
                width=400
            )

            self.datas_escolhidas[med_id] = None
            self.datas_label_por_med[med_id] = ft.Text("Nenhuma data selecionada ➡️", size=14, color=ft.Colors.GREY_700)

            def gerar_on_data(med_id):
                def on_data(e):
                    self.datas_escolhidas[med_id] = e.control.value
                    data_formatada = e.control.value.strftime('%d/%m/%Y')
                    self.datas_label_por_med[med_id].value = f"Data: {data_formatada}"
                    self.page.update()
                return on_data

            self.date_pickers[med_id] = ft.DatePicker(
                first_date=datetime.date.today(),
                last_date=datetime.date.today() + datetime.timedelta(days=365),
                on_change=gerar_on_data(med_id)
            )

            self.page.overlay.append(self.date_pickers[med_id])

            med_info = next((m for m in listar_medicamentos() if m[0] == med_id), None)
            farmacia_nome = med_info[8] if med_info else "Não disponível"
            farmacia_endereco = med_info[9] if med_info else "Endereço não encontrado" 

            medicamento_inputs.append(
                ft.Container(
                    width=550,
                    bgcolor="#F0F9FF",
                    padding=16,
                    border_radius=16,
                    content=ft.Column([
                        ft.Text(f"{item['nome']} ({item['quantidade']} un.)", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Text(f"🏥 Farmácia: {farmacia_nome}", size=14, color=ft.Colors.BLUE_900),
                        ft.Text(f"📍 Endereço: {farmacia_endereco}", size=14, color=ft.Colors.BLUE_900),
                        self.horarios_por_med[med_id],
                        ft.Row([
                            self.datas_label_por_med[med_id],
                            ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.BLUE_900, on_click=self.abrir_calendario_handler(med_id)
                            )
                        ])
                    ], spacing=10)
                )
            )

        def confirmar_agendamento(e):
            for item in self.carrinho:
                med_id = item["id"]
                codigo = item["codigo"]
                quantidade = item["quantidade"]

                med_info = next((m for m in listar_medicamentos() if m[0] == med_id), None)
                horario_dd = self.horarios_por_med.get(med_id)
                data_obj = self.datas_escolhidas.get(med_id)

                if not horario_dd or not data_obj:
                    self.page.snack_bar.content.value = f"❗ Preencha todos os campos para o agendamento."
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
                    return
                
                if not med_info or not med_info[8]:
                    self.page.snack_bar.content.value = f"❗ Não foi possível identificar a farmácia do medicamento {item['nome']}."
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
                    return

                farmacia_id = med_info[10] 

                horario = horario_dd.value
                data = data_obj.strftime('%Y-%m-%d')

                estoque = consultar_estoque_farmacia(farmacia_id, med_id)
                if estoque < quantidade:
                    self.page.snack_bar.content.value = f"❌ Estoque insuficiente para {item['nome']}!"
                    self.page.snack_bar.bgcolor = ft.Colors.RED_400
                    self.page.snack_bar.open = True
                    self.page.update()
                    return

                reduzir_estoque_farmacia(farmacia_id, med_id, quantidade)
                adicionar_agendamento(self.usuario_id, med_id, farmacia_id, codigo, data, horario, "Pendente", quantidade)
                registrar_medicamento_reservado(self.usuario_id, med_id, quantidade)

            for item in self.carrinho:
                remover_do_carrinho_db(self.usuario_id, item["id"])
            self.carrinho.clear()
            self.atualizar_contador()

            self.page.snack_bar.content.value = "✅ Agendamentos realizados com sucesso!"
            self.page.snack_bar.bgcolor = ft.Colors.GREEN_500
            self.page.snack_bar.open = True
            self.page.update()
            self.page.go("/agendamento_confirmado")

        if self.page.snack_bar not in self.page.overlay:
            self.page.overlay.append(self.page.snack_bar)

        return ft.View(
            route="/agendamento",
            controls=[
                self.page.snack_bar,
                *self.date_pickers.values(),
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
                                alignment=ft.alignment.center,
                                padding=30,
                                border_radius=24,
                                bgcolor="#F0F9FF",
                                shadow=ft.BoxShadow(blur_radius=25, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                                content=ft.Column(
                                    spacing=25,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Escolha a data e o horário desejado:", size=18, color=ft.Colors.BLUE_900, text_align=ft.TextAlign.CENTER),
                                        ft.Column(
                                            controls=medicamento_inputs,
                                            spacing=20,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                        ft.ElevatedButton(
                                            "Confirmar Agendamento",
                                            icon=ft.Icons.CHECK_CIRCLE,
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
                                icon=ft.Icons.ARROW_BACK,
                                color=ft.Colors.BLUE_900,
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
        medicamento = self.page.client_storage.get("medicamento_detalhe")
        self.sincronizar_carrinho()

        if not medicamento:
            return ft.View(
                route="/detalhes_medicamento",
                controls=[
                    self.page.snack_bar,
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Text("❌ Nenhum medicamento selecionado.", size=20, color=ft.Colors.RED)
                    )
                ]
            )

        self.qtd_ref = ft.Ref[ft.TextField]()
        self.imagem_principal = ft.Ref[ft.Image]()

        def trocar_imagem(nova_src):
            def handler(e):
                self.imagem_principal.current.src = nova_src
                self.imagem_principal.current.update()
            return handler

        conteudo = ft.Container(
            expand=True,
            bgcolor="#F9FAFB",
            padding=30,
            content=ft.Column(
                spacing=30,
                controls=[
                    # Header com título e ícones
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            tooltip="Voltar",
                            icon_color="#1E3A8A",
                            on_click=lambda e: self.page.go("/usuario")
                        ),
                        ft.Text("Detalhes do Medicamento", size=28, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                        ft.Container(expand=True),
                        self.icone_carrinho(),
                        ft.CircleAvatar(foreground_image_src="/images/profile.jpg", radius=20),
                        ft.Text(self.nome_usuario.upper(), size=13, weight=ft.FontWeight.BOLD)
                    ]),

                    # Imagem e info do medicamento
                    ft.ResponsiveRow([
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            padding=20,
                            bgcolor="white",
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK26, offset=ft.Offset(0, 10)),
                            content=ft.Column([
                                ft.Image(ref=self.imagem_principal, src=medicamento["imagem"], width=300, height=300),
                                ft.Row([
                                    ft.GestureDetector(
                                        content=ft.Image(src=medicamento["imagem"], width=60, height=60),
                                        on_tap=trocar_imagem(medicamento["imagem"])
                                    ) for _ in range(3)
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                            ], spacing=15)
                        ),
                        ft.Container(
                            col={"sm": 12, "md": 6},
                            padding=20,
                            content=ft.Column([
                                ft.Text(medicamento["nome"], size=26, weight=ft.FontWeight.BOLD, color="#1E3A8A"),
                                ft.Text("Tipo: Uso controlado", size=14),
                                ft.Text("Marca: " + medicamento['fabricante'], size=14),
                                ft.Text(f"Quantidade: {medicamento['estoque']}", size=14),
                                ft.Text(f"Farmácia: {medicamento.get('farmacia', 'Não disponível')}", size=14),
                                ft.Text(f"Endereço: {medicamento.get('endereco', 'Não disponível')}", size=14),
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
                                        icon=ft.Icons.ADD_SHOPPING_CART,
                                        icon_color=ft.Colors.WHITE,
                                        style=ft.ButtonStyle(
                                            bgcolor="#1E3A8A",
                                            color=ft.Colors.WHITE,
                                            padding=ft.padding.symmetric(vertical=14, horizontal=20),
                                            shape=ft.RoundedRectangleBorder(radius=12)
                                        ),
                                        on_click=lambda e: self.adicionar_ao_carrinho(medicamento, int(self.qtd_ref.current.value or "1"))
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
                            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                            content=ft.Column([
                                ft.Text("📘 Descrição", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Medicamento de uso controlado, indicado conforme prescrição médica. Para garantir sua eficácia e segurança, utilize conforme orientação profissional.", size=14),
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
                            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK26, offset=ft.Offset(0, 8)),
                            content=ft.Column([
                                ft.Text("📦 Características", size=20, weight=ft.FontWeight.BOLD),
                                ft.Divider(),
                                ft.Row([ft.Text("Código: ", expand=True), ft.Text(medicamento["codigo"])]),
                                ft.Row([ft.Text("Peso:", expand=True), ft.Text("1g")]),
                                ft.Row([ft.Text("Marca: ", expand=True), ft.Text(medicamento["fabricante"])]),
                            ], spacing=8)
                        )
                    ], run_spacing=20, spacing=30)
                ]
            )
        )

        return ft.View(
            route="/detalhes_medicamento",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self.page.snack_bar,
                ft.Stack(
                    expand=True,
                    controls=[
                        conteudo,
                        ft.Container(
                            content=self.carrinho_drawer,
                            left=0,
                            top=0
                        )
                    ]
                )
            ]
        )



    
    def tela_meus_agendamentos(self):
        from database import listar_agendamentos_usuario
        agendamentos = listar_agendamentos_usuario(self.usuario_id)
        self.sincronizar_carrinho()
        def status_badge(status):
            cores = {
                "Pendente": (ft.Colors.AMBER_700, ft.Colors.AMBER_100),
                "Confirmado": (ft.Colors.GREEN_600, ft.Colors.GREEN_100),
                "Cancelado": (ft.Colors.RED_600, ft.Colors.RED_100),
            }
            cor_texto, cor_bg = cores.get(status, (ft.Colors.GREY, ft.Colors.GREY_200))
            icone = (
                ft.Icons.CHECK_CIRCLE_OUTLINE if status == "Confirmado"
                else ft.Icons.HOURGLASS_EMPTY if status == "Pendente"
                else ft.Icons.CANCEL
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
        for ag in agendamentos:
            agendamento = {
                "medicamento": ag[1],
                "farmacia": ag[2],
                "endereco": ag[3],
                "codigo": ag[4],
                "data": ag[5],
                "horario": ag[6],
                "status": ag[7],
            }

            badge = status_badge(agendamento["status"])

            # importante: usar lambda com default para capturar valor corretamente
            acoes = ft.Row([
                ft.ElevatedButton(
                    "Reagendar",
                    icon=ft.Icons.UPDATE,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=14, vertical=8),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        bgcolor=ft.Colors.INDIGO_100,
                        color=ft.Colors.INDIGO_900
                    ),
                    on_click=lambda e, registro=ag: self.abrir_tela_reagendamento(registro)
                ),
                ft.ElevatedButton(
                    "📥 Comprovante",
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        shape=ft.RoundedRectangleBorder(radius=12),
                        bgcolor=ft.Colors.BLUE_800,
                        color=ft.Colors.WHITE
                    ),
                    on_click=lambda e, dados=ag: self.gerar_pdf_comprovante(dados)
                )
            ], spacing=10)


            cards.append(
                ft.Container(
                    padding=20,
                    margin=10,
                    border_radius=12,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK26),
                    content=ft.Column([
                        ft.Text(f"💊 Medicamento: {agendamento['medicamento']}", size=16, weight="bold"),
                        ft.Text(f"🏥 Farmácia: {agendamento['farmacia']}"),
                        ft.Text(f"📍Endereço: {agendamento['endereco']} "),
                        ft.Text(f"🆔 Código: {agendamento['codigo']}"),
                        ft.Text(f"📅 Data: {agendamento['data']}"),
                        ft.Text(f"⏰ Horário: {agendamento['horario']}"),
                        badge,
                        acoes
                    ], spacing=5)
                )
            )

        conteudo = (
            ft.Container(
                content=ft.Column(cards, spacing=20),
            )
            if cards else
            ft.Container(
                content=ft.Column([
                    ft.Text("📭 Nenhum agendamento encontrado", size=20, color=ft.Colors.GREY_600),
                    ft.Text("Você ainda não possui agendamentos realizados.", size=14, color=ft.Colors.GREY_500),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=60,
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.BLACK26)
            )
        )

        return ft.View(
            route="/agendamentos",
            scroll=ft.ScrollMode.AUTO,
            bgcolor="#F0F9FF",  # ✅ Scroll só aqui
            controls=[
                self.page.snack_bar,
                ft.Container(
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
                                icon=ft.Icons.DESCRIPTION,
                                tooltip="Ver documentos necessários",
                                icon_color=ft.Colors.BLUE_700,
                                on_click=lambda e: self.page.go("/documentos")
                            )
                        ),
                        ft.Column([
                            ft.Icon(name=ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_900, size=32),
                            ft.Text("Meus Agendamentos", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8),
                        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),

                        # Conteúdo dos cards + botões no fim
                        conteudo,  # Cards de agendamentos

                        ft.Divider(height=30, color=ft.Colors.TRANSPARENT),

                        ft.ElevatedButton(
                            "Voltar",
                            icon=ft.Icons.ARROW_BACK_IOS_NEW,
                            bgcolor=ft.Colors.GREY_50,
                            color=ft.Colors.BLUE_900,
                            width=160,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=16),
                                padding=ft.padding.symmetric(vertical=14)
                            ),
                            on_click=lambda e: self.page.go("/usuario")
                        ),

                        ft.Container(height=40)  # espaço extra final para segurança
                    ],
                    spacing=30,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ]
        )
    
    def tela_agendamento_confirmado(self):
        from database import listar_agendamentos_usuario
        self.sincronizar_carrinho()

        # Último agendamento do usuário
        agendamentos = listar_agendamentos_usuario(self.usuario_id)
        ultimo = agendamentos[0] if agendamentos else None

        return ft.View(
            route="/agendamento_confirmado",
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self.page.snack_bar,
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
                            ft.Container(
                                padding=30,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=20,
                                shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK12, offset=ft.Offset(0, 10)),
                                content=ft.Column([
                                    ft.Icon(name=ft.Icons.HOURGLASS_TOP, size=80, color=ft.Colors.AMBER_700),
                                    ft.Text(
                                        "Agendamento Recebido!",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_900,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Text(
                                        "Seu agendamento foi registrado com sucesso e está aguardando aprovação do administrador.",
                                        size=18,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Text(
                                        f"🏥 Farmácia: {ultimo[2]}" if ultimo else "🏥 Farmácia: Não disponível",
                                        size=16,
                                        text_align=ft.TextAlign.CENTER,
                                        color=ft.Colors.BLUE_600,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        f"📍 Endereço da Farmácia: {ultimo[3]}" if ultimo else "📍 Endereço da Farmácia: Não disponível",
                                        size=16,
                                        text_align=ft.TextAlign.CENTER,
                                        color=ft.Colors.BLUE_600,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Text(
                                        "Você poderá acompanhar o status na aba 'Meus Agendamentos'.",
                                        size=16,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(height=20),
                                    ft.Container(
                                        bgcolor=ft.Colors.AMBER_100,
                                        padding=16,
                                        border_radius=12,
                                        content=ft.Column([
                                            ft.Row([
                                                ft.Icon(name=ft.Icons.INFO_OUTLINE, color=ft.Colors.AMBER_700),
                                                ft.Text(
                                                    "Importante!",
                                                    color=ft.Colors.AMBER_900,
                                                    weight=ft.FontWeight.BOLD,
                                                    size=16
                                                )
                                            ], spacing=8),
                                            ft.Text(
                                                "• Verifique em 'Meus Agendamentos' se o status mudou para CONFIRMADO.\n"
                                                "• Leve o comprovante de agendamento impresso no dia da retirada.\n"
                                                "• Você tem até 20 dias para realizar a retirada.\n",
                                                size=14,
                                                color=ft.Colors.AMBER_900
                                            )
                                        ], spacing=10)
                                    ),
                                    ft.Container(height=25),
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "Ver Meus Agendamentos",
                                            icon=ft.Icons.CALENDAR_MONTH,
                                            style=ft.ButtonStyle(
                                                bgcolor=ft.Colors.BLUE_900,
                                                icon_color=ft.Colors.WHITE,
                                                color=ft.Colors.WHITE,
                                                padding=ft.padding.symmetric(horizontal=24, vertical=14),
                                                shape=ft.RoundedRectangleBorder(radius=12)
                                            ),
                                            on_click=lambda e: self.page.go("/agendamentos")
                                        ),
                                        ft.ElevatedButton(
                                            text="📥 Baixar Comprovante",
                                            bgcolor=ft.Colors.BLUE_600,
                                            color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=14),
                                                padding=ft.padding.symmetric(horizontal=24, vertical=14),
                                                elevation=8,
                                                overlay_color="#3B82F6"
                                            ),
                                            on_click=lambda e: self.gerar_pdf_comprovante(ultimo)
                                        ),
                                        ft.OutlinedButton(
                                            "Voltar à Página Inicial",
                                            icon=ft.Icons.HOME_OUTLINED,
                                            style=ft.ButtonStyle(
                                                padding=ft.padding.symmetric(horizontal=24, vertical=14),
                                                shape=ft.RoundedRectangleBorder(radius=12),
                                                color=ft.Colors.BLUE_800,
                                            ),
                                            on_click=lambda e: self.page.go("/usuario")
                                        )
                                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER)
                                ], spacing=20)
                            )
                        ]
                    )
                )
            ]
        )
    
    def gerar_pdf_comprovante(self, agendamento):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor
        from datetime import datetime

        if not agendamento:
            self.page.snack_bar.content.value = "❌ Nenhum agendamento encontrado."
            self.page.snack_bar.bgcolor = "red"
            self.page.snack_bar.open = True
            self.page.update()
            return

        caminho = "comprovante_agendamento.pdf"
        c = canvas.Canvas(caminho, pagesize=A4)
        largura, altura = A4

        # Título
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(HexColor("#1E3A8A"))
        c.drawCentredString(largura / 2, altura - 2 * cm, "Comprovante de Agendamento")

        # Dados do paciente
        y = altura - 3.5 * cm
        c.setFont("Helvetica", 12)
        c.setFillColor("black")
        c.drawString(2 * cm, y, f"Nome do Paciente: {self.nome_usuario}")
        y -= 1 * cm
        c.drawString(2 * cm, y, f"E-mail: {self.email_usuario}")

        # Detalhes do agendamento
        y -= 1.5 * cm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2 * cm, y, "■ Detalhes do Agendamento")
        c.setFont("Helvetica", 11)

        y -= 0.8 * cm
        c.drawString(2 * cm, y, f"Medicamento: {agendamento[1]}")         # Nome do medicamento
        y -= 0.6 * cm
        c.drawString(2 * cm, y, f"Farmácia: {agendamento[2]}")            # Nome da farmácia
        y -= 0.6 * cm
        c.drawString(2 * cm, y, f"Endereço: {agendamento[3]}")            # Endereço
        y -= 0.6 * cm
        c.drawString(2 * cm, y, f"Data: {agendamento[5]}")                # Data do agendamento
        y -= 0.6 * cm
        c.drawString(2 * cm, y, f"Horário: {agendamento[6]}")             # Horário
        y -= 0.6 * cm
        c.drawString(2 * cm, y, f"Status atual: {agendamento[7]}")        # Status do agendamento

        from datetime import datetime, timedelta
        validade_limite = datetime.strptime(agendamento[5], "%Y-%m-%d") + timedelta(days=20)
        c.drawString(2 * cm, y - 0.8 * cm, f" Validade: até {validade_limite.strftime('%d/%m/%Y')}")
        y -= 1.5 * cm


        # Rodapé
        y -= 2 * cm
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(HexColor("#6B7280"))
        c.drawString(2 * cm, y, "Leve este comprovante impresso no dia da retirada.")
        y -= 0.6 * cm
        c.drawString(2 * cm, y, f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

        c.save()
        self.page.launch_url(caminho)



    def gerar_documento_autorizacao(self):
        caminho = "documento_autorizacao.pdf"
        c = canvas.Canvas(caminho, pagesize=A4)
        largura, altura = A4
        margem = 2.5 * cm
        y = altura - margem

        azul_escuro = HexColor("#1E3A8A")
        cinza_suave = HexColor("#6B7280")

        def centralizado(texto, tamanho=12, bold=False, desloca=0.8 * cm, cor=black):
            nonlocal y
            c.setFont("Helvetica-Bold" if bold else "Helvetica", tamanho)
            c.setFillColor(cor)
            c.drawCentredString(largura / 2, y, texto)
            y -= desloca

        def campo_rotulado(rotulo, largura_linha=15.5 * cm):
            nonlocal y
            c.setFont("Helvetica", 11)
            c.setFillColor(black)
            c.drawString(margem, y, rotulo)
            y -= 0.5 * cm
            c.setStrokeColor(grey)
            c.setLineWidth(0.5)
            c.line(margem, y, margem + largura_linha, y)
            y -= 1.0 * cm

        def desenhar_texto_quebrado(texto, largura_max=95):
            nonlocal y
            linhas = wrap(texto, width=largura_max)
            for linha in linhas:
                c.drawString(margem + 0.5 * cm, y, linha)
                y -= 0.5 * cm

        # Cabeçalho
        centralizado("FarmConnect", tamanho=16, bold=True, cor=azul_escuro, desloca=1.2 * cm)
        centralizado("Autorização para Retirada de Medicamentos por Terceiros", tamanho=13, bold=True)
        centralizado("Documento obrigatório para retirada por pessoa diferente do paciente.", tamanho=10, cor=cinza_suave, desloca=1.2 * cm)

        # Campos
        campo_rotulado("Nome do Paciente (Titular):")
        campo_rotulado("CPF do Paciente:")
        campo_rotulado("RG do Paciente:")
        campo_rotulado("Nome do Responsável pela Retirada:")
        campo_rotulado("CPF do Responsável:")
        campo_rotulado("RG do Responsável:")

        # Declaração
        c.setFont("Helvetica", 11)
        c.drawString(margem, y, "Declaração:")
        y -= 0.6 * cm

        declaracao_1 = (
            "Declaro estar ciente de que o(a) responsável acima está autorizado(a) a retirar meus medicamentos, "
        )
        declaracao_2 = (
            "Esta autorização é válida somente para a data especificada no agendamento."
        )

        desenhar_texto_quebrado(f"- {declaracao_1}")
        y -= 0.3 * cm
        desenhar_texto_quebrado(f"- {declaracao_2}")

        # Assinatura
        y -= 1.5 * cm
        c.setStrokeColor(grey)
        c.line(margem, y, largura - margem, y)
        y -= 0.5 * cm
        centralizado("Assinatura do Paciente ou Responsável Legal", tamanho=11, cor=cinza_suave)

        # Data
        data_atual = datetime.now().strftime("%d/%m/%Y")
        y -= 1.5 * cm
        c.setFont("Helvetica", 11)
        c.drawString(margem, y, f"Data: {data_atual}")

        # Rodapé
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(cinza_suave)
        c.drawCentredString(largura / 2, 1.5 * cm, "Documento gerado automaticamente via FarmConnect")

        # Marca d'água
        c.setFont("Helvetica", 50)
        c.setFillColor(HexColor("#F3F4F6"))
        c.saveState()
        c.translate(largura / 4, altura / 2)
        c.rotate(30)
        c.drawString(0, 0, "FARMCONNECT")
        c.restoreState()

        c.save()
        self.page.launch_url(caminho)





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
            elif page.route == "/reagendamento":
                page.views.append(dashboard.tela_reagendamento())
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



