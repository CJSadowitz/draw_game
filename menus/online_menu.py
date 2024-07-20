import pygame

from menus.auto_aspr import Screen

def online_screen(Screen):
    running = True
    while running:
        Screen.draw_rect((10, 10, 10), (0, 0, 1, 1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    Screen.toggle_fullscreen()
        matchmaking_button = Screen.menu_button_rect((0, 255, 50), (0.05, 0.6, 0.4, 0.7))
        private_button = Screen.menu_button_rect((125, 25, 59),   (0.05, 0.35, 0.4, 0.45))
        back_button = Screen.menu_button_rect((0, 0, 255),   (0.05, 0.1, 0.2, 0.2))
        if (pygame.mouse.get_just_released()[0]):
            if (matchmaking_button):
                running = False
                return "quit" # Exit menu logic goes here
            if (private_button):
                running = False
                return "quit" # Exit menu logic goes here
            if (back_button):
                running = False
                return "play"
        pygame.display.update()
    return "main_menu"