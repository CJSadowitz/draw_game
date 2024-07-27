import pygame               # Window handler
import tkinter as tk        # Get your monitor's dimensions (in px)


class Screen:

    game_aspect_ratio = None        # The fixed aspect ratio of the actual render area (ignoring black bars)

    window = None                   # The pygame window (which can be resized by the user at will)

    is_fullscreen = None            # Tracks if the user has toggled fullscreen via F11

    SCREEN_WIDTH_PX = None          # The width and height (px) of your monitor (for fullscreen)
    SCREEN_HEIGHT_PX = None

    ''' Drawing text '''

    font_parameters_dict = None     # A dict from fonts to their (optional_v_scale, optional_v_shift) parameters

    def __init__(self):

        Screen.game_aspect_ratio = 4/3

        Screen.window = pygame.display.set_mode((600, 600/Screen.game_aspect_ratio), pygame.RESIZABLE)
        pygame.display.set_caption("Draw")

        Screen.is_fullscreen = False

        root = tk.Tk()

        Screen.SCREEN_WIDTH_PX = root.winfo_screenwidth()
        Screen.SCREEN_HEIGHT_PX = root.winfo_screenheight()

        ''' Drawing text '''

        pygame.font.init()                                                  # Initialize fonts to draw text
        Screen.font_parameters_dict = {"Comic Sans MS": (1.6, 0.025)}       # Each font's optional parameters

    @staticmethod
    def toggle_fullscreen():

        pygame.display.quit()

        if Screen.is_fullscreen:

            Screen.window = pygame.display.set_mode((600, 600/Screen.game_aspect_ratio), pygame.RESIZABLE)

        else:

            Screen.window = pygame.display.set_mode((Screen.SCREEN_WIDTH_PX, Screen.SCREEN_HEIGHT_PX),
                                                    pygame.RESIZABLE)

        pygame.display.set_caption("Draw")

        Screen.is_fullscreen = not Screen.is_fullscreen

    @staticmethod
    def compute_render_boundaries():                # Compute where the actual render area is (in pixel coords)

        w, h = Screen.window.get_size()

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

    @staticmethod
    def to_pixel_coords(window_x, window_y):        # Window coords (0.0 through 1.0) to pixel coords

        x_left, x_right, y_bottom, y_top = Screen.compute_render_boundaries()

        x = window_x * (x_right - x_left) + x_left
        y = window_y * (y_top - y_bottom) + y_bottom

        return int(x), int(y)

    @staticmethod
    def to_window_coords(pixel_x, pixel_y):         # Pixel coords (e.g. (1600, 900)) to window coords

        x_left, x_right, y_bottom, y_top = Screen.compute_render_boundaries()

        window_x = (pixel_x - x_left) / (x_right - x_left)
        window_y = (pixel_y - y_bottom) / (y_top - y_bottom)

        return window_x, window_y

    @staticmethod
    def mouse_in_rectangle(window_coords_4_tuple):  # (x1, y1, x2, y2); coords from 0.0 to 1.0

        mouse_pixel_coords = pygame.mouse.get_pos()

        mouse_window_x, mouse_window_y = Screen.to_window_coords(mouse_pixel_coords[0], mouse_pixel_coords[1])

        return (window_coords_4_tuple[0] <= mouse_window_x <= window_coords_4_tuple[2] and
                window_coords_4_tuple[1] <= mouse_window_y <= window_coords_4_tuple[3])

    @staticmethod
    def to_rect_coords(window_coords_4_tuple):                  # Window coords (0.0 through 1.0) to rect formatting

        x1, y1 = Screen.to_pixel_coords(window_coords_4_tuple[0], window_coords_4_tuple[1])

        x2, y2 = Screen.to_pixel_coords(window_coords_4_tuple[2], window_coords_4_tuple[3])

        w = x2 - x1
        h = -(y2 - y1)

        return x1, y2, w, h                                     # Top-left corner x, y

    @staticmethod
    def draw_rect(rgba_tuple, window_coords_4_tuple):   # (r, g, b, a), (x1, y1, x2, y2); coords from 0.0 to 1.0

        if rgba_tuple:                                              # Only draw the rectangle if a color is inputted

            rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)

            x_left, y_top, width, height = rect_coords_4_tuple      # Pixel coordinates of the rectangle

            rect = pygame.Surface((width, height))                  # Create the rectangle

            rect.fill(rgba_tuple[0:3])                              # Set its rgb color to (r, g, b)

            if len(rgba_tuple) == 4:                                # If an alpha value is provided in rgba_tuple,
                rect.set_alpha(rgba_tuple[3])                           # set the rectangle's opacity to alpha (0 - 255)

            Screen.window.blit(rect, (x_left, y_top))               # Draw the rectangle to the window

    @staticmethod
    def draw_sprite(sprite, window_coords_4_tuple):     # pygame.image.load(filename), (x1, y1, x2, y2) in 0.0 to 1.0

        if sprite:                                                   # Only draw the sprite if one is inputted

            rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)

            x_left, y_top, width, height = rect_coords_4_tuple

            resized_sprite = pygame.transform.scale(sprite, (width, height))

            Screen.window.blit(resized_sprite, (x_left, y_top))

    @staticmethod
    def draw_text(text, font, rgba_tuple, window_coords_4_tuple):

        # Examples:
        # text = "Hello world!"
        # font = "Comic Sans MS"
        # rgba_tuple = (255, 0, 0)
        # window_coords_4_tuple defines your bounding rectangle the text must fit within (e.g. (0, 0, 0.5, 0.5))
        # See below for info on the optional_v_scale & optional_v_shift font parameters in constructor

        if font in Screen.font_parameters_dict:    # If there are vertical parameters for this font in the constructor,

            optional_v_scale, optional_v_shift = Screen.font_parameters_dict[font]      # use them (as described below)

        else:                                       # Otherwise, default to standard vertical alignment
            optional_v_scale = 1.0
            optional_v_shift = 0.0

        rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)

        rect_x_left, rect_y_top, rect_w, rect_h = rect_coords_4_tuple               # Dimensions of bounding rect (px)

        ''' Create test text w/ font size 100 to compute the font size that will fit in user's bounding rectangle '''

        test_font = pygame.font.SysFont(font, 100)
        test_surface = test_font.render(text, True, (0, 0, 0))

        test_w, test_h = test_surface.get_size()                                    # Dimensions of test text (px)

        test_h /= optional_v_scale                                                  # (See bottom of function)

        if rect_w / rect_h <= test_w / test_h:                      # Test text has wider ratio than bounding rectangle

            font_size = int(100 * rect_w / test_w)

        else:                                                       # Test text has taller ratio than bounding rectangle

            font_size = int(100 * rect_h / test_h)

        ''' Create the actual text that fits the user's bounding rectangle, using computed font_size '''

        actual_font = pygame.font.SysFont(font, font_size)
        surface = actual_font.render(text, True, rgba_tuple[0:3])

        if len(rgba_tuple) == 4:                                    # If an alpha value is provided in rgba_tuple,

            surface.set_alpha(rgba_tuple[3])                                # set the text's opacity to alpha (0 - 255)

        text_w, text_h = surface.get_size()                         # Dimensions (px) of the actual text

        text_x_left = rect_x_left + (rect_w - text_w) / 2
        text_y_top = rect_y_top + (rect_h - text_h) / 2 - (optional_v_shift * text_h)

        Screen.window.blit(surface, (text_x_left, text_y_top))

        '''
            pygame's internal text surface often wastes vertical space (varies with font & text),
            so you can manually adjust the optional_v_scale (when calling draw_text())
            to >1.0 to exceed your bounding box and recover this space, making text a better fit.
            You can also modify optional_v_shift to vertically align text (+1.0 is up 1.0 pygame text surfaces)

            (Visualize this by uncommenting below)
        '''

        '''

        # Dimensions of the text surface (px)

        text_x_right = text_x_left + text_w
        text_y_bottom = text_y_top + text_h

        # Dimensions of the text surface (window coords)

        text_x_left_win, text_y_top_win = Screen.to_window_coords(text_x_left, text_y_top)

        text_x_right_win, text_y_bottom_win = Screen.to_window_coords(text_x_right, text_y_bottom)

        surface_window_coords_4_tuple = (text_x_left_win, text_y_bottom_win, text_x_right_win, text_y_top_win)

        # Bounding rectangle the user defined (drawn in gray)

        Screen.draw_rect((64, 64, 64, 128), window_coords_4_tuple)

        # pygame's internal text surface (drawn in user's text color)

        Screen.draw_rect((rgba_tuple[0:3] + (64,)), surface_window_coords_4_tuple)
        
        '''
