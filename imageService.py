import os
import time
import base64
from datetime import datetime
from watchdog.events import FileSystemEventHandler
from requestApi import requestApi
import logging

# Configurar o logger
logging.basicConfig(
    filename='meu_log.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

class ImageService(FileSystemEventHandler):
    def __init__(self, id_cam, enviados_path):
        self.id_cam = id_cam
        self.enviados_path = enviados_path

    def leituraDiretorioEnvioManual(self,path):
        return os.listdir(path)

    def realizarEnviosManuais(self, event, path, listaImagens):
        logging.info(f"Iniciando o envio manual de " + len(listaImagens))
        for imagemPath in listaImagens:
            event.src_path = path + "/" +  imagemPath #quando usado em WINDOWS utilizar contra barra dupla
            self.enviar(event)
            print("enviomanual-----------------")
        return True

    def enviar(self, event):
        init_size = -1
        while True: 
            current_size = os.path.getsize(event.src_path)
            if current_size == init_size:
                break
            else:
                init_size = os.path.getsize(event.src_path)
                time.sleep(1)

        body = self.process_image(event.src_path, self.id_cam)
        if body:
            request = requestApi(event, body)
            request.enviarImagem(self.enviados_path)
        else:
            return None

    def process_image(self, image_path, id_cam):
        filename = os.path.basename(image_path)
        parts = filename.split('_')
        if len(parts) != 4:
            print(f"Filename {filename} does not match expected format.")
            return None

        date_str, time_str, plate, id_register = parts
        if plate == "000000" or plate =='_No Plate':
            print(f"Plate is invalid, deleting image {image_path}.")
            os.remove(image_path)
            return None

        try:
            capture_datetime = datetime.strptime(date_str + time_str, '%Y%m%d%H%M%S').strftime('%Y-%m-%dT%H:%M:%S')
            if not os.path.isfile(image_path):
                print(f"Image file {image_path} does not exist.")
                return None

            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                if not image_data:
                    print(f"Failed to read image data from {image_path}.")
                    return None
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                print(f"Image {image_path} successfully converted to base64.")
        except Exception as e:
            logging.error(f"Failed to read or convert image {image_path} to base64: {e}")
            print(f"Failed to read or convert image {image_path} to base64: {e}")
            return None

        body = {
            "idRegister": id_register.split('.')[0],
            "captureDateTime": capture_datetime,
            "plate": plate,
            "idCam": id_cam,
            "latitude": "",
            "longitude": "",
            "image": image_base64
        }
        return body