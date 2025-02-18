import socket
import threading

# Configurações do servidor
host = "0.0.0.0"  # Aceita conexões de qualquer IP
port = 6840

# Criando o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(2)  # Permite até 2 conexões na fila

print(f"Servidor rodando em {host}:{port}")

# Dicionário para armazenar os clientes conectados
clientes = {}

def user1(adres1, adres2):
    messagecl1 = clientes[adres1][1].recv(1024).decode()
    clientes[adres2][1].send(f'O {clientes[adres1][0]}: {messagecl1}'.encode())
    if messagecl1.lower() == "sair":
        return
    print(f'O {clientes[adres1][0]} falou {messagecl1}')

def user2(adres1, adres2):
    messagecl2 = clientes[adres2][1].recv(1024).decode()
    clientes[adres1][1].send(f'O {clientes[adres2][0]}: {messagecl2}'.encode())
    if messagecl2.lower() == "sair":
        return
    print(f'O {clientes[adres1][0]} falou {messagecl2}')



# Função para lidar com cada cliente individualmente
def handle_client(address1, address2):
    print(f"Conexão entre {clientes[address1][0]} e {clientes[address2][0]}")   

    while True:
        user1(address1, address2)
        user2(address1, address2)


    # Remove os clientes da lista ao desconectar
    del clientes[address1]
    del clientes[address2]
    print(f"Conexões encerradas com {address1} e {address2}")

def conex(client_socket, client_address):
    try:
        nameUser = client_socket.recv(1024).decode()
        clientes[client_address] = (nameUser, client_socket)

        print(f"Cliente {client_address} conectado como {nameUser}")

    except Exception as e:
        print(f"Erro ao conectar cliente {client_address}: {e}")

# Loop principal para aceitar múltiplas conexões
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Nova conexão de {client_address}")
    client_socket.send('Dispositivo conectado, se quiser se desconectar pressione "sair"'.encode())

    conex(client_socket, client_address)

    if len(clientes) == 2:
        addresses = list(clientes.keys())
        client_thread = threading.Thread(target=handle_client, args=(addresses[0], addresses[1]))
        client_thread.start()