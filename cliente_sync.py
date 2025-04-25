import os
import socket
import hashlib
import json

FOLDER = "dadosc"
SERVER_IP = '127.0.0.1'
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

def list_server_files(s):
    request = {"action": "LIST"}
    s.send(json.dumps(request).encode())
    data = s.recv(8192).decode()
    return json.loads(data)

def send_file(s, filename):
    filepath = os.path.join(FOLDER, filename)
    filesize = os.path.getsize(filepath)
    request = {"action": "PUT", "filename": filename, "filesize": filesize}
    s.send(json.dumps(request).encode())

    with open(filepath, 'rb') as f:
        s.sendfile(f)

def get_file(s, filename):
    request = {"action": "GET", "filename": filename}
    s.send(json.dumps(request).encode())

    filepath = os.path.join(FOLDER, filename)
    with open(filepath, 'wb') as f:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            f.write(chunk)

def sync():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))

        try:
            server_files = list_server_files(s)
            server_dict = {f['filename']: f for f in server_files}
            local_files = [file_info(f) for f in os.listdir(FOLDER)]
            local_dict = {f['filename']: f for f in local_files if f}

            # Sincronizar arquivos
            for filename in set(local_dict) | set(server_dict):
                local = local_dict.get(filename)
                remote = server_dict.get(filename)

                if not local:
                    print(f"[↓] Baixando novo arquivo do servidor: {filename}")
                    get_file(s, filename)
                elif not remote:
                    print(f"[↑] Enviando novo arquivo ao servidor: {filename}")
                    send_file(s, filename)
                else:
                    # Ambos têm o arquivo → comparar timestamp
                    if local['hash'] != remote['hash']:
                        if local['timestamp'] > remote['timestamp']:
                            print(f"[↑] Atualizando servidor com: {filename}")
                            send_file(s, filename)
                        elif remote['timestamp'] > local['timestamp']:
                            print(f"[↓] Atualizando cliente com: {filename}")
                            get_file(s, filename)
                        else:
                            print(f"[=] Conflito não resolvido em: {filename} (hash diferente, timestamp igual)")
                    else:
                        print(f"[✓] Arquivo sincronizado: {filename}")
            input("t ")

        finally: s.send(json.dumps({"action": "EXIT"}).encode())
                    
sync()
