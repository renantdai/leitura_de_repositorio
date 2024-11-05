import os
import time
from watchdog.observers import Observer
from conexao import BancoDeDados
from imageHandler import ImageHandler
from removeImageObserver import RemoveImageObserver
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

    tmp_path = os.path.join(path, 'tmp')
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
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
    remove_image_observers = []

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

        # Cria e inicia um novo observer para remover imagens
        remove_observer = RemoveImageObserver(os.path.join(path, 'enviados'), 1)
        remove_observer.iniciar_observer()
        remove_image_observers.append(remove_observer)

    if len(observers) == 0:
        print("A lista está vazia")
        exit()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        for remove_observer in remove_image_observers:
            remove_observer.observer.stop()  # Parar cada observer de remoção de imagem
    for observer in observers:
        observer.join()
    for remove_observer in remove_image_observers:
        remove_observer.observer.join()  # Juntar cada observer de remoção de imagem



if __name__ == "__main__":
    main()