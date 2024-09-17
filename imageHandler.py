from watchdog.events import FileSystemEventHandler
from imageService import ImageService

class ImageHandler(FileSystemEventHandler):
    def __init__(self, id_cam, enviados_path):
        self.id_cam = id_cam
        self.enviados_path = enviados_path

    def on_created(self, event):
        print('------------------------------------------------')
        if event.is_directory:
            return
        if event.src_path.endswith(".jpg"):
            print(f"Processing image {event.src_path}")
            imageService = ImageService(self.id_cam, self.enviados_path)
            imageService.enviar(event) 
        print('------------------------------------------------')

    def leituraDiretorioEnvioManual(self, path):
        imageService = ImageService(self.id_cam, self.enviados_path)
        return imageService.leituraDiretorioEnvioManual(path) 

    def realizarEnviosManuais(self, path, listaImagens):
        if not listaImagens:
            return True

        listaImagens.remove('enviados')
        if not listaImagens:
            return True

        imageService = ImageService(self.id_cam, self.enviados_path)
        return imageService.realizarEnviosManuais(self, path, listaImagens) 
