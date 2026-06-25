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
        print(url_download + ' foi selecionada')
        

    def resultado(e : ft.FilePickerResultEvent):
        nonlocal pasta_destino
        pasta_destino = e.path
        
        texto_diretorio_selecionado.value = pasta_destino
        texto_diretorio_selecionado.update()

        print(pasta_destino + ' foi selecionada')

        page.open(
            ft.SnackBar(
                content = ft.Text(
                    value = f'Pasta Selecionada: {str(pasta_destino)}'
                )
            )
        )


    def abrir_seletor(e):
        picker.get_directory_path()
    

    def baixar_musica(e):        
        try:
            resultado = baixar_via_ffmpeg(
                url = url_download,
                pasta_destino = pasta_destino
            )

            texto_diretorio_dawnload.value = resultado
            page.update()

            page.open(
                ft.SnackBar(
                    content = ft.Text(
                        value = f'Download concluído com sucesso'
                    )
                )
            )
        except Exception as e:
            page.open(
                ft.SnackBar(
                    content = ft.Text(
                        value = f'Falha no Download, tente novamente!'
                    )
                )
            )
        
        
    picker = ft.FilePicker(
        on_result = resultado
    )

    page.overlay.append(picker)

    input_link_video = ft.TextField(
        on_change = carregar_link
    )

    botao_selecionar_pasta = ft.TextButton(
        text = 'Selecionar Pasta',
        on_click = abrir_seletor
    )
    
    texto_diretorio_selecionado = ft.Text(
        value = 'Nenhum diretório selecionado'
    )
    
    botao_baixar_musica = ft.TextButton(
        text = 'Baixar Música',
        on_click = baixar_musica
    )

    texto_diretorio_dawnload = ft.Text(
        value = f'Assets/Download/...'
    )

    page.add(
        ft.SafeArea(
            content = ft.Column(
                controls = [
                    input_link_video,
                    texto_diretorio_selecionado,
                    botao_selecionar_pasta,
                    botao_baixar_musica,
                    texto_diretorio_dawnload
                ]
            )
        )
    )


ft.app(
    target = main,
    assets_dir = 'Assets'
)