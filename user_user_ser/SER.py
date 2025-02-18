import socket
import threading

# Configurações do servidor
host = "0.0.0.0"  # Aceita conexões de qualquer IP
port = 6840

# Criando o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)  # Permite até 5 conexões na fila

print(f"Servidor rodando em {host}:{port}")

# Lista para armazenar os clientes conectados
clientes = {}

# Função para lidar com cada cliente individualmente
def handle_client(client_socket, address):
    print(f"Nova conexão de {address}")

    while True:
        try:
            # Recebe dados do cliente
            message = client_socket.recv(1024).decode()
            if message.upper() == 'SAIR':
                client_socket.send('desc'.encode())
                break  # Se o cliente desconectar, sai do loop

           
            print(f"{clientes[address[1]]} diz: {message}")

            # Envia a mensagem de volta para o cliente
            client_socket.sendall(b"Mensagem recebida!")

        except ConnectionResetError:
            print(f"Cliente {clientes[address[1]]} desconectou inesperadamente.")
            break

    # Remove o cliente da lista ao desconectar
    del clientes[address[1]]
    client_socket.close()
    print(f"Conexão encerrada com {address}")


# Loop principal para aceitar múltiplas conexões
while True:
    client_socket, client_address = server_socket.accept()
    client_socket.send('Dispositivo conectado, se quiser se desconectar pressione "sair"'.encode())

    nameUser = client_socket.recv(1024).decode()

    clientes[client_address[1]] = nameUser
    print(clientes)

    # Cria uma thread para lidar com cada cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
