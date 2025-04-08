import requests

url = 'http://127.0.0.1:5000/user-1'
dados = {
    'senha': '12345678'  # experimente mudar para testar
}

resposta = requests.post(url, json=dados)

print('Status:', resposta.status_code)
print('Resposta:', resposta.json())
