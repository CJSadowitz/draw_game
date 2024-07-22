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
from lan.client import client
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
                    del server
                except:
                    print("Server DNE")
                display = lan_screen(Screen)
            case "settings":
                display = settings_screen(Screen)
            case "host":
                server = Server()
                host_thread = threading.Thread(target=server.host, args=(59,))
                host_thread.start()
                time.sleep(1)
                # client_thread = threading.Thread(target=client)
                # client_thread.start()
                display = lan_lobby_screen(Screen)
                # if display == "lan": # Shut down the servers
                
                # Show lobby of current players
                # Go to play logic (Host starts game)
            case "connect":
                client_thread = threading.Thread(target=client)
                client_thread.start()
                display = lan_lobby_screen(Screen)
                # Show window to join avalible servers
                # Once joined show the lobby of current players (Cannot start game)
            case "lanplay":
                break
                # join the server as a client, play begins
            case "matchmaking":
                break
            case "private":
                break
    pygame.quit()
    # LAN Game connections
    """Handle creating a server on hosts machine, and joining it as a client,"""
    # P2P matchmaking :D
    """Good luck buddy"""

if __name__ == "__main__":
    main()