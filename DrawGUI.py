import pygame               # Window handler
import tkinter as tk        # Get your monitor (screen)'s dimensions
import os                   # Manage file paths


class Screen:

    game_aspect_ratio = None

    window = None

    is_fullscreen = None

    SCREEN_WIDTH = None
    SCREEN_HEIGHT = None

    ''' Specific to Draw below '''

    # All cards (and "zzz" = back of card) in the game; loaded from Draw in constructor
    all_cards_list = None

    # All cards will be stored in a {"r7" : sprite} dictionary; calculated in constructor
    sprites_dict = None

    # The card associated with each quadrant of a selected wild card
    quadrants_dict = {0: "wcrq", 1: "wcyq", 2: "wcgq", 3: "wcbq",
                      4: "wprq", 5: "wpyq", 6: "wpgq", 7: "wpbq"}

    # Hardcoded locations of the card piles displayed on the window
    # (r, y, g, b, w, deck, discard)
    card_locations = [(5/48, 0, 11/48, 1/4), (13/48, 0, 19/48, 1/4), (21/48, 0, 27/48, 1/4),
                      (29/48, 0, 35/48, 1/4), (37/48, 0, 43/48, 1/4), (17/48, 3/8, 23/48, 5/8),
                      (25/48, 3/8, 31/48, 5/8)]

    # Borders around the cards
    gray = (32, 32, 32)                                 # (r, g, b)
    green = (0, 255, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    border_width = 0.007                                # Window width = 1.0

    # Semi-transparent dark card filters (for illegal cards)

    dark_filter_color = (0, 0, 0, 225)                  # (r, g, b, a)
    less_dark_filter_color = (0, 0, 0, 160)

    def __init__(self, all_cards_list):

        Screen.game_aspect_ratio = 4/3

        Screen.window = pygame.display.set_mode((600, 600/Screen.game_aspect_ratio), pygame.RESIZABLE)
        pygame.display.set_caption("Draw")

        Screen.is_fullscreen = False

        root = tk.Tk()

        Screen.SCREEN_WIDTH = root.winfo_screenwidth()
        Screen.SCREEN_HEIGHT = root.winfo_screenheight()

        ''' Specific to Draw below '''

        Screen.all_cards_list = all_cards_list          # Constructor takes cards_list from Draw

        Screen.sprites_dict = Screen.load_images()      # Load all images and create the {"r7" : sprite} sprites_dict

    @staticmethod
    def window_size():
        return Screen.window.get_size()

    @staticmethod
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

    @staticmethod
    def to_pixel_coords(window_x, window_y):                    # Window coords (0.0 through 1.0) to pixel coords

        x_left, x_right, y_bottom, y_top = Screen.compute_window_boundaries()

        x = (x_right - x_left) * window_x + x_left
        y = (y_top - y_bottom) * window_y + y_bottom

        return int(x), int(y)

    @staticmethod
    def to_window_coords(pixel_x, pixel_y):                     # Pixel coords (e.g. (1600, 900)) to window coords

        x_left, x_right, y_bottom, y_top = Screen.compute_window_boundaries()

        window_x = (pixel_x - x_left) / (x_right - x_left)
        window_y = (pixel_y - y_bottom) / (y_top - y_bottom)

        return window_x, window_y

    @staticmethod
    def mouse_in_rectangle(window_coords_4_tuple):              # (x1, y1, x2, y2); coords from 0.0 to 1.0

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

        rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)

        x_left, y_top, width, height = rect_coords_4_tuple      # Pixel coordinates of the rectangle

        rect = pygame.Surface((width, height))                  # Create the rectangle

        rect.fill(rgba_tuple[0:3])                              # Set its rgb color to (r, g, b)

        if len(rgba_tuple) == 4:                                # If an alpha value is provided in rgba_tuple

            rect.set_alpha(rgba_tuple[3])                               # set the rectangle's opacity to alpha

        Screen.window.blit(rect, (x_left, y_top))               # Draw the rectangle to the window

    @staticmethod
    def draw_sprite(sprite, window_coords_4_tuple):     # pygame.image.load(filename), (x1, y1, x2, y2) in 0.0 to 1.0

        rect_coords_4_tuple = Screen.to_rect_coords(window_coords_4_tuple)

        x_left, y_top, width, height = rect_coords_4_tuple

        resized_sprite = pygame.transform.scale(sprite, (width, height))

        Screen.window.blit(resized_sprite, (x_left, y_top))

    @staticmethod
    def toggle_fullscreen():

        pygame.display.quit()

        if Screen.is_fullscreen:

            Screen.window = pygame.display.set_mode((600, 600/Screen.game_aspect_ratio), pygame.RESIZABLE)

            Screen.is_fullscreen = False

        else:

            Screen.window = pygame.display.set_mode((Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGHT), pygame.RESIZABLE)

            Screen.is_fullscreen = True

        pygame.display.set_caption("Draw")

    ''' Specific to Draw below '''

    @staticmethod
    def mouse_over_pile(index):             # Returns True if the mouse is hovering over index's pile, else False

        return Screen.mouse_in_rectangle(Screen.card_locations[index])

    @staticmethod
    def mouse_hovered_index():              # Returns the index the mouse is over (r, y, g, b, w, deck, discard), or -1

        for i in range(0, 6 + 1):

            if Screen.mouse_over_pile(i):

                return i

        return -1

    @staticmethod
    def border_coords_all_sides(coords):    # Calculate a border (coords) completely surrounding any rectangle coords

        border_coords = (coords[0] - Screen.border_width, coords[1] - Screen.border_width * 4 / 3,
                         coords[2] + Screen.border_width, coords[3] + Screen.border_width * 4 / 3)

        return border_coords

    @staticmethod
    def border_coords_down(coords):         # Calculate a border (coords) only on the bottom of any rectangle coords

        border_coords = (coords[0], coords[1] - Screen.border_width * 4 / 3, coords[2], coords[3])

        return border_coords

    '''----------------------------'''

    @staticmethod
    def draw_card_borders(legal_indices_list):

        for i in range(0, 6 + 1):                                       # r, y, g, b, w, deck, discard

            location = Screen.card_locations[i]                         # Location of the card on the window (0.0 - 1.0)

            border_coords = Screen.border_coords_all_sides(location)    # Calculate the rect coords of the border

            if i == 6:

                Screen.draw_rect(Screen.gray, border_coords)

            elif i in legal_indices_list:

                if Screen.mouse_over_pile(i):       # If the mouse is hovering over the card,

                    Screen.draw_rect(Screen.white, border_coords)

                else:

                    Screen.draw_rect(Screen.green, border_coords)

            else:

                if Screen.mouse_over_pile(i):   # If the mouse is hovering over the card,

                    Screen.draw_rect(Screen.red, border_coords)

                else:

                    Screen.draw_rect(Screen.gray, border_coords)




    @staticmethod
    def draw_dark_card_filters(legal_indices_list):     # Draw a semi-transparent dark filter over illegal cards

        for i in range(0, 4 + 1):                                           # r, y, g, b, w

            # Draw a dark filter over all illegal cards

            if i not in legal_indices_list:

                if Screen.mouse_over_pile(i):

                    Screen.draw_rect(Screen.less_dark_filter_color, Screen.card_locations[i])

                else:

                    Screen.draw_rect(Screen.dark_filter_color, Screen.card_locations[i])

    '''-----------------'''

    @staticmethod
    def load_images():                  # Create all sprites and store in a {"r7" : sprite} dictionary

        # folder_path = os.path.dirname(os.path.abspath(__file__))        # The path of the folder this script is in

        # print(folder_path)

        all_sprites_dict = {}  # Build a {"r7" : sprite} dictionary for all sprites

        for card_str in Screen.all_cards_list:

            card_filename = card_str + ".png"  # e.g. "r7.png"

            sprite = pygame.image.load(os.path.join("assets", card_filename))  # Create the card's sprite

            all_sprites_dict[card_str] = sprite  # Add the "r7" : sprite pair to the dict

        return all_sprites_dict

    @staticmethod
    def top_card(card_list):                                # Returns the top card of a pile

        if len(card_list) > 0:

            return card_list[len(card_list) - 1]

        else:

            return "non"

    @staticmethod
    def double_list_to_top_cards(double_list):              # Returns the top cards of each color

        top_cards = []

        for color_list in double_list:
            top_cards.append(Screen.top_card(color_list))

        return top_cards

    @staticmethod
    def draw_player_hand(double_list):                      # Draw the top card in each color pile (r, y, g, b, w)

        top_color_cards = Screen.double_list_to_top_cards(double_list)

        for i in range(len(top_color_cards)):                           # For every color card, draw it

            Screen.draw_sprite(Screen.sprites_dict[top_color_cards[i]], Screen.card_locations[i])

    @staticmethod
    def mouse_hovered_wild_quadrant(wild_list):

        x_left, y_bottom, x_right, y_top = Screen.card_locations[4]

        x_mid = (x_left + x_right) / 2

        y_mid = (y_bottom + y_top) / 2

        if Screen.mouse_in_rectangle((x_left, y_mid, x_mid, y_top)):            # Top-left quadrant

            quadrant = 0

        elif Screen.mouse_in_rectangle((x_mid, y_mid, x_right, y_top)):         # Top-right quadrant

            quadrant = 1

        elif Screen.mouse_in_rectangle((x_mid, y_bottom, x_right, y_mid)):      # Bottom-right quadrant

            quadrant = 2

        elif Screen.mouse_in_rectangle((x_left, y_bottom, x_mid, y_mid)):       # Bottom-left quadrant

            quadrant = 3

        else:

            return -1

        if Screen.top_card(wild_list) == "wp":                              # Switch to +4 quadrant sprites if needed

            quadrant += 4

        return quadrant

    @staticmethod
    def draw_split_wild_card(wild_list, legal_indices_list, location=card_locations[4]):

        if Screen.mouse_over_pile(4) and 4 in legal_indices_list:

            quadrant = Screen.mouse_hovered_wild_quadrant(wild_list)

            card = Screen.quadrants_dict[quadrant]

            Screen.draw_sprite(Screen.sprites_dict[card], location)

    @staticmethod
    def draw_deck(deck_list):                               # Draw the deck texture (back-of-card) if there are cards

        top_deck_card = Screen.top_card(deck_list)

        if top_deck_card == "non":                                                      # If no card in the deck,

            Screen.draw_sprite(Screen.sprites_dict["non"], Screen.card_locations[5])        # draw no-card texture

        else:                                                                           # If any cards in the deck,

            Screen.draw_sprite(Screen.sprites_dict["zzz"], Screen.card_locations[5])        # draw back-of-card texture

    @staticmethod
    def draw_discard_pile(discard_list):                    # Draw the top card of the discard pile

        top_discarded_card = Screen.top_card(discard_list)                              # Get the top card

        Screen.draw_sprite(Screen.sprites_dict[top_discarded_card], Screen.card_locations[6])       # and draw it

    @staticmethod
    def draw_any_pile_to_top(card_list, legal_indices_list):    # Draw any pile of cards to the top of the window

        card_height = 1/4                                               # Card height = window height / 4

        card_width = card_height / (1.5 * Screen.game_aspect_ratio)

        loop = 22                                                       # The number of cards that fit left-to-right

        for i in range(len(card_list)):                                 # For every card in the pile,

            x_left = (i % loop) * card_width/3                                  # compute card coordinates

            x_right = x_left + card_width

            vertical_shift = card_height/4 * (i // loop)                 # (Used by cards that get moved down a line(s))

            y_bottom = (1 - card_height) - vertical_shift

            y_top = 1 - vertical_shift

            curr_card_coords = (x_left, y_bottom, x_right, y_top)

            curr_border_coords = Screen.border_coords_down(curr_card_coords)    # compute border coords

            Screen.draw_rect(Screen.gray, curr_border_coords)                           # Draw the gray "down-borders"

            Screen.draw_sprite(Screen.sprites_dict[card_list[i]], curr_card_coords)     # Draw the card

            if Screen.mouse_over_pile(4) and i == len(card_list) - 1:   # Draw wild card quadrants on the last card

                quadrant = Screen.mouse_hovered_wild_quadrant(card_list)

                Screen.draw_split_wild_card(card_list, legal_indices_list, curr_card_coords)

    @staticmethod
    def draw_hovered_pile_to_top(double_list, discard_list, legal_indices_list):

        # Draw the pile the mouse is hovering over to the top

        for i in range(0, 4 + 1):                                           # r, y, g, b, w

            if Screen.mouse_over_pile(i):                                   # If mouse hovering over any color pile,

                Screen.draw_any_pile_to_top(double_list[i], legal_indices_list)     # draw it to the top of the screen

        if Screen.mouse_over_pile(6):                                       # If mouse hovering over discard pile,

            Screen.draw_any_pile_to_top(discard_list, legal_indices_list)           # draw it to the top of the screen
