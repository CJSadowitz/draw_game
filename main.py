"""
Game loop. Calls appropriate networking engine, and display functions
"""
import pygame
import threading
import time

from menus.main_menu import title_screen
from menus.play_menu import play_options_screen
from menus.lan_menu import lan_screen
from menus.settings_menu import settings_screen
from menus.online_menu import online_screen
from menus.auto_aspr import Screen
from menus.lan_lobby import lan_lobby_screen
from lan.client import Client
from lan.server import Server

def main():
    running = True
    display = "main_menu"
    Screen()
    # Menu Logic
    while running:
        match display:
            case "quit":
                running = False
            case "main_menu":
                display = title_screen(Screen)
            case "play":
                display = play_options_screen(Screen)
            case "online":
                display = online_screen(Screen)
            case "lan":
                try:
                    server.stop()
                    client.stop()

                    del server
                    del client
                except:
                    print("Server/Client DNE")
                display = lan_screen(Screen)
            case "settings":
                display = settings_screen(Screen)
            case "host":
                server = Server()
                host_thread = threading.Thread(target=server.host, args=(59,))
                host_thread.start()
                time.sleep(0.5)
                client = Client()
                client_thread = threading.Thread(target=client.client)
                client_thread.start()
                time.sleep(0.5)
                player_list = []
                while display == "host":
                    player_list = client.get_player_list()
                    if player_list:
                        break
                display = lan_lobby_screen(Screen, player_list)
            case "connect":
                client = Client()
                client_thread = threading.Thread(target=client.client)
                client_thread.start()
                display = lan_lobby_screen(Screen)
            case "matchmaking":
                break
            case "private":
                break
    pygame.quit()

if __name__ == "__main__":
    main()