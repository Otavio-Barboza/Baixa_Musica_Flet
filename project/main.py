from assets.core.controller_download import ControllerDownload
from assets.core.download import download
import os, sys
import flet as ft

# forçando o sistema operacional usar do encoding utf-8, para suprir a necessidade de visibilidade de emojis ou outros caracteres especiais.
os.environ["PYTHONUTF8"] = "1"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def main(page: ft.Page):

    # Comandos e configurações gerais da page.
    page.title = "Baixa Música"
        
    page.window.min_width = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {
        "google_sans_flex" : r"font\GoogleSansFlex.ttf"
    }
    page.theme = ft.Theme(
        font_family = "google_sans_flex"
    )
    page.bgcolor = "#121219"


    # Event Handlers (Manipuladores de Eventos) - funções que correspondem a um evento.
    def handle_url_submit(event):
        """
        _summary_: Função capta o conteúdo submetido pelo TextField, adicionando-o ao _cache_downloads e adicionando o/os container(s) de download;

        Args:
            event (evento on_submit): Realização a sbmissão do conteúdo.
        """

        url_download: list[str] = str(event.control.value).splitlines()
        ControllerDownload.add_url_to_download(url_download)
        
        input_link_video.value = ""
        input_link_video.update()
        
    def remove_container(event):
        """
        _summary_: Função criada para a remoção do container desejado. Por conta do evento estar no IconButton, foi associado o "data" do container ao button também, assim com o loop for é possível obter o container de referência clicado e removê-lo.  

        Args:
            event (evento do on_click): Click no IconButton do container.
        """
  
        container_to_remove: ft.Container | None = None

        for container in downloads_list_view.controls:
            if container.data == event.control.data:
                container_to_remove = container
                break
        
        if container_to_remove is not None:
            ControllerDownload.remove_url_to_download(event.control.data)

            downloads_list_view.controls.remove(container_to_remove)
            downloads_list_view.update()

    # Seleção de pasta
    def on_directory_selected(e: ft.FilePickerResultEvent):
        """
        _summary_: Função para abrir o seletor nativo do flet, com auxilio da função open_selector(e) capturando o diretório destinado pelo usuário e atualizando a variável destination_path para atribuição do download na pasta atribuída pelo usuário; 

        Args:
            e (ft.FilePickerResultEvent): Evento da captura da pasta selecionada.
        """

        if e.path is None:
            ControllerDownload.notify_callback(
                event = "information_download",
                data = "Selecione uma pasta válida"
            )
            return

        download.set_path(e.path)
        
        selected_directory_text.value = f"Pasta selecionada: {e.path}"
        selected_directory_text.update()

        ControllerDownload.notify_callback(
            event = "snack_bar_information",
            data = f"Pasta Selecionada: {e.path}"
        )

    def open_selector(e):
        picker.get_directory_path()
    
    picker = ft.FilePicker(
        on_result = on_directory_selected
    )

    # Monitoramento de redimensionamento
    def handle_resize(event):
        # Função para monitoramento do redimensionamento (width) na atualização do posicionamento do texto informátivo de download e tamanho ocupado pelos containeres do ListView.

        align: ft.TextAlign = directory_download_text.text_align
        
        if page.width <= 575 and align != ft.TextAlign.LEFT:
            # atualizando TextAlifgn do texto informativo de download
            directory_download_text.text_align = ft.TextAlign.LEFT
            directory_download_text.update()

            # atualizando o tamanho do espaço ocupado pela url em cada container da ListView
            if len(downloads_list_view.controls) != 0:
                for container in downloads_list_view.controls:
                    container.content.controls[1].width = 380
                    container.update()
        elif page.width > 575 and align != ft.TextAlign.RIGHT:
            # atualizando TextAlifgn do texto informativo de download
            directory_download_text.text_align = ft.TextAlign.RIGHT 
            directory_download_text.update()

            # atualizando o tamanho do espaço ocupado pela url em cada container da ListView
            if len(downloads_list_view.controls) != 0:
                for container in downloads_list_view.controls:
                    container.content.controls[1].width = 460
                    container.update()
        else:
            return
        

    # Helper Functions (Funções Auxiliares) - são funções auxiliares que ajudam outras funções, mas não responde diretamente a eventos.
    def _create_text_button(
        text: str, 
        icon: ft.Icons,
        on_click: callable,
        color: str,
        secundary_color: str,
        icon_size: int = 16
    ) -> ft.TextButton:
        return ft.TextButton(
            width = 400,
            height = 40,
            col = {"xs": 12, "sm": 6},
            text = text,
            icon = icon,

            on_click = on_click,

            style = ft.ButtonStyle(
                bgcolor = {
                    ft.ControlState.DEFAULT: color,
                    ft.ControlState.HOVERED: secundary_color
                },
                text_style = ft.TextStyle(
                    size = 16,
                    weight = ft.FontWeight.W_500,
                    font_family = "google_sans_flex"
                ),
                shape = ft.RoundedRectangleBorder(
                    radius = 15
                ),
                icon_size = icon_size,
                icon_color = "#ededf1",
                color = "#ededf1"
            )
        )
    
    def _create_download_container(url: str) -> ft.Container:
        return ft.Container(
            height = 60,
            bgcolor = "#1e1b2e",
            border_radius = ft.border_radius.only(
                top_right = 15,
                bottom_right = 15
            ),

            data = url,

            content = ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Container(
                        height = 60,
                        width = 5.5,
                        border_radius = ft.border_radius.only(
                            top_left = 15,
                            bottom_left = 15
                        ),
                        bgcolor = "#ff8c00",
                    ),

                    ft.Column(
                        width = 460,    
                        spacing = 2.5,
                        alignment = ft.MainAxisAlignment.CENTER,

                        controls = [
                            ft.Text(
                                value = ControllerDownload.return_title_video(url),
                                size = 16,
                                color = "#ededf1",
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                font_family = "google_sans_flex"
                            ),
                            ft.Text(
                                value = "🔸 Aguardando download...",
                                size = 13,
                                color = "#ededf1",
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                weight = ft.FontWeight.W_300,
                                font_family = "google_sans_flex"
                            ),
                        ]
                    ),

                    ft.Container(expand = True),

                    ft.IconButton(
                        icon = ft.Icons.CLOSE,

                        style = ft.ButtonStyle(
                            color = {
                                ft.ControlState.DEFAULT: "#ff8c00",
                                ft.ControlState.HOVERED: "#ededf1"
                            },
                            overlay_color = ft.Colors.TRANSPARENT
                        ),

                        data = url,

                        on_click = remove_container
                    )
                ]
            )
        )
                
    def _add_download_container(urls: list[str]):
        # Função para adicionar um novo container de download conforme as url(s) que o usuário submeter.

        _existing_urls: list[str] = []

        for container in downloads_list_view.controls:
            _existing_urls.append(container.data)

        for url in urls:
            downloads_list_view.controls.append(
                _create_download_container(url)
            )
            downloads_list_view.update()


    # Funções de download e atualização de status
    def download_music(event):
        ControllerDownload.start_downloads_queue()

    def _update_containers_downloads(data: str):
        print(data)
        if len(downloads_list_view.controls) != 0:
            for container in downloads_list_view.controls:
                if data["url"] == container.data:
                    container.content.controls[1].controls[1].value = data["status"]
                    container.update()

    def clear_containers(*_):
        downloads_list_view.controls.clear()
        downloads_list_view.update()

    def _update_title_download(text: str):
        title_download.value = text
        title_download.update()

    def _update_information_downloads(data: dict[str, int | float]):
        error_text.value = f"erro(s): {data.get('number_of_download_errors') or 0}"
        
        downloaded_text.value = f"""baixados: {
            data.get('current_downloaded_quantity') or 0
        }/{
            data.get('total_downloads') or 0
        }  |  {
            data.get('current_percentage_downloaded') or 0.0
        }%"""
        
        error_text.update()
        downloaded_text.update()
    
    def update_progress_bar(value: int):
        if value is None:
            return
        
        progress_bar.value = value
        progress_bar.update()

    def update_directory_download_save(path: str):
        print('chamando callback')
        directory_download_text.value = path
        directory_download_text.update()

    def snack_bar(text: str):
        """
        _summary_: Função para operar de modo informativo, para erros, sucessos etc.

        Args:
            text (str): texto informativo qualquer.
        """

        page.open(
            ft.SnackBar(
                content = ft.Text(
                    value = text
                )
            )
        )

    # Overlay e resize
    page.overlay.append(picker)
    page.on_resized = handle_resize


    # callbacks
    ControllerDownload.register_callback(
        event = "snack_bar_information",
        callback = snack_bar
    )
    ControllerDownload.register_callback(
        event = "add_download",
        callback = _add_download_container
    )
    ControllerDownload.register_callback(
        event = "downloaded_text",
        callback = _update_information_downloads
    )
    ControllerDownload.register_callback(
        event = "title_download",
        callback = _update_title_download
    )
    ControllerDownload.register_callback(
        event = "update_container_download",
        callback = _update_containers_downloads
    )
    ControllerDownload.register_callback(
        event = "update_progress_bar",
        callback = update_progress_bar
    )
    ControllerDownload.register_callback(
        event = "clear_containers",
        callback = clear_containers
    )
    ControllerDownload.register_callback(
        event = "path_download_saved",
        callback = update_directory_download_save
    )

    page.add(
        ft.SafeArea(
            width = 860,

            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,
                spacing = 15,

                controls = [
                    # Listagem dos downloads em fila
                    title_download := ft.Text(
                        value = "Nenhum link atribuído para download...",
                        size = 24,
                        color = "#ededf1",
                        weight = ft.FontWeight.BOLD
                    ),
                    
                    ft.Column(
                        controls = [
                            progress_bar := ft.ProgressBar(
                                value = 0,
                                border_radius = ft.border_radius.all(20),
                                color = "#ffa94d"
                            ),

                            ft.Row(
                                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                alignment = ft.MainAxisAlignment.SPACE_BETWEEN,

                                controls = [
                                    ft.Text(
                                        value = "Status Downloads...",
                                        weight = ft.FontWeight.BOLD,
                                        size = 13
                                    ),
                                    error_text := ft.Text(
                                        value = "erro(s):",
                                        weight = ft.FontWeight.W_300,
                                        size = 13
                                    ),
                                    downloaded_text := ft.Text(
                                        value = "baixados: 0/0  |  0%",
                                        weight = ft.FontWeight.W_300,
                                        size = 13
                                    )
                                ]
                            )
                        ]
                    ),

                    downloads_list_view := ft.ListView(
                        height = 500,
                        spacing = 7.5,

                        controls = []
                    ),

                    ft.Divider(
                        color = "#2d2a3d",
                        opacity = 0.75,
                        height = 1.5
                    ),

                    input_link_video := ft.TextField(
                        height = 110,
                        min_lines = 3,
                        max_lines = 50,
                        border_color = "#6c3aed",
                        border_width = 1.5,
                        border_radius = ft.border_radius.all(15),
                        shift_enter = True,
                        label = "Digite ou cole a URL do Vídeo...",
                        align_label_with_hint = True,
                        on_submit = handle_url_submit
                    ),
                    
                    ft.ResponsiveRow(
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls = [
                            selected_path_button := _create_text_button(
                                text = "Selecionar Pasta",
                                icon = ft.Icons.FOLDER_COPY_ROUNDED,
                                on_click = open_selector,
                                color = "#6c3aed",
                                secundary_color = "#8b5cf6"
                            ),
                            download_music_button := _create_text_button(
                                text = "Baixar Música",
                                icon = ft.Icons.FILE_DOWNLOAD_OUTLINED,
                                on_click = download_music,
                                color = "#ff8c00",
                                secundary_color = "#ffa94d",
                                icon_size = 20
                            )
                        ]
                    ),
                    
                    ft.ResponsiveRow(
                        width = 860,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                        
                        controls = [
                            selected_directory_text := ft.Text(
                                value = "Nenhum diretório selecionado",
                                color = "#ededf1",
                                col = {"xs" : 12, "sm" : 6},
                                text_align = ft.TextAlign.LEFT
                            ),
                            directory_download_text := ft.Text(
                                value = f"Assets/Download/...",
                                color = "#ededf1",
                                col = {"xs" : 12, "sm" : 6},
                                text_align = ft.TextAlign.RIGHT
                            )
                        ]
                    )
                ]
            )
        )
    )


ft.app(
    target = main,
    assets_dir = "assets"
)