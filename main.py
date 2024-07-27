"""
Game loop. Calls appropriate networking engine, and display functions
"""
import pygame
import threading
import time

from lan.client import Client
from lan.server import Server
from Button import Button
from State import State
from Events import check_events
from Screen import Screen

def main():

    # PROGRAM:DRAW (v1.0; July 2024)
    # Brendan Brooks, Dawson Hawk, Colin Sadowitz, Carter Scott

    Screen()
    State()

    Button(
        game_state="bouncing_draw_logo",

        center_coords_tuple=(0, 0.125),
        height=0.125,
        w_h_ratio=4,

        four_colors_list=[(255, 0, 255), (255, 255, 255), None, None],
        text="      Host      ", text_four_colors_list=[(0, 0, 0), (255, 0, 255), None, None],

        set_game_state_to="host",
    )

    Button(
        game_state="bouncing_draw_logo",

        center_coords_tuple=(0, -0.125),
        height=0.125,
        w_h_ratio=4,

        four_colors_list=[(0, 255, 0), (255, 255, 255), None, None],
        text="    Connect    ", text_four_colors_list=[(0, 0, 0), (0, 255, 0), None, None],

        set_game_state_to="connect"
    )

    Button(
        game_state="host",

        center_coords_tuple=(0, -0.375),
        height=0.125,
        w_h_ratio=3,

        four_colors_list=[(100, 100, 100), (255, 255, 255), None, None],
        text="    Back    ", text_four_colors_list=[(0, 0, 0), (0, 0, 255), None, None],

        set_game_state_to="bouncing_draw_logo",
    )

    Button(
        game_state="connect",

        center_coords_tuple=(0, -0.375),
        height=0.125,
        w_h_ratio=3,

        four_colors_list=[(100, 100, 100), (255, 255, 255), None, None],
        text="    Back    ", text_four_colors_list=[(0, 0, 0), (0, 0, 255), None, None],

        set_game_state_to="bouncing_draw_logo"
    )


    # Game LOOP :D

    while check_events():

        State.run_current_game_state()

        Button.draw_all_buttons()

if __name__ == "__main__":
    main()
    