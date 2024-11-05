import os
import time
import schedule

class RemoveImageObserver:
    def __init__(self, diretorio_enviados, intervalo_horas):
        self.diretorio_enviados = diretorio_enviados
        self.intervalo_horas = intervalo_horas
        self.is_running = True  # Flag para controlar o ciclo de execução

        # Agendar a remoção de imagens
        schedule.every(self.intervalo_horas).minutes.do(self.remover_imagens_enviadas)

    def remover_imagens_enviadas(self):
        try:
            # Extensões de arquivos de imagem para serem removidos
            extensoes_imagem = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

            # Itera sobre os arquivos no diretório
            for filename in os.listdir(self.diretorio_enviados):
                file_path = os.path.join(self.diretorio_enviados, filename)

                # Verifica se é um arquivo de imagem
                if os.path.isfile(file_path) and file_path.lower().endswith(extensoes_imagem):
                    os.remove(file_path)  # Remove o arquivo
                    print(f"Imagem {filename} removida com sucesso.")

            print("Todas as imagens no diretório 'enviados' foram removidas.")
        
        except Exception as e:
            print(f"Ocorreu um erro ao remover as imagens: {e}")

    def iniciar_observer(self):
        print(f"Observer de remoção iniciado para o diretório {self.diretorio_enviados}.")
        
        try:
            while self.is_running:
                schedule.run_pending()  # Executa as tarefas agendadas quando chega o momento
                time.sleep(1)  # Pausa para reduzir o uso da CPU
        except KeyboardInterrupt:
            self.parar_observer()  # Para o observer caso o loop seja interrompido

    def parar_observer(self):
        self.is_running = False
        print("Observer de remoção parado.")
