"""
Game loop. Calls appropriate networking engine, and display functions
"""
import pygame

from menus.main_menu import title_screen
from menus.play_menu import play_options_screen
from menus.lan_menu import lan_screen
from menus.settings_menu import settings_screen
from menus.online_menu import online_screen
from menus.auto_aspr import Screen

def main():
    running = True
    display = "main_menu"
    Screen()
    while running:
        if display == "quit":
            running = False
        if display == "main_menu":
            display = title_screen(Screen)
        if display == "play":
            display = play_options_screen(Screen)
        if display == "online":
            display = online_screen(Screen)
        if display == "lan":
            display = lan_screen(Screen)
        if display == "settings":
            display = settings_screen(Screen)
    pygame.quit()
    # LAN Game connections
    """Handle creating a server on hosts machine, and joining it as a client,"""
    # P2P matchmaking :D
    """Good luck buddy"""

if __name__ == "__main__":
    main()