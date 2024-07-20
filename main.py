"""
Game loop. Calls appropriate networking engine, and display functions
"""
import pygame
import threading

from menus.main_menu import title_screen
from menus.play_menu import play_options_screen
from menus.lan_menu import lan_screen
from menus.settings_menu import settings_screen
from menus.online_menu import online_screen
from menus.auto_aspr import Screen
from lan.server import host

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
                display = lan_screen(Screen)
            case "settings":
                display = settings_screen(Screen)
            case "host":
                print("Do we make it here")
                host_thread = threading.Thread(target=host, args=(1,))
                host_thread.start()
                display = title_screen(Screen)
                # Show lobby of current players
                # Go to play logic (Host starts game)
            case "connect":
                break
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