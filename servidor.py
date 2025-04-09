from main import start
from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = {
    'user1': {'senha': '123'}
}

@app.route('/', methods=['GET'])
def index(): return 'Esta página não pode ser acessada por navegador, entre em contato com o desenvolvedor para mais informações!'

@app.route('/usuario', methods=['POST'])
def usuario():
    if request.is_json:
        dados = request.get_json()
        user_nane = dados.get('user_name')
        senha = dados.get('senha')
        print(dados, user_nane, senha, sep='\n')

        if user_nane in list(usuarios.keys()):
            if senha == usuarios[user_nane]['senha']:
                print('acessado com sucesso')
                return jsonify({'mensagem': 'Acesso concedido com sucesso!'}), 200
            else:
                return jsonify({'erro': 'A senha informada está incorreta!'}), 401
        else: return jsonify({'erro': 'O usuario não está cadastrado!'}), 404
    else:
        return jsonify({'erro': 'Requisição precisa estar no formato JSON!'}), 400

def iniciar(): app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__': app.run(debug=True, host='0.0.0.0', port=5000)
