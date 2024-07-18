# PROGRAM:DRAW

import socket                   # Connection to server
import time                     # Delays
import pygame                   # Window handler
import tkinter as tk            # Get your monitor (screen)'s dimensions
import os                       # Manage file paths

from DrawGUI import Screen      # The Screen class (drawing sprites to window)

int_to_card_dict = {

    1:  "r1",       13: "y1",       25: "g1",       37: "b1",
    2:  "r2",       14: "y2",       26: "g2",       38: "b2",
    3:  "r3",       15: "y3",       27: "g3",       39: "b3",
    4:  "r4",       16: "y4",       28: "g4",       40: "b4",
    5:  "r5",       17: "y5",       29: "g5",       41: "b5",
    6:  "r6",       18: "y6",       30: "g6",       42: "b6",
    7:  "r7",       19: "y7",       31: "g7",       43: "b7",
    8:  "r8",       20: "y8",       32: "g8",       44: "b8",
    9:  "r9",       21: "y9",       33: "g9",       45: "b9",
    10: "rs",       22: "ys",       34: "gs",       46: "bs",
    11: "rr",       23: "yr",       35: "gr",       47: "br",
    12: "rp",       24: "yp",       36: "gp",       48: "bp",

    49: "r1",       61: "y1",       73: "g1",       85: "b1",
    50: "r2",       62: "y2",       74: "g2",       86: "b2",
    51: "r3",       63: "y3",       75: "g3",       87: "b3",
    52: "r4",       64: "y4",       76: "g4",       88: "b4",
    53: "r5",       65: "y5",       77: "g5",       89: "b5",
    54: "r6",       66: "y6",       78: "g6",       90: "b6",
    55: "r7",       67: "y7",       79: "g7",       91: "b7",
    56: "r8",       68: "y8",       80: "g8",       92: "b8",
    57: "r9",       69: "y9",       81: "g9",       93: "b9",
    58: "rs",       70: "ys",       82: "gs",       94: "bs",
    59: "rr",       71: "yr",       83: "gr",       95: "br",
    60: "rp",       72: "yp",       84: "gp",       96: "bp",

    97: "r0",       101: "wc",      105: "wp",
    98: "y0",       102: "wc",      106: "wp",
    99: "g0",       103: "wc",      107: "wp",
    100: "b0",      104: "wc",      108: "wp",

    # Non-holdable cards below

    109: "wcr",     113: "wpr",     117: "wcrq",    121: "wprq",
    110: "wcy",     114: "wpy",     118: "wcyq",    122: "wpyq",
    111: "wcg",     115: "wpg",     119: "wcgq",    123: "wpgq",
    112: "wcb",     116: "wpb",     120: "wcbq",    124: "wpbq",

    125: "zzz",
    -1: "non"

}

'''
    "rs" = red skip
    "rr" = red reverse
    "rp" = red +2

    "wc" = wild card
    "wp" = +4
    
    "wcr" = wild card, red (in discard pile)
    "wcrq" = wild card, red quadrant (during selection)
    "zzz" = back of card (texture)
    "non" = no card (black)
    
'''

# All cards (and "zzz" = back of card) in the game
cards_list = sorted(set(int_to_card_dict.values()))

# print(cards_list)

colors_dict = {

    'r': 0,     # red
    'y': 1,     # yellow
    'g': 2,     # green
    'b': 3,     # blue
    'w': 4,     # wild

}


class Turn:

    counter = 0         # 0 through 3 (for 4 players)

    direction = 1       # 1 (forwards) or -1 (reversed)

    @staticmethod
    def advance_turn_counter(num):      # Advance the turn counter by num in the correct direction

        Turn.counter = (Turn.counter + (Turn.direction * num)) % 4

    @staticmethod
    def reverse_turn_direction():       # For reverse cards

        Turn.direction *= (-1)


class Pseudo:                       # Pseudo RNG class with seeding

    A = 40014
    B = 40692
    M1 = (2 ** 31) - 85
    M2 = (2 ** 31) - 249

    # period = M1 * M2

    def __init__(self, int_seed=0):

        if int_seed == 0:

            self.s1 = 12345
            self.s2 = 67890

        else:

            self.s1 = (Pseudo.A * seed) % Pseudo.M1
            self.s2 = seed % Pseudo.M2

    def rand_int(self, lower, upper):

        self.s1 = (Pseudo.A * self.s1) % Pseudo.M1
        self.s2 = (Pseudo.B * self.s2) % Pseudo.M2

        rand_float = ((self.s1 - self.s2) / Pseudo.M1) % 1

        rand_int = lower + int(rand_float * (upper - lower + 1))

        return rand_int

    def rand_int_list(self, lower, upper, length):

        rand_int_list = [self.rand_int(lower, upper) for _ in range(0, length)]

        return rand_int_list


def shuffle_pile_ints(int_list, int_seed):      # Returns the list of ints, shuffled deterministically by the seed

    rand_obj = Pseudo(int_seed)

    indices_list = rand_obj.rand_int_list(0, len(int_list) - 1, len(int_list))

    for i in range(len(int_list)):

        temp = int_list[i]

        int_list[i] = int_list[indices_list[i]]

        int_list[indices_list[i]] = temp

    return int_list


def card(num):                                                      # card(1) = "r1"

    try:

        return int_to_card_dict[num]

    except KeyError:                                                # card(-1) = ""

        return ""


def int_list_to_cards(int_list):                                    # int_list_to_cards([1, 2, 3]) = ['r1', 'r2', 'r3']

    return [card(num) for num in int_list]


def double_int_list(int_list):                                      # Sorts a player's cards (as ints) into each color

    double_list = [[], [], [], [], []]                              # r, y, g, b, w

    for num in int_list:

        if card(num)[0] == 'r':

            double_list[0].append(num)

        elif card(num)[0] == 'y':

            double_list[1].append(num)

        elif card(num)[0] == 'g':

            double_list[2].append(num)

        elif card(num)[0] == 'b':

            double_list[3].append(num)

        elif card(num)[0] == 'w':

            double_list[4].append(num)

    return double_list


def double_int_list_to_cards(double_list):                          # Displays a double list as cards (e.g. "r1")

    double_card_list = [[], [], [], [], []]                         # r, y, g, b, w

    for i in range(5):

        for num in double_list[i]:

            double_card_list[i].append(card(num))

    return double_card_list


def legal_indices_list(player_double_int_list, deck_int_list, discard_int_list):        # r, y, g, b, w, deck

    if len(discard_int_list) == 0:                                  # For the first move in the game, all choices legal

        legal_list = []

        for i in range(len(player_double_int_list)):                # For every color,

            if len(player_double_int_list[i]) > 0:                          # if that color has cards,

                legal_list.append(i)                                        # it's legal

        legal_list.append(5)                                        # Drawing from the deck always legal for first move

        return legal_list

    top_cards_int_list = []                                         # Find the top card of every color (r, y, g, b, w)

    for i in range(0, 5):

        curr_color_list = player_double_int_list[i]

        if len(curr_color_list) > 0:                                # The current color has a card

            curr_color_top_card = curr_color_list[len(curr_color_list) - 1]

        else:                                                       # The current color doesn't have a card

            curr_color_top_card = -1

        top_cards_int_list.append(curr_color_top_card)

    top_cards_list = int_list_to_cards(top_cards_int_list)          # The top card of every color (r, y, g, b, w)

    # print(top_cards_list)

    top_discarded_card = card(discard_int_list[len(discard_int_list) - 1])      # The discard pile's top card

    # print(top_discarded_card)

    all_legal_indices = set()                                       # The set of all legal indices

    for i in range(len(top_cards_list)):                            # Check every color's top card for a color match

        try:

            curr_top_card_color = top_cards_list[i][0]              # The color of the current top card, if it exists

        except IndexError:

            curr_top_card_color = ''                                # This color doesn't have a top card

        if curr_top_card_color == top_discarded_card[0] and curr_top_card_color != 'w':   # The colors match (ignore wilds)

            all_legal_indices.add(colors_dict[curr_top_card_color])

        if len(top_discarded_card) == 3 and curr_top_card_color == top_discarded_card[2]:       # Colored wild card on top of discard pile

            all_legal_indices.add(colors_dict[curr_top_card_color])

    for i in range(len(top_cards_list)):                            # Check every color's top card for a number match

        try:

            curr_top_card_number = int(top_cards_list[i][1])        # The number of the current top card, if it exists

        except IndexError:

            curr_top_card_number = -1                               # This color doesn't have a top card

        except ValueError:

            curr_top_card_number = -1                               # This color's top card isn't a number card

        try:

            top_discarded_number = int(top_discarded_card[1])       # The number of the discard pile's top card

        except ValueError:

            top_discarded_number = -1                                # The discard pile's top card isn't a number card

        if curr_top_card_number == top_discarded_number and curr_top_card_number != -1:  # The numbers match (both nums)

            all_legal_indices.add(i)

    if top_discarded_card[1] in ['s', 'r', 'p'] and top_discarded_card[0] != 'w':       # Skips, reverses, and plus 2's

        for i in range(len(top_cards_list)):                        # Check every color's top card for a match

            try:

                curr_top_card_color = top_cards_list[i][0]          # The color of the current top card, if it exists

                curr_top_card_type = top_cards_list[i][1]           # The type of the current top card, if it exists

            except IndexError:

                curr_top_card_color = ''                            # This color doesn't have a top card

                curr_top_card_type = ''                             # This color doesn't have a top card

            if curr_top_card_type == top_discarded_card[1] and curr_top_card_color != 'w':

                all_legal_indices.add(i)                            # The cards match (e.g. both skips, etc.)

    if top_cards_list[4] == "wc":    # A wild card can always be played

        all_legal_indices.add(4)

    if top_cards_list[4] == "wp" and len(all_legal_indices) == 0:

        # A +4 card can be played iff all the player's other colors are illegal (the player can still draw)

        all_legal_indices.add(4)

    if len(deck_int_list) + len(discard_int_list) > 1:

        all_legal_indices.add(5)

    return sorted(all_legal_indices)


# Connect to client socket

# cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# cs.connect(('10.42.0.1', 36258))

try:

    # initial_info = cs.recv(1024).decode("UTF-8")        # Receive player_id and seed in one string

    initial_info = "042"

    print("initial_info = " + initial_info)

    ''' Your unique player id (0 through 3); it is your turn iff Turn.counter == your_player_id'''

    your_player_id = int(initial_info[0])

    ''' The seed for the Pseudo RNG class; used to create the shuffled deck of 108 cards '''

    seed = int(initial_info[1:])

except:

    print("Failed to get initial_info")

''' Create a sorted deck of 108 cards '''

all_cards_ints = [i for i in range(1, 109)]                         # List of all cards, sorted ([1, 2, 3, ... 108])

''' Shuffle the deck of 108 cards (with Pseudo RNG) '''

all_cards_shuffled_ints = shuffle_pile_ints(all_cards_ints, seed)           # Shuffled deck (ints) of 108 cards

num_cards_each = 13                                                         # Number of starting cards per player

''' Create each player's hand of 13 cards (4 double int lists, each sorted by color) '''

players_triple_int_list = [[], [], [], []]                                  # 4 nested double lists; faster indexing :)

players_triple_int_list[0] = double_int_list(all_cards_shuffled_ints[0:1*num_cards_each])

players_triple_int_list[1] = double_int_list(all_cards_shuffled_ints[1*num_cards_each:2*num_cards_each])

players_triple_int_list[2] = double_int_list(all_cards_shuffled_ints[2*num_cards_each:3*num_cards_each])

players_triple_int_list[3] = double_int_list(all_cards_shuffled_ints[3*num_cards_each:4*num_cards_each])

''' The deck you draw from (the 52 cards to the players have been removed) '''

deck_ints = all_cards_shuffled_ints[4*num_cards_each:108]

''' The pile of discarded cards (the player must match their card to the discard pile's top card) '''

discard_pile_ints = [1]

''' Instantiate the Screen class to handle basically everything in pygame '''

Screen(cards_list)

# Game LOOP :D
running = True

while running:

    ''' Variables for Screen class (pygame) '''

    curr_double_int_list = players_triple_int_list[Turn.counter]                        # Current player's hand (ints)

    curr_double_list = double_int_list_to_cards(curr_double_int_list)                   # The current player's hand

    deck = int_list_to_cards(deck_ints)                                                 # The current deck

    discard_pile = int_list_to_cards(discard_pile_ints)                                 # The current discard pile

    legal_choices = legal_indices_list(curr_double_int_list, deck_ints, discard_pile_ints)   # All legal piles to play

    ''' ——————————————————————————————————— '''

    Screen.draw_rect((0, 0, 0), (0, 0, 1, 1))       # Black background

    Screen.draw_any_pile_to_top(deck, legal_choices)                            # TEMP : DELETE THIS

    Screen.draw_card_borders(legal_choices)                                     # Colored borders around every pile

    Screen.draw_player_hand(curr_double_list)                                   # r, y, g, b, w piles

    Screen.draw_dark_card_filters(legal_choices)                                # Dark filters over illegal cards

    Screen.draw_hovered_pile_to_top(curr_double_list, discard_pile, legal_choices)  # Draw mouse-hovered pile to the top

    Screen.draw_deck(deck)                                                      # The deck

    Screen.draw_discard_pile(discard_pile)                                      # The discard pile

    Screen.draw_split_wild_card(curr_double_list[4], legal_choices)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_F11:               # F11 (fullscreen)

                Screen.toggle_fullscreen()

        elif event.type == pygame.MOUSEBUTTONDOWN:      # Mouse press (play the mouse-hovered card)

            if Screen.mouse_hovered_index() in legal_choices:

                choice = Screen.mouse_hovered_index()

                if choice in range(0, 4 + 1):

                    curr_color_list = curr_double_int_list[choice]

                    # The card the player is going to play
                    curr_card = curr_color_list[len(curr_color_list) - 1]

                    print(card(curr_card))

                    # Remove the player's card from its pile and put everything back into the 4-player triple list
                    del curr_color_list[len(curr_color_list) - 1]

                    players_triple_int_list[your_player_id][choice] = curr_color_list

                    if choice == 4:

                        quadrant = Screen.mouse_hovered_wild_quadrant(curr_double_list[4])

                        if card == "wp":

                            curr_card += 4

                        curr_card = quadrant + 109

                    # Put the card being played into the played cards pile
                    discard_pile_ints.append(curr_card)

                else:  # Draw from the deck

                    keep_drawing = True

                    while keep_drawing:

                        # The player's hand
                        player_double_list = players_triple_int_list[Turn.counter]

                        if len(deck_ints) > 0:

                            # Get the current card being drawn from the top of the deck
                            current_card = deck_ints[len(deck_ints) - 1]

                            # Calculate where to place the player's drawn card in their hand
                            current_card_color = card(current_card)[0]

                            current_card_index = colors_dict[current_card_color]

                            # Remove the drawn card from the deck
                            del deck_ints[len(deck_ints) - 1]

                            # Add the drawn card to the player's double list
                            player_double_list[current_card_index].append(current_card)

                            # If the drawn card can be played, stop drawing from the deck
                            if current_card_index in legal_indices_list(player_double_list, deck_ints, discard_pile_ints):
                                keep_drawing = False

                        else:

                            keep_drawing = False


        elif event.type == pygame.QUIT:                 # Quit

            running = False

    if len(deck) == 0 and len(discard_pile) > 1:

        deck_ints = shuffle_pile_ints(discard_pile_ints[0:len(discard_pile_ints) - 1], seed)

        for i in range(len(deck_ints)):

            if card(deck_ints[i])[0:2] == "wc":  # Strip color from wild cards

                deck_ints[i] = 101

            elif card(deck_ints[i])[0:2] == "wp":

                deck_ints[i] = 105

        print("deck = ", int_list_to_cards(deck_ints))

        discard_pile_ints = [discard_pile_ints[len(discard_pile_ints) - 1]]

        print("discard pile = ", int_list_to_cards(discard_pile_ints))



    pygame.display.update()
