import socket

HOST = '127.0.0.1'  # IP do servidor
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

loop = True
while loop:
    enviar = input('Digite a mensagem: ').strip()
    if enviar == '1': break
    if enviar == '': continue

    cliente.sendall(enviar.encode())

    resposta = cliente.recv(1024)
    resposta = resposta.decode()
    print(resposta)

cliente.close()
print('Conexão finalizada')
