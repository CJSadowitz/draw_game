from Screen import Screen        # Draws black background & toggles fullscreen
from Button import Button       # Mouse clicks press Button objects

import pygame                   # Get pygame events


def check_events():

    pygame.display.flip()
    Screen.window.fill((0, 0, 0))               # Draw the black background every frame

    running = True                              # Kills the game loop in main when set to False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:           # Quit the game loop in main
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_F11:       # F11 to toggle fullscreen
                Screen.toggle_fullscreen()

    if pygame.mouse.get_just_released()[0]:           # Mouse click attempts to press all Button objects in current game state
        Button.attempt_pressing_all_buttons()

    return running
