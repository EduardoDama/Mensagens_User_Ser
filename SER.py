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
lock = threading.Lock()  # Para garantir acesso thread-safe ao dicionário

def handle_client(cl1, cl2):
    while True:
        try:
            # Recebe a mensagem do cliente
            message = clientes[cl1][1].recv(1024).decode()
            if not message or message.lower() == "sair":
                print(f"{clientes[cl1][0]} desconectou.")
                desconectar(cl1, cl2)
                break  # Encerra a thread

            print(f"{clientes[cl1][0]} disse: {message}")
            # Encaminha a mensagem para o outro cliente
            with lock:
                if cl2 in clientes:  # Verifica se o outro cliente ainda está conectado
                    clientes[cl2][1].send(f"{clientes[cl1][0]}: {message}".encode())
        except Exception as e:
            print(f"Erro com {clientes[cl1][0]}: {e}")
            desconectar(cl1, cl2)
            break

def desconectar(cl1, cl2):
    with lock:
        # Remove o cliente que se desconectou
        if cl1 in clientes:
            print(f"Removendo {clientes[cl1][0]} da lista de clientes.")
            clientes[cl1][1].send(f"sair".encode())

            del clientes[cl1]

        # Notifica o outro cliente sobre a desconexão
        if cl2 in clientes:
            try:
                clientes[cl2][1].send(f"{clientes[cl1][0]} saiu da conversa.".encode())
            except Exception as e:
                print(f"Erro ao notificar {clientes[cl2][0]} sobre a desconexão: {e}")

def conex(client_socket, client_address):
    try:
        nameUser = client_socket.recv(1024).decode()
        with lock:
            clientes[client_address] = (nameUser, client_socket)

        print(f"Cliente {client_address} conectado como {nameUser}")
    except Exception as e:
        print(f"Erro ao conectar cliente {client_address}: {e}")

# Loop principal para aceitar múltiplas conexões
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Nova conexão de {client_address}")
    client_socket.send('Dispositivo conectado. Para se desconectar, digite "sair".'.encode())

    conex(client_socket, client_address)

    if len(clientes) == 2:
        addresses = list(clientes.keys())
        client_1 = threading.Thread(target=handle_client, args=(addresses[0], addresses[1]))
        client_2 = threading.Thread(target=handle_client, args=(addresses[1], addresses[0]))
        client_1.start()
        client_2.start()