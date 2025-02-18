import socket

# Criar um socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir o endereço do servidor
host = '127.0.0.1'
port = 6840

# Conectar ao servidor
client_socket.connect((host, port))

print(f"{client_socket.recv(1024).decode()}")
while True:

    # Enviar mensagem ao servidor
    message = input('Qual sua mensagem: ')
    client_socket.send(message.encode())

    # Receber resposta do servidor
    servidor = client_socket.recv(1024).decode()
    if servidor == "desc":
        break
    print(f"{servidor}")

