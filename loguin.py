import os
from armazenamento import Banco

class Loguin:
    def __init__(self):
        self.banco = Banco('usuario.csv', cabecalho= ['nome', 'senha', 'tipo'])
    
    def buscar_users(self):
        admin = 'admin'
        user = 'user'
        usuarios = {
            admin: {'senha': admin, 'tipo': admin},
            user: {'senha': user, 'tipo': user}
        }
        return usuarios
    
    def escolher_usuario(self, usuarios: dict):
        os.system('clear')
        print('\tFaça o seu loguin')
        w = 0
        while w < 3:
            w += 1
            usuario = input('Nome: ').strip()
            if usuario in list(usuarios.keys()):
                senha = input('Senha: ').strip()
                if senha == usuarios[usuario]['senha']:
                    return {'usuario': usuario, 'tipo': usuarios[usuario]['tipo']}
                else:
                    w = 0
                    print('Senha incorreta!')
            else: print('Usuário não cadastrado!!')
    
    def salvar_acesso(self):
        self.banco.escrever()

    def start(self):
        usuario = self.escolher_usuario(self.buscar_users())
        print(usuario)

if __name__ == '__main__':
    L = Loguin()
    L.start()
