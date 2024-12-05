import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class CleanupHandler(FileSystemEventHandler):
    """
    Handler para monitorar e limpar arquivos de um diretório a cada intervalo de tempo.
    """
    def __init__(self, directory, cleanup_interval=60):
        super().__init__()
        self.directory = directory
        self.cleanup_interval = cleanup_interval
        self.last_cleanup_time = time.time()
        self.lock = threading.Lock()

    def process_event(self, event):
        """
        Processa qualquer evento de modificação no diretório.
        """
        print(f"Evento detectado: {event.event_type} - {event.src_path}")
        self.verificar_e_limpar()

    def verificar_e_limpar(self):
        """
        Verifica o tempo e limpa o diretório, se necessário.
        """
        with self.lock:  # Garante que apenas um processo de limpeza acontece por vez.
            current_time = time.time()
            if current_time - self.last_cleanup_time >= self.cleanup_interval:
                self.limpar_diretorio()
                self.last_cleanup_time = current_time

    def limpar_diretorio(self):
        """
        Remove todos os arquivos do diretório monitorado.
        """
        print(f"Iniciando limpeza do diretório: {self.directory}")
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Removido: {file_path}")
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # Remove diretórios vazios
                    print(f"Diretório vazio removido: {file_path}")
            except Exception as e:
                print(f"Erro ao remover {file_path}: {e}")

    def on_any_event(self, event):
        """
        Método chamado para qualquer evento observado no diretório.
        """
        self.process_event(event)