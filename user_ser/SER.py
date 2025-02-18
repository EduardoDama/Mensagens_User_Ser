import socket

# Criar um socket TCP (SOCK_STREAM) 
# (AF_INET indica que usaremos ipv4, se fosse ipv6 AF_NET6)
# (SOCK.STREAM fala que vamos usar TCP, se fosse UDP usaria SOCK.DGRAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Definir endereço e porta do servidor 
host = '127.0.0.1'  # Endereço local IPV4
port = 6840        # Porta para comunicação

# Associar o socket ao endereço e porta
#falar por onde vamos nos comunicar e vincula a essa conexão
server_socket.bind((host, port))

# Colocar o socket no modo de escuta
server_socket.listen(5)  # Aceita até 5 conexões

print(f"Servidor ouvindo em {host}:{port}...")
while True:
    client_socket, addr = server_socket.accept()
    print(f"Dispositivo conectado: {addr}")

    client_socket.send("Dispositivo conectado ao servidor, se quiser desconectar, digite 'sair'".encode())

    while True:
        mensagemClie = client_socket.recv(1024).decode() 

        if mensagemClie.upper() == 'SAIR':
            client_socket.send("desc".encode())
            break

        print(f"{mensagemClie}")
        mensagemSR = input('Qual a sua mensagem: ')

        client_socket.send(mensagemSR.encode())
        
    if input('Quer desligar o servidor? (S/N): ').upper() == 'S':
        break