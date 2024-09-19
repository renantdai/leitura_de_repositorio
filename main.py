import os
import time
from watchdog.observers import Observer
from conexao import BancoDeDados
from imageHandler import ImageHandler
import json

with open('parametros.json', 'r') as config_file:
    parametros = json.load(config_file)

def inicializaBancoDeDados():
    return BancoDeDados()

def obterDiretorios(db):
    query = "SELECT id, cameras_id, diretorio FROM diretorios WHERE situacao_registro_id = 1"
    return db.realizar_consulta(query)

def verificaDiretorio(path):
    if not os.path.exists(path):
        print(f"Directory {path} does not exist.")
        return False

    enviados_path = os.path.join(path, 'enviados')
    if not os.path.exists(enviados_path):
        os.makedirs(enviados_path)
    return True

def leituraDiretorioEnvioManual(imageHandler, path):
    return imageHandler.leituraDiretorioEnvioManual(path)

def realizarEnviosManuais(imageHandler, path, listaImagens):
    return imageHandler.realizarEnviosManuais(path, listaImagens)

def main():
    if parametros['banco_de_dados']:
        db = inicializaBancoDeDados()    
        directories = obterDiretorios(db)
        db.close()
    else:
        directories = parametros['diretorios']

    observers = []
    for directory in directories:
        dir_id, id_cam, path = directory

        if not verificaDiretorio(path):
            continue

        event_handler = ImageHandler(id_cam, os.path.join(path, 'enviados'))
        listaImagens = leituraDiretorioEnvioManual(event_handler, path)

        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()
        observers.append(observer)

        realizarEnviosManuais(event_handler, path, listaImagens)

    if len(observers) == 0:
        print("A lista está vazia")
        exit()

    try:
        while True:
            time.sleep(1)
            pass
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
    for observer in observers:
        observer.join()



if __name__ == "__main__":
    main()