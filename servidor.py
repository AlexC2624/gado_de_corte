from main import start
from flask import Flask, request, jsonify

app = Flask(__name__)

SENHA_CORRETA = '12345678'

@app.route('/', methods=['GET'])
def index(): return False, 'Esta página não pode ser acessada por navegador!!!'

@app.route('/user-1', methods=['POST'])
def user_1():
    if request.is_json:
        dados = request.get_json()
        senha = dados.get('senha')
        if senha == SENHA_CORRETA:
            pass
        else: return False, 'A senha informada esta incorreta!!!'
    else: return False, 'O nome de usuário não está cadastrado!!!'

def iniciar(): app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__': app.run(debug=True, host='0.0.0.0', port=5000)
