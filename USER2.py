import socket
import threading
# Criar um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir o endereço do servidor
host = '127.0.0.1'
port = 6840

nameUser = 'Cleberson'
# Conectar ao servidor
client_socket.connect((host, port))

client_socket.send(nameUser.encode())
print(client_socket.recv(1024).decode())

def envia():
    while True:
        message = input(' ')
        client_socket.send(message.encode())

def recebe():
    while True:
        servidor = client_socket.recv(1024).decode()
        print(f"{servidor}")

    
env = threading.Thread(target=envia)
rec = threading.Thread(target=recebe)

env.start()
rec.start()
