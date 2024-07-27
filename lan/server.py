import socket
import threading
import time

# This needs to be running in the background so reconnects can happen
class Server:

    def __init__(self):
        self.clients = []
        self.usr_names = []
        self.threads = []
        self.card_list = []
        self.game_state = False
        self.stop_event = False

    def discover_server(self):
        print("discover_server: started")
        discover_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discover_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while not self.stop_event:
            discover_socket.sendto(b"Game Server", ('<broadcast>', 37020))
            time.sleep(1)
        print("discover_server: closed")

    def echo_server(self, seed):
        # Get the ip of the host's server
        local_ip = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((local_ip, 36258))
        server.listen(4)
        server.settimeout(1)

        print("echo_server: started")
        while not self.stop_event:
            try:
                client_socket, addr = server.accept()
                self.clients.append(client_socket)
                print(f"Connection from {addr}")
                # Send new player their id and seed
                first_message = str(self.clients.index(client_socket)) + "," + str(seed)
                client_socket.send(first_message.encode('utf-8'))
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                self.threads.append(client_handler)
                client_handler.start()
            except socket.timeout:
                continue
        print("echo_server: closed")

    def handle_client(self, client_socket):
        print("handle_client: started")
        client_socket.settimeout(1) # allows looping (thread doesn't get stuck)
        player_name_recieved = False # get first message and doesn't repeat

        while not self.stop_event:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                # first ever message sent will be the player sending the server its username
                if player_name_recieved == False:
                    self.usr_names.append(message)
                    player_name_recieved = True
                
                elif not message:
                    continue
                
                elif message == "player_count": # send list on pull_request
                    client_socket.send(self.get_player_list().encode())
                    continue
                
                elif message == "card_list": # send list on pull_request
                    client_socket.send(self.get_card_list().encode())
                    continue
            
                if self.game_state == True: # game loop
                    # send the message to all connected clients to start the game
                    start_message = "start_game"
                    self.broadcast_message(start_message)
                    # process received card (place inside the card_list list)
                    print("Server: " + message)
                    self.card_list.append(message)
                    print(card_list)
                    continue

            except socket.timeout:
                continue
            except:
                if client_socket not in self.clients:
                    break
        client_socket.close()
        print("handle_client: closed")
        try:
            self.clients.remove(client_socket)
        except:
            print("Client DNE")

    def broadcast_message(self, message):
        for client in self.clients:
            try:
                client.send(message.encode('utf-8'))
            except Exception as ex:
                print("Broadcast: " + str(ex))

    def stop(self):
        self.stop_event = True
        for thread in self.threads:
            thread.join()
            print("Joined a thread")
    
    def get_player_list(self):
        csv_players = str(len(self.usr_names)) + ","
        if self.usr_names != "":
            for i in range(len(self.usr_names)):
                csv_players += self.usr_names[i] + ","
        return csv_players

    def get_card_list(self):
        csv_cards = str(len(self.card_list)) + ","
        if self.card_list != "":
            for i in range(len(self.card_list)):
                csv_cards += self.card_list[i] + ","
        return csv_cards

    def start_game(self):
        self.game_state = True

    def host(self, seed):
        discover_thread = threading.Thread(target=self.discover_server)
        self.threads.append(discover_thread)
        discover_thread.start()
        echo_thread = threading.Thread(target=self.echo_server, args=(seed,))
        self.threads.append(echo_thread)
        echo_thread.start()
        print("Server Started")
    