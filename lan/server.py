import socket
import threading
import time

# This needs to be running in the background so reconnects can happen
def discover_server():
    discover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discover_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        discover_socket.sendto(b"Game Server", ('<broadcast>', 37020))
        time.sleep(1)

def echo_server(seed):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), 36258))
    server.listen(4)

    clients = []
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Connection from {addr}")
        first_message = clients.index(client_socket) + seed
        print(first_message)
        client_socket.send(first_message.encode('utf-8'))
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
            broadcast_message(f"Broadcast: {message}", client_socket)
        except:
            break
    client_socket.close()
    clients.remove(client_socket)   

def broadcast_message(message, sender_socket):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            client.close()
            clients.remove(client)

def host(seed):
    discover_thread = threading.Thread(target=discover_server)
    discover_thread.start()
    echo_thread = threading.Thread(target=echo_server, args=(seed,))
    echo_thread.start()
    print("Server Started")
    