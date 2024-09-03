import flet as ft
from flet_core.types import WEB_BROWSER


def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = 'Hospital Assist - Maqueiros'
    page.window_max_width = 400
    page.window_max_height = 650
    page.bgcolor = '#F5F5F5'  # Cor de fundo neutra (cinza claro)

    # Função para retornar à tela principal
    def voltar_para_menu_principal(e):
        page.controls.clear()
        page.add(nome, menu)
        page.update()

    # Função chamada ao clicar em "Chamados"
    def button_clicked_chamados(e):
        solicitacoes = ft.ListView(expand=1, spacing=10, padding=20)
        historico = []

        # Aceitar solicitação
        def aceitar_solicitacao(e):
            historico.append({"id": e.control.key, "status": "Aceito"})
            e.control.visible = False
            page.update()

        # Recusar solicitação
        def recusar_solicitacao(e):
            historico.append({"id": e.control.key, "status": "Recusado"})
            e.control.visible = False
            page.update()

        # Adicionar nova solicitação
        def adicionar_solicitacao():
            solicitacao_id = len(historico) + 1
            solicitacao = ft.Row(
                key=str(solicitacao_id),
                controls=[
                    ft.Text(f"Transporte {solicitacao_id}", size=15, color='#333333'),  # Texto em tom de cinza escuro
                    ft.ElevatedButton(
                        text="Aceitar",
                        on_click=aceitar_solicitacao,
                        bgcolor='#E0E0E0',  # Botão em cinza claro
                        color='#333333'  # Texto do botão em cinza escuro
                    ),
                    ft.ElevatedButton(
                        text="Recusar",
                        on_click=recusar_solicitacao,
                        bgcolor='#E0E0E0',
                        color='#333333'
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
            solicitacoes.controls.append(solicitacao)
            page.update()

        # Exibir histórico de solicitações
        def exibir_historico(e):
            historico_str = "\n".join(
                [f"Solicitação {item['id']}: {item['status']}" for item in historico]
            )
            dialog = ft.AlertDialog(
                title=ft.Text("Histórico de Solicitações", color='white'),
                content=ft.Text(historico_str, color='white'),  # Texto do histórico em cinza médio
                on_dismiss=lambda e: print("Dialog dismissed")
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        # Botões de controle
        adicionar_button = ft.ElevatedButton(
            text="Adicionar Solicitação",
            bgcolor='#E0E0E0',
            color='#333333',
            on_click=lambda e: adicionar_solicitacao()
        )
        historico_button = ft.ElevatedButton(
            text="Exibir Histórico",
            bgcolor='#E0E0E0',
            color='#333333',
            on_click=exibir_historico
        )

        # Botão Voltar
        voltar_button = ft.ElevatedButton(
            text="Voltar",
            bgcolor='#E0E0E0',
            color='#333333',
            on_click=voltar_para_menu_principal
        )

        # Limpa o conteúdo da página antes de adicionar os controles
        page.controls.clear()
        page.add(voltar_button, adicionar_button, historico_button, solicitacoes)
        page.update()

    # Função chamada ao clicar em "Pacientes"
    def button_clicked_pacientes(e):
        # Configurações iniciais da página
        page.title = 'Hospital Assist - Pacientes'
        page.scroll = ft.ScrollMode.AUTO  # Permitir rolagem para telas menores

        # Contêiner para "Chamados"
        chamados_container = ft.Column(visible=False, expand=True)

        # Dados dos pacientes (Exemplo)
        pacientes = [
            {"nome": "Paciente 1", "localizacao": "Sala 101", "status": "Aguardando transporte", "prioridade": "Alta"},
            {"nome": "Paciente 2", "localizacao": "Sala 202", "status": "Aguardando transporte", "prioridade": "Média"},
            {"nome": "Paciente 3", "localizacao": "Sala 303", "status": "Aguardando transporte", "prioridade": "Baixa"},
        ]

        # Dados de incidentes
        incidentes = []

        # Função para atualizar o status do paciente
        def atualizar_status(paciente, novo_status):
            paciente['status'] = novo_status
            page.update()

        # Função para registrar um incidente
        def registrar_incidente(paciente):
            def submit_incidente(e):
                descricao = incidente_input.value
                if descricao:
                    incidentes.append({"paciente": paciente["nome"], "descricao": descricao})
                    dialog.open = False
                    page.update()

            incidente_input = ft.TextField(label="Descreva o incidente", multiline=True, expand=True)
            submit_button = ft.ElevatedButton(text="Registrar", on_click=submit_incidente, expand=True)

            dialog = ft.AlertDialog(
                title=ft.Text(f"Registrar Incidente - {paciente['nome']}"),
                content=ft.Column([incidente_input, submit_button]),
                on_dismiss=lambda e: print("Dialog dismissed")
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        # Lista de pacientes para visualização e gestão de prioridades
        def criar_lista_pacientes():
            lista = ft.ListView(expand=True, spacing=10, padding=10)
            for paciente in pacientes:
                status_menu = ft.Dropdown(
                    value=paciente["status"],
                    options=[
                        ft.dropdown.Option("Aguardando transporte"),
                        ft.dropdown.Option("Em transporte"),
                        ft.dropdown.Option("Chegou ao destino"),
                    ],
                    on_change=lambda e, p=paciente: atualizar_status(p, e.control.value),
                    height=40,  # Ajuste de altura para mobile
                )
                prioridade_label = ft.Text(f"Prioridade: {paciente['prioridade']}", size=12, color='#555555')

                incidente_button = ft.IconButton(
                    icon=ft.icons.REPORT_PROBLEM,
                    tooltip="Registrar Incidente",
                    on_click=lambda e, p=paciente: registrar_incidente(p),
                    icon_size=20
                )
                item = ft.ResponsiveRow(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(f"{paciente['nome']} ({paciente['prioridade']} prioridade)", size=15,
                                        color='#333333'),
                                ft.Text(f"Localização: {paciente['localizacao']}", size=12, color='#555555'),
                                prioridade_label,
                            ],
                            col=8,
                            alignment=ft.MainAxisAlignment.START,
                            #wrap=True
                        ),
                        ft.Column(
                            controls=[status_menu],
                            col=3,
                            alignment=ft.MainAxisAlignment.CENTER,
                            #wrap=True
                        ),
                        ft.Column(
                            controls=[incidente_button],
                            col=1,
                            alignment=ft.MainAxisAlignment.CENTER,
                            #wrap=True
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=5,
                    #wrap=True
                )
                lista.controls.append(item)
            return lista

        # Botão Voltar
        voltar_button = ft.ElevatedButton(
            text="Voltar",
            bgcolor='#E0E0E0',
            color='#333333',
            on_click=voltar_para_menu_principal
        )

        # Limpa o conteúdo da página antes de adicionar os controles
        page.controls.clear()
        page.add(voltar_button, criar_lista_pacientes())
        page.update()

    # Título da aplicação
    nome = ft.Row(
        controls=[
            ft.Text('HOSPITAL ASSIST', size=35, color='#333333')

        ],
        alignment=ft.MainAxisAlignment.CENTER,

    )

    # Menu principal responsivo
    menu = ft.Row(
        controls=[
            ft.ElevatedButton(
                text='Chamados',
                tooltip='Solicitações',
                bgcolor='#E0E0E0',
                color='#333333',
                on_click=button_clicked_chamados,
            ),
            ft.ElevatedButton(
                text='Pacientes',
                bgcolor='#E0E0E0',
                color='#333333',
                on_click=button_clicked_pacientes
            ),
            ft.ElevatedButton(
                icon=ft.icons.HELP,
                bgcolor='#E0E0E0',
                color='#333333',
                tooltip='Sobre',
                text='.'
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        wrap=True
    )

    # Adicionando os elementos à página
    page.add(nome, menu)

ft.app(target=main, view=WEB_BROWSER)


