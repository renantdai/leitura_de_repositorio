import requests
import json
import os
import logging

# Configurar o logger
logging.basicConfig(
    filename='meu_log.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

class requestApi():
    def __init__(self, event, body):
        self.event = event
        self.body = body

    def enviarImagem(self, enviados_path):
        try:
            print(f"Sending request for image {self.event.src_path}")
            response = requests.post(config['url'], json=self.body)
            if response.status_code == 200:
                print(f"Image {self.event.src_path} sent successfully.")
                os.rename(self.event.src_path, os.path.join(enviados_path, os.path.basename(self.event.src_path)))
            else:
                os.rename(self.event.src_path, os.path.join(enviados_path, os.path.basename(self.event.src_path)))
                self.logRequest(response)
        except Exception as e:
            logging.error(f"erro  {e}")
            print(f"erro  {e}")

    def logRequest(self, response):
        logging.critical(f"Failed to send image {self.event.src_path}. Status code: {response.status_code}")
        print(f"Failed to send image {self.event.src_path}. Status code: {response.status_code}")
