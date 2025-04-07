from armazenamento import Banco

class Loguin:
    def __init__(self):
        self.banco = Banco('usuarios.csv', cabecalho= ['nome', 'senha', 'tipo'])
    
    def buscar_users(self):
        users = self.banco.ler()
        print(users)
        usuarios = {}
        for linha in users[1:]:
            usuarios[linha[0]] = {users[0][1]: linha[1], users[0][2]: linha[0][2]}
        return usuarios

    def start(self):
        users = self.buscar_users()
        print(users)

if __name__ == '__main__':
    L = Loguin()
    L.start()
