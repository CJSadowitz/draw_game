import pygame
import threading
import time
from Lobby import Lobby
from Button import Button
from menus.auto_aspr import Screen


class Menu:
    def __init__(self, lobby=None):
        # As these lists are updated. They are automatically drawn onto screen
        self.buttons = [] # list of button objects to place on screen
        self.sprites = [] # list of sprite objects to place on screen
        self.lobby = lobby
        self.run = True
        pass
    
    def stop(self):
        self.run = False

    # This method constatly updates the menu, other function calls are gettings to input into this
    def thread(self):
        while self.run:
            Screen.draw_rect((10, 10, 10), (0, 0, 1, 1))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_F11:
                        Screen.toggle_fullscreen()
            for button in self.buttons:
                print("We made it here")
                time.sleep(1)
                Screen.menu_button_rect((button.rgba), (button.four_pos_tuple))
            for sprite in self.sprites:
                Screen.menu_button_sprite((sprite.sprite), (sprite.four_pos_tuple))
            if (self.lobby != None):
                for i in range(len((self.lobby.player_list))):
                    Screen.menu_button_rect((255, 255, 0), (0, 0.2 + i, 0.2, 0.5 + i))
            pygame.display.update()
