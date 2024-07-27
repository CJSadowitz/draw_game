from Screen import Screen    # pygame
from lan.client import Client
from lan.server import Server
from Player_Display import PlayerDisplay
import threading
import pygame
import time

class State:

    current_game_state = None    # The current state the game is in (e.g. "main_menu", "settings", "game", etc.)

    DEFAULT_GAME_STATE = None    # The default game state if run_current_game_state() sees illegal current_game_state

    lan_objects_created = None

    host_client = None

    host_server = None

    def __init__(self):

        State.DEFAULT_GAME_STATE = "bouncing_draw_logo"

        State.set_game_state(State.DEFAULT_GAME_STATE)

        State.lan_objects_created = False

    @staticmethod
    def set_game_state(new_state):
        State.current_game_state = new_state

    @staticmethod
    def run_current_game_state():
        try:                                                # A legal game state will execute its respective function
            exec("State." + State.current_game_state + "()")

        except AttributeError:                              # An unknown game state resets the game
            print("No such game state! Resetting game...")
            State.set_game_state(State.DEFAULT_GAME_STATE)

        except SyntaxError:                                 # An unknown game state resets the game
            print("No such game state! Resetting game...")
            State.set_game_state(State.DEFAULT_GAME_STATE)

    ''' All game states below '''

    @staticmethod
    def bouncing_draw_logo():

        Screen.draw_rect((10, 10, 10), (0, 0, 1, 1))

    @staticmethod
    def host():

        Screen.draw_rect((10, 10, 10), (0, 0, 1, 1))
        # Note: handle if failed to create server
        if State.lan_objects_created == False:
            State.host_server = Server()
            State.host_client = Client()
            server_thread = threading.Thread(target=State.host_server.host, args=(0,)) # 0 is the seed :/
            client_thread = threading.Thread(target=State.host_client.client)
            server_thread.start()
            time.sleep(0.3)
            client_thread.start()
            State.lan_objects_created = True
            time.sleep(0.3)
        # place the players on the screen
        if State.host_client.player_list != "":
            result_list = [item for item in State.host_client.player_list.split(",") if item]
            for i in range(int(State.host_client.player_list[0])):
                PlayerDisplay(i, result_list[i]).place_button()
        # Start game button
        if PlayerDisplay.play_button_rect((93, 44, 178), (0.80, 0.05, 0.90, 0.15)) and (pygame.mouse.get_just_released()[0]):
            # Start game logic
            State.host_server.start_game()
            State.current_game_state = "game"


    @staticmethod
    def connect():

        Screen.draw_rect((10, 10, 10), (0, 0, 1, 1))
        # initialize the client for connection
        # Currently must join after the lobby has been created
        # Back button does not clear server/client threads
        if State.lan_objects_created == False: 
            State.host_client = Client()
            client_thread = threading.Thread(target=State.host_client.client)
            client_thread.start()
            State.lan_objects_created = True
            time.sleep(0.3)
        if State.host_client.player_list != "":
            result_list = [item for item in State.host_client.player_list.split(",") if item]
            for i in range(int(State.host_client.player_list[0])):
                PlayerDisplay(i, result_list[i]).place_button()
        if State.host_client.in_game == True:
            State.current_game_state = "game"


    @staticmethod
    def game():
        Screen.draw_rect((137, 15, 199), (0, 0, 1, 1))
        print("We are in 'game' State")
        time.sleep(1)
        """simply pass in the card to move into this, server will update move list and send it to all clients"""
        # State.host_client.play_move("r1") # This tells the client to send to the server the move to append to the move list
        # print(State.host_client.get_player_list()) # This gets the player list (which is perm set at game start)
        # print(State.host_client.get_move_list()) # This gets all moves that were played this game
        # print(State.host_client.get_player_id_seed())
        """
        Note the following list format:
        player_list: (retrived as string (converted from a list))
        "size,first_connected_player,second_connected_player,"

        move_list: (retrived as string (converted from a list))
        "size,first_played_card,second_played_card,"

        player_id_seed:
        "player_id,seed"
        """
