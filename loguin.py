import os
from servidor import start
from armazenamento import Banco

class Loguin:
    def __init__(self):
        self.banco = Banco('conexao.csv', cabecalho= ['tipo', 'endereco', 'porta']) # tipo= servidor/cliente
    
    def __limpar_tela__(self):
        """
        Limpa a tela do terminal para melhorar a visualização do menu.

        O comando utilizado para limpar a tela é:
            - 'cls' para sistemas Windows.
            - 'clear' para sistemas Unix-based (Linux, macOS).
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def formulario(self):
        self.__limpar_tela__()
        print('\tConfiguração inicial')
        print('1 - Servidor')
        print('2 - Cliente')
        print('3 - Sair')
        execusoes = 0
        while execusoes < 4:
            execusoes += 1
            try:
                escolha = int(input('>>> ').strip())
                if escolha == 1:
                    ip_cliente = input('\n Digite o ip do cliente ').strip()
                    porta = int(input(' Digite a porta de coneção ').strip())
                    self.salvar_acesso(['servidor', ip_cliente, porta])
                    break
                else: raise ValueError
            except ValueError:
                print('Digite um número válido!')
                continue
    
    def salvar_acesso(self, dados):
        self.banco.escrever(dados, sobrescrever=True)
        return True

    def buscar_acesso(self):
        """Procura pelos dados do acesso anterior.

        Returns:
            bool: Se não encontrar registros retorna False.
            list[list]: O conteúdo salvo do acesso anterior que pode ser usado para conctar novamente automaticamente.
        """
        if self.banco.contagem() == 0: return False
        return self.banco.ler()[1:]

    def start(self):
        self.formulario()

if __name__ == '__main__':
    L = Loguin()
    L.start()
