from servidor import start
from armazenamento import Banco

class Loguin:
    def __init__(self):
        self.banco = Banco('conexao.csv', cabecalho= ['tipo', 'endereco', 'porta']) # tipo= servidor/cliente, 
    pass
    def buscar_acesso(self):
        """Procura pelos dados do acesso anterior.

        Returns:
            bool: Se não encontrar registros retorna False.
            list[list]: O conteúdo salvo do acesso anterior que pode ser usado para conctar novamente automaticamente.
        """
        if self.banco.contagem() == 0: return False
        return self.banco.ler()[1:]
    
    def buscar_users(self):
        pass
    
    def escolher_usuario(self):
        pass
    
    def salvar_acesso(self):
        pass

    def start(self):
        pass

if __name__ == '__main__':
    L = Loguin()
    L.start()
