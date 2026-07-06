class DownloadQueue:
    
    def __init__(self):
        self._queue: list[dict[str, str]] = []
        self._queue_information: dict[str, int | float] = {
            "number_of_download_errors" : 0,
            "current_downloaded_quantity" : 0,
            "total_downloads" : 0,
            "current_percentage_downloaded" : 0.0
        }
        self._current_index: int = 0
        self._is_running: bool = False
    

    # Utilidades de métodos internos da classe
    def set_is_running(self, value: bool):
        self._is_running = value
    
    def return_queue_information(self):
        return self._queue_information
    
    def return_is_running(self):
        return self._is_running

    def add(self, urls: list[str]):
        for url in urls:
            if url not in self._queue:
                self._queue.append({
                    "url" : url,
                    "status" : "🔸 aguardando..."
                })
        
        self._queue_information["total_downloads"] = len(self._queue)

    def remove(self, url: str):
        index_dict_to_remove: int = None

        for index, dic in enumerate(self._queue):
            if dic["url"] == url:
                index_dict_to_remove = index
                break

        del self._queue[index_dict_to_remove]
        self._queue_information["total_downloads"] = len(self._queue)

    def clear_queue(self):
        self._queue.clear()


    # Comandos e controle do download
    def start(self):
        from .controller_download import ControllerDownload
        from .download import download

        if len(self._queue) == 0:
            ControllerDownload.notify_callback(
                event = "snack_bar_information",
                data = "Lista de downloads vazia"
            )
            return
        
        if download._path is None or not isinstance(download._path, str):
            ControllerDownload.notify_callback(
                event = "snack_bar_information",
                data = "Selecione uma pasta"
            )
            return
        
        if self._is_running == False:
            ControllerDownload.notify_callback(
                event = "snack_bar_information",
                data = "Houve um problema ao iniciar os downloads, tente novamente!"
            )
            return

        ControllerDownload.notify_callback(
            event = "snack_bar_information",
            data = "Iniciando downloads..."
        )

        # notificar alteração de estado do botão
        ControllerDownload.notify_callback(
            event = "state_button",
            data = None
        )
        while self._is_running:
            
            status = download.download(
                url = self._queue[self._current_index]["url"]
            )

            if status == False:
                self._queue[self._current_index]["status"] = "🔺 erro..."
                self._queue_information["number_of_download_errors"] += 1

                ControllerDownload.notify_callback(
                    event = "downloaded_text",
                    data = self.return_queue_information()
                )
                ControllerDownload.notify_callback(
                    event = "update_container_download",
                    data = self._queue[self._current_index]
                )
            else:
                self._queue[self._current_index]["status"] = "🔹 download concluído!"

                self._queue_information["current_downloaded_quantity"] += 1
                self._queue_information["current_percentage_downloaded"] = int(
                    (self._queue_information["current_downloaded_quantity"] / self._queue_information["total_downloads"]) * 100
                )

                ControllerDownload.notify_callback(
                    event = "downloaded_text",
                    data = self.return_queue_information()
                )
                ControllerDownload.notify_callback(
                    event = "update_container_download",
                    data = self._queue[self._current_index]
                )
                ControllerDownload.notify_callback(
                    event = "update_progress_bar",
                    data = self._queue_information["current_percentage_downloaded"] / 100
                )
            
            self.next()

    def stop(self):
        from .controller_download import ControllerDownload
        
        self.set_is_running(False)
        
        ControllerDownload.notify_callback(
            event = "snack_bar_information",
            data = "Lista de downloads terminou!"
        )
    
    def next(self):
        from .controller_download import ControllerDownload

        if len(self._queue) == 0:
            return
        
        if self._current_index >= len(self._queue) - 1:
            if self._queue_information["number_of_download_errors"] != 0:
                index_errors: list[dict[str, str]] = []
                
                for url in self._queue:
                    if url["status"] == "🔺 erro...":
                        index_errors.append(url)

                self._queue.clear()
                self._queue.extend(index_errors)

                self._current_index = 0
                self._queue_information["number_of_download_errors"] = 0
                return
            
            self.stop()

            self._current_index = 0
            self._queue_information = {
                "number_of_download_errors" : 0,
                "current_downloaded_quantity" : 0,
                "total_downloads" : 0,
                "current_percentage_downloaded" : 0.0
            }

            ControllerDownload.clear_downloads()
            ControllerDownload.notify_callback(
                event = "downloaded_text",
                data = self.return_queue_information()
            )
            ControllerDownload.notify_callback(
                event = "update_progress_bar",
                data = self._queue_information["current_percentage_downloaded"] / 100
            )
        else:
            self._current_index += 1
        
    def current_download(self):
        ...


download_queue = DownloadQueue()