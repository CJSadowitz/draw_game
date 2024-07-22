"""
Runs in the background, recieves information from the server, sends it to the game loop
The gameloop will only update on information recieved from the server

First thing that is recieved is the player id and the seed which is stored in the game loop
"""
import socket
import threading

# Need discover logic to find the server to connect to it. Allow user to select the server?
# Once selected join the server and recieve player id and seed
# Once game has started, need to send and recieve information on a given turn

def find_server():
    find_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    find_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    find_server_socket.bind(('', 37020))
    while True:
        message, server_address = find_server_socket.recvfrom(1024)
        if message == b"Game Server":
            return server_address[0]

def client():
    server_ip = find_server()
    print(f"Connecting to server at {server_ip}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 36258))

    message = "Player_Name"
    client.send(message.encode('utf-8'))
    while True:
        try:
            response = client.recv(1024).decode('utf-8')
            if not response:
                continue
            print(f"Server: {response}")
        except:
            print("Failed to recieve message")
