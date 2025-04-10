
def start(host='127.0.0.1', port=5000):
    import socket

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))

    servidor.listen(1)
    print("Aguardando conexão...")

    conn, addr = servidor.accept()
    print(f"Conectado por {addr}")

    while True:
        dados = conn.recv(1024)
        if not dados:
            break
        dados = dados.decode()
        print('dados', dados)

        if dados == '123': resposta = '123'
        else: resposta = f'Resposta do servidor: {dados}'
        conn.sendall(resposta.encode())

    conn.close()
    print('Conexão finalizada')

if __name__ == '__main__': start()
