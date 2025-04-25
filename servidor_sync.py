import os
import socket
import threading
import json
import hashlib

FOLDER = "dados"
HOST = '0.0.0.0'
PORT = 5001

def file_info(filename):
    filepath = os.path.join(FOLDER, filename)
    if not os.path.isfile(filepath):
        return None
    with open(filepath, 'rb') as f:
        content = f.read()
        return {
            "filename": filename,
            "timestamp": os.path.getmtime(filepath),
            "hash": hashlib.md5(content).hexdigest()
        }

def handle_client(conn, addr):
    print(f"[{addr}] Novo cliente, esperando dados...")
    try:
        while True:
            data = conn.recv(4096).decode()
            print(f"[{addr}] ✅ Dados recebidos:", data)
            request = json.loads(data)

            if request['action'] == 'LIST':
                files = [file_info(f) for f in os.listdir(FOLDER)]
                files = [f for f in files if f]
                conn.send(json.dumps(files).encode())

            elif request['action'] == 'GET':
                filepath = os.path.join(FOLDER, request['filename'])
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as f:
                        conn.sendfile(f)

            elif request['action'] == 'PUT':
                filename = request['filename']
                filesize = request['filesize']
                filepath = os.path.join(FOLDER, filename)

                with open(filepath, 'wb') as f:
                    bytes_read = 0
                    while bytes_read < filesize:
                        chunk = conn.recv(min(4096, filesize - bytes_read))
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_read += len(chunk)
            elif request['action'] == 'EXIT': break

    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()
        print(f"[{addr}] Conexão finalizada")

def start_server():
    print(" Iniciando o servidor...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f" Aguardando conexões em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

start_server()
