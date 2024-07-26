import pygame
import threading
import time
from Lobby import Lobby
from Button import Button
from menus.auto_aspr import Screen


class Menu:
    def __init__(self, lobby=None):
        # As these lists are updated. They are automatically drawn onto screen
        self.button_objects = [] # list of button objects to place on screen
        self.button_interactables = [] # interactable spaces on the screen
        self.sprites = [] # list of sprite objects to place on screen
        self.lobby = lobby
        self.run = True
        self.next_menu = ""
        pass
    
    def stop(self):
        self.run = False
    
    def buttons(self):
        for button in self.button_objects:
            button_title = button.title
            button_bool = Screen.menu_button_rect((button.rgba), (button.four_pos_tuple))
            self.button_interactables.append((button_title, button_bool))
        for sprite in self.sprites:
            Screen.menu_button_sprite((sprite.sprite), (sprite.four_pos_tuple))
        if (self.lobby != None):
            for i in range(len((self.lobby.player_list))):
                Screen.menu_button_rect((255, 255, 0), (0, 0.2 + i, 0.2, 0.5 + i))
    
    def reset_buttons(self):
        for button in self.button_objects:
            pass


    # This method constatly updates the menu, other function calls are gettings to input into this
    def thread(self):
        while self.run:
            Screen.draw_rect((10, 10, 10), (0, 0, 1, 1))
            self.next_menu = ""
            self.buttons()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_F11:
                        Screen.toggle_fullscreen()
            if (pygame.mouse.get_just_released()[0]):
                for button_tuple in self.button_interactables:
                    if button_tuple[1] == True:
                        self.next_menu = button_tuple[0]
                        print(self.next_menu)
                        self.run = False
                        break
                        

            
            pygame.display.update()
