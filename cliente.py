import requests

url = 'http://127.0.0.1:5000/usuario'
dados = {
    'user_name': 'user1',
    'senha': '123'  # experimente mudar para testar
}

resposta = requests.post(url, json=dados)

print('Status:', resposta.status_code)
print('Resposta:', resposta.json())
