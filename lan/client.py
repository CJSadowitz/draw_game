"""
Runs in the background, recieves information from the server, sends it to the game loop
The gameloop will only update on information recieved from the server

First thing that is recieved is the player id and the seed which is stored in the game loop
"""
import socket
import threading
import time

# Need discover logic to find the server to connect to it. Allow user to select the server?
# Once selected join the server and recieve player id and seed
# Once game has started, need to send and recieve information on a given turn
class Client():
    
    def __init__(self):
        self.is_active = True
        self.in_game = False
        self.first_message = False
        self.move_list = []
        self.player_list = []
        self.player_id_seed = ""

    def stop(self):
        self.is_active = False
    
    def get_move_list(self):
        return self.move_list
    
    def get_player_list(self):
        return self.player_list

    def find_server(self):
        find_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        find_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        find_server_socket.bind(('', 37020))
        while True:
            message, server_address = find_server_socket.recvfrom(1024)
            if message == b"Game Server":
                return server_address[0]

    def client(self):
        server_ip = self.find_server()
        print(f"Connecting to server at {server_ip}...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, 36258))
        client.settimeout(1)

        message = "Player_1"
        client.send(message.encode('utf-8'))
        time.sleep(0.2)
        while self.is_active:
            try:
                if self.first_message == False:
                    response = client.recv(1024).decode('utf-8')
                    if not response:
                        continue
                    self.player_id_seed = response
                    self.first_message = True
                elif self.in_game == False:
                    player_count_pull_request = "player_count"
                    client.send(player_count_pull_request.encode('utf-8'))
                    response = client.recv(1024).decode('utf-8')
                    if response == "start_game":
                        self.in_game = True
                    elif not response:
                        continue
                    self.player_list = response
                    time.sleep(1)

                else:
                    response = client.recv(1024).decode('utf-8')
                    if response[0] == 'm': # move list flag
                        self.move_list = response
                    if not response:
                        continue
                    print(f"Server: {response}")
            except:
                break
            
