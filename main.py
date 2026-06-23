from Assets.Code.download import baixar_via_ffmpeg
import flet as ft

def main(page : ft.Page):
    page.title = 'Baixa Música'

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.GREY_900
    
    pasta_destino : str | None = None
    url_download : str | None = None

    def carregar_link(e):
        nonlocal url_download
        url_download = e.control.value
        

    def resultado(e : ft.FilePickerResultEvent):
        nonlocal pasta_destino
        pasta_destino = e.path


    def abrir_seletor(e):
        picker.get_directory_path()

    
    def baixar_musica(e):
        baixar_via_ffmpeg()
    

    picker = ft.FilePicker(
        on_result = resultado
    )

    page.overlay.append(picker)

    input_link_video = ft.TextField(
        on_submit = carregar_link
    )

    botao_selecionar_pasta = ft.TextButton(
        text = 'Selecionar Pasta',
        on_click = abrir_seletor
    )
    
    texto_diretório_selecionado = ft.Text(
        value = 'Nenhum diretório selecionado'
    )
    
    texto_diretório_dawnload = ft.Text(
        value = r'Assets\Download\...'
    )
    
    botao_baixar_musica = ft.TextButton(
        text = 'Baixar Música',
        on_click = baixar_musica
    )

    page.add(
        ft.SafeArea(
            content = ft.Column(
                controls = [
                    input_link_video,
                    texto_diretório_selecionado,
                    botao_selecionar_pasta,
                    botao_baixar_musica,
                    texto_diretório_dawnload
                ]
            )
        )
    )


ft.app(
    target = main,
    assets_dir = 'Assets'
)