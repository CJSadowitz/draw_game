import pygame
import tkinter as tk
import os

class Screen:
    game_aspect_ratio = None
    window = None
    is_fullscreen = None
    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None

    def __init__(self):
        Screen.game_aspect_ratio = 4/3
        Screen.window = pygame.display.set_mode((600, 600/Screen.game_aspect_ratio), pygame.RESIZABLE)
        pygame.display.set_caption("Draw")
        Screen.is_fullscreen = False
        root = tk.Tk()
        Screen.SCREEN_WIDTH = root.winfo_screenwidth()
        Screen.SCREEN_HEIGHT = root.winfo_screenheight()

    def window_size():
        return Screen.window.get_size()

    def compute_window_boundaries():                     # Compute where the black bars for the game are (in pixels)
        w = Screen.window_size()[0]
        h = Screen.window_size()[1]
        if Screen.game_aspect_ratio <= w / h:
            x_left = (w - h * Screen.game_aspect_ratio) / 2
            x_right = (w + h * Screen.game_aspect_ratio) / 2
            y_bottom = h
            y_top = 0

        else:
            x_left = 0
            x_right = w
            y_bottom = (h + w / Screen.game_aspect_ratio) / 2
            y_top = (h - w / Screen.game_aspect_ratio) / 2
        return x_left, x_right, y_bottom, y_top

    def to_pixel_coords(window_x, window_y):                    # Window coords (0.0 through 1.0) to pixel coords
        x_left, x_right, y_bottom, y_top = Screen.compute_window_boundaries()
        x = (x_right - x_left) * window_x + x_left
        y = (y_top - y_bottom) * window_y + y_bottom
        return int(x), int(y)

    def to_window_coords(pixel_x, pixel_y):                     # Pixel coords (e.g. (1600, 900)) to window coords
        x_left, x_right, y_bottom, y_top = Screen.compute_window_boundaries()
        window_x = (pixel_x - x_left) / (x_right - x_left)
        window_y = (pixel_y - y_bottom) / (y_top - y_bottom)
        return window_x, window_y

    def mouse_in_rectangle(window_coords_4_tuple):              # (x1, y1, x2, y2); coords from 0.0 to 1.0
        mouse_pixel_coords = pygame.mouse.get_pos()
        mouse_window_x, mouse_window_y = Screen.to_window_coords(mouse_pixel_coords[0], mouse_pixel_coords[1])
        return (window_coords_4_tuple[0] <= mouse_window_x <= window_coords_4_tuple[2] and
                window_coords_4_tuple[1] <= mouse_window_y <= window_coords_4_tuple[3])

    def to_rect_coords(window_coords_4_tuple):                  # Window coords (0.0 through 1.0) to rect formatting
        x1, y1 = Screen.to_pixel_coords(window_coords_4_tuple[0], window_coords_4_tuple[1])
        x2, y2 = Screen.to_pixel_coords(window_coords_4_tuple[2], window_coords_4_tuple[3])
        w = x2 - x1
        h = -(y2 - y1)
        return x1, y2, w, h                                     # Top-left corner x, y

    def draw_rect(rgba_tuple, window_coords_4_tuple):   # (r, g, b, a), (x1, y1, x2, y2); coords from 0.0 to 1.0
        rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)
        x_left, y_top, width, height = rect_coords_4_tuple      # Pixel coordinates of the rectangle
        rect = pygame.Surface((width, height))                  # Create the rectangle
        rect.fill(rgba_tuple[0:3])                              # Set its rgb color to (r, g, b)
        if len(rgba_tuple) == 4:                                # If an alpha value is provided in rgba_tuple
            rect.set_alpha(rgba_tuple[3])                               # set the rectangle's opacity to alpha
        Screen.window.blit(rect, (x_left, y_top))               # Draw the rectangle to the window

    def draw_sprite(sprite, window_coords_4_tuple):     # pygame.image.load(filename), (x1, y1, x2, y2) in 0.0 to 1.0
        rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)
        x_left, y_top, width, height = rect_coords_4_tuple
        resized_sprite = pygame.transform.scale(sprite, (width, height))
        Screen.window.blit(resized_sprite, (x_left, y_top))

    def toggle_fullscreen():
        pygame.display.quit()
        if Screen.is_fullscreen:
            Screen.window = pygame.display.set_mode((600, 600/Screen.game_aspect_ratio), pygame.RESIZABLE)
            Screen.is_fullscreen = False

        else:
            Screen.window = pygame.display.set_mode((Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT), pygame.RESIZABLE)
            Screen.is_fullscreen = True
        pygame.display.set_caption("Draw")

