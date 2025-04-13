import os
import subprocess
from armazenamento import Banco

class Sincronizar:
    def __init__(self):
        pass
    
    def __limpar_tela__(self):
        """
        Limpa a tela do terminal para melhorar a visualização do menu.

        O comando utilizado para limpar a tela é:
            - 'cls' para sistemas Windows.
            - 'clear' para sistemas Unix-based (Linux, macOS).
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def atualizar(self):
        repo_dir = os.path.dirname(os.path.abspath(__file__))

        subprocess.run(["git", "pull"], check=True, cwd=repo_dir)

    def start(self):
        mensagem = 'Erro: sem conexão com o servidor git '

        return mensagem

if __name__ == '__main__': pass
