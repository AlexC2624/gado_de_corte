import os
from armazenamento import Banco

class Loguin:
    def __init__(self):
        self.banco = Banco('usuario.csv', cabecalho= ['Nome', ])
    
    def buscar_acesso(self):
        pass
    
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
