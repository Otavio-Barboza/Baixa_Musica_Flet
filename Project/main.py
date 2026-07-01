from assets.core.cache_download import CacheDownload
from assets.core.download import baixar_via_ffmpeg
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
    page.title = 'Baixa Música'
        
    page.window.min_width = 500
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121219"


    # Variáveis auxiliares do app
    destination_path: str | None = None


    # Event Handlers (Manipuladores de Eventos) - funções que correspondem a um evento.
    def handle_url_submit(event):
        url_download = event.control.value

        CacheDownload.add_download(url_download)
        add_download_container(url_download)

    # Seleção de pasta
    def on_directory_selected(e: ft.FilePickerResultEvent):
        destination_path = e.path
        
        selected_directory_text.value = destination_path
        selected_directory_text.update()

        print(destination_path + ' foi selecionada')

        page.open(
            ft.SnackBar(
                content = ft.Text(
                    value = f'Pasta Selecionada: {str(destination_path)}'
                )
            )
        )

    def open_selector(e):
        picker.get_directory_path()
    
    picker = ft.FilePicker(
        on_result = on_directory_selected
    )

    # Monitoramento de redimensionamento
    def handle_resize(event):
        width = page.width
        align = directory_download_text.text_align
        
        if page.width <= 575 and align != ft.TextAlign.LEFT:
            directory_download_text.text_align = ft.TextAlign.LEFT
            directory_download_text.update()
        elif page.width > 575 and align != ft.TextAlign.RIGHT:
            directory_download_text.text_align = ft.TextAlign.RIGHT 
            directory_download_text.update()
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
            col = {'xs': 12, 'sm': 6},
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
                    weight = ft.FontWeight.W_500
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
            height = 50,
            bgcolor = "#1e1b2e",
            border_radius = ft.border_radius.only(
                top_right = 15,
                bottom_right = 15
            ),

            content = ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Container(
                        height = 50,
                        width = 5.5,
                        border_radius = ft.border_radius.only(
                            top_left = 15,
                            bottom_left = 15
                        ),
                        bgcolor = "#ff8c00",
                    ),

                    ft.Text(
                        value = url,
                        size = 16,
                        color = "#ededf1",
                        max_lines = 2,
                        overflow = ft.TextOverflow.ELLIPSIS
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
                    )
                ]
            )
        )
        
    def add_download_container(url: str):
        downloads_list_view.controls.append(
            _create_download_container(url = url)
        )
        downloads_list_view.update()

    def download_music(event):
        ...


    # Overlay e resize
    page.overlay.append(picker)
    page.on_resized = handle_resize

    page.add(
        ft.SafeArea(
            width = 860,

            content = ft.Column(
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                alignment = ft.MainAxisAlignment.CENTER,
                spacing = 15,

                controls = [
                    # Listagem dos downloads em fila
                    information_downloads := ft.Text(
                        value = 'Nenhum link atribuído para download...',
                        size = 24,
                        color = "#ededf1"
                    ),
                    
                    downloads_list_view := ft.ListView(
                        height = 600,
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
                        label = 'Digite ou cole a URL do Vídeo...',
                        align_label_with_hint = True,
                        on_submit = handle_url_submit
                    ),
                    
                    ft.ResponsiveRow(
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls = [
                            selected_path_button := _create_text_button(
                                text = 'Selecionar Pasta',
                                icon = ft.Icons.FOLDER_COPY_ROUNDED,
                                on_click = open_selector,
                                color = "#6c3aed",
                                secundary_color = "#8b5cf6"
                            ),
                            download_music_button := _create_text_button(
                                text = 'Baixar Música',
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
                                value = 'Nenhum diretório selecionado',
                                color = "#ededf1",
                                col = {'xs' : 12, 'sm' : 6},
                                text_align = ft.TextAlign.LEFT
                            ),
                            directory_download_text := ft.Text(
                                value = f'Assets/Download/...',
                                color = "#ededf1",
                                col = {'xs' : 12, 'sm' : 6},
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
    assets_dir = 'assets'
)