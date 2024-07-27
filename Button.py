from Screen import Screen            # pygame
from State import State       # Button presses can update the game state (ignore warning)
from lan.server import Server
from lan.client import Client
import threading
import time

class Button:

    all_states_button_dict = {}     # Static dictionary from each game state to the list of all the Button objects in it

    def __init__(self,                                          # Create a single Button object

                 # Required* parameters below

                 game_state,                                    # The game state (as a string) the button is drawn in

                 center_coords_tuple, height, w_h_ratio,        # Coords

                 four_colors_list=None,                         # EITHER (up to) four solid colors OR
                 four_sprites_list=None,                        # (up to) four sprites to define button's texture

                 # Optional parameters below

                 pressable=True,                                # The button can/can't be pressed; defaults to True

                 set_game_state_to=None,                        # Button press changes game state (in State class)
                 function=None,                                 # Button press runs any code (inputted as a string),

                 border_thickness=0.0,                          # The thickness of the (optional) border around button
                 border_side="all",                             # The side of the button the border will be drawn on
                 border_four_colors_list=None,                  # (Up to) four solid colors to define button's border

                 text=None,                                     # The custom text the button will display
                 text_font="Comic Sans MS",                     # The font text will be displayed with ("Comic Sans MS")
                 text_four_colors_list=None                     # (Up to) four solid colors to define button's text

                 ):

        self.game_state = game_state

        self.center_coords_tuple = center_coords_tuple      # (x, y); -0.5 through 0.5; (0, 0) is center of game screen

        self.height = height                                # Relative to game's height; 1.0 = 1.0 game heights
        self.w_h_ratio = w_h_ratio                          # Button's width/height (independent of game's aspect ratio)

        self.window_coords_4_tuple = None
        self.compute_window_coords()                        # Compute the button's bounding rectangle (in window coords)

        '''
                If your button will be drawn with solid colors, set the four_colors_list as follows:

                Use an (r, g, b) tuple to define each of these four distinct colors for your button:
                [pressable & NOT hovered, pressable & hovered, NOT pressable & NOT hovered, NOT pressable & hovered]

                Use None for colors that won't ever be drawn.
        '''

        self.four_colors_list = four_colors_list

        '''
                If instead your button will be drawn with sprites, set the four_sprites_list as follows:

                Use a pygame sprite to define each of these four distinct statuses for your button:
                [pressable & NOT hovered, pressable & hovered, NOT pressable & NOT hovered, NOT pressable & hovered]

                Use None for sprites that won't ever be drawn.
        '''

        self.four_sprites_list = four_sprites_list

        self.pressable = pressable

        self.set_game_state_to = set_game_state_to
        self.function = function

        self.border_thickness = border_thickness
        self.border_side = border_side                                  # "left", "right", "top", "bottom", or "all"
        self.border_four_colors_list = border_four_colors_list          # Define border colors same as four_colors_list

        self.border_window_coords_4_tuple = None
        self.compute_border_window_coords()                 # Compute button's border's bounding rect (window coords)

        self.text = text
        self.text_font = text_font
        self.text_four_colors_list = text_four_colors_list              # Define text colors same as in four_colors_list

        self.text_window_coords_4_tuple = None
        self.compute_text_window_coords()                   # Compute button's text's bounding rect (window coords)

        self.insert_button_into_dict()                      # Insert the button into the static dictionary

    def insert_button_into_dict(self):                  # Insert button into its game state's list in the dictionary

        if self.game_state not in Button.all_states_button_dict:        # If the button's game state is not present,

            Button.all_states_button_dict[self.game_state] = []             # create the state's (empty) list of buttons

        Button.all_states_button_dict[self.game_state].append(self)     # Add the button to its game state's list

    @staticmethod
    def get_curr_state_buttons_list():                  # Get the list of buttons found in the current game state

        if State.current_game_state in Button.all_states_button_dict:       # If current game state has list of buttons,

            return Button.all_states_button_dict[State.current_game_state]          # return it

        else:                                                               # Otherwise, curr game state has no buttons
            return []

    def compute_window_coords(self):                    # Compute and save the button's bounding rect (in window coords)

        x_center, y_center = self.center_coords_tuple

        x_center += 0.5                                             # Adjust from [-0.5, 0.5] center coords
        y_center += 0.5                                             # to [0, 1] window coords

        h = self.height                                             # Height and width of the button (window coords)
        w = h * self.w_h_ratio / Screen.game_aspect_ratio

        x_left = x_center - w / 2                                   # Coordinates of the button (window coords)
        x_right = x_center + w / 2

        y_bottom = y_center - h / 2
        y_top = y_center + h / 2

        self.window_coords_4_tuple = (x_left, y_bottom, x_right, y_top)

    def compute_text_window_coords(self):               # Compute & save button's text's bounding rect (window coords)

        if self.text:                                               # Only compute text coords if button has text

            button_x_left, button_y_bottom, button_x_right, button_y_top = self.window_coords_4_tuple

            x_left = button_x_left + self.border_thickness / Screen.game_aspect_ratio
            x_right = button_x_right - self.border_thickness / Screen.game_aspect_ratio

            y_bottom = button_y_bottom + self.border_thickness
            y_top = button_y_top - self.border_thickness

            self.text_window_coords_4_tuple = (x_left, y_bottom, x_right, y_top)

    def compute_border_window_coords(self):             # Compute & save button's border's bounding rect (window coords)

        if self.border_thickness:                                   # Only compute border coords if button has a border

            button_x_left, button_y_bottom, button_x_right, button_y_top = self.window_coords_4_tuple

            x_left = button_x_left - self.border_thickness / Screen.game_aspect_ratio
            x_right = button_x_right + self.border_thickness / Screen.game_aspect_ratio

            y_bottom = button_y_bottom - self.border_thickness
            y_top = button_y_top + self.border_thickness

            self.border_window_coords_4_tuple = (x_left, y_bottom, x_right, y_top)

    def mouse_over_button(self):                        # Returns True if mouse is currently hovering over the button

        return Screen.mouse_in_rectangle(self.window_coords_4_tuple)

    def draw_button(self):                              # Draw the button, its text, and its border (if it has these)

        if self.pressable and not self.mouse_over_button():         # Button is pressable and NOT hovered over
            index = 0
        elif self.pressable and self.mouse_over_button():           # Button is pressable and hovered over
            index = 1
        elif not self.pressable and not self.mouse_over_button():   # Button is NOT pressable and NOT hovered over
            index = 2
        else:                                                       # Button is NOT pressable and hovered over
            index = 3

        if self.four_sprites_list:                                  # Button is drawn with sprites
            Screen.draw_sprite(self.four_sprites_list[index], self.window_coords_4_tuple)

        elif self.four_colors_list:                                 # Button is drawn with solid colors
            Screen.draw_rect(self.four_colors_list[index], self.window_coords_4_tuple)

        if self.text:                                               # Button is drawn with text
            Screen.draw_text(self.text, self.text_font, self.text_four_colors_list[index], self.text_window_coords_4_tuple)

    @staticmethod
    def draw_all_buttons():                             # Draw all buttons in the current game state

        for button in Button.get_curr_state_buttons_list():         # For each button in the current game state,

            button.draw_button()                                            # draw it

    def attempt_pressing_button(self):                  # Attempt pressing button from anywhere (even if mouse is far)

        if self.pressable and self.mouse_over_button():             # If button is pressable and hovered over,

            try:
                # set game state (in State class)
                if self.set_game_state_to:
                    exec("State.set_game_state('" + self.set_game_state_to + "')")

                # execute button's function (input parameter)
                if self.function:
                    exec(self.function)

            except SyntaxError:
                pass

    @staticmethod
    def attempt_pressing_all_buttons():                 # Attempt to press all buttons in the current game state

        for button in Button.get_curr_state_buttons_list():         # For each button in the current game state,

            button.attempt_pressing_button()                                # attempt pressing it
