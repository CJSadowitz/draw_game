"""
Game loop. Calls appropriate networking engine, and display functions
"""
import pygame

from menus.main_menu import title_screen
from menus.play_menu import play_options_screen
from menus.auto_aspr import Screen


def main():
    running = True
    display = "main_menu"
    Screen()
    while running:
        if display == "main_menu":
            Screen.draw_rect((0, 0, 0), (0, 0, 1, 1))
            display = title_screen(Screen)
        if display == "play":
            Screen.draw_rect((0, 0, 0), (0, 0, 1, 1))
            display = play_options_screen(Screen)
        if display == "online":
            running = False
    pygame.quit()
    # Main menu options:
    """Play, settings, quit: Play having local and online"""
    # LAN Game connections
    """Handle creating a server on hosts machine, and joining it as a client,"""
    # P2P matchmaking :D
    """Good luck buddy"""

if __name__ == "__main__":
    main()