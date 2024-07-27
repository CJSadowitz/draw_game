import pygame
from Screen import Screen

class PlayerDisplay:
    def __init__(self, index, name):
        self.index = index
        self.name = name

    def player_color_rect(self, rgba, four_pos_tuple):
        rect_coords_4_tuple = Screen.to_rect_coords(four_pos_tuple)
        x_left, y_top, width, height = rect_coords_4_tuple
        Screen.draw_rect(rgba, four_pos_tuple)

    @staticmethod
    def play_button_rect(rgba, four_pos_tuple):
        rect_coords_4_tuple = Screen.to_rect_coords(four_pos_tuple)
        x_left, y_top, width, height = rect_coords_4_tuple
        Screen.draw_rect(rgba, four_pos_tuple)
        if (pygame.mouse.get_pos()[0] >= (x_left) and
            pygame.mouse.get_pos()[1] >= (y_top) and
            pygame.mouse.get_pos()[0] <= (x_left + width) and
            pygame.mouse.get_pos()[1] <= (y_top + height)):
            return True
        else:
            return False
    
    def place_button(self):
        rgba = (0, 250, 128)
        four_tuple = (0.05, 0.2 + 0.15 * self.index, 0.95, 0.3 + 0.15 * self.index)
        self.player_color_rect(rgba, four_tuple)