import pygame

from menus.auto_aspr import Screen

def play_options_screen(Screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    Screen.toggle_fullscreen()
        online_button = Screen.menu_button_rect((0, 255, 0), (0.25, 0.25, 0.75, 0.75))
        back_button = Screen.menu_button_rect((0, 0, 255), (0.1, 0.1, 0.2, 0.2))
        if (pygame.mouse.get_just_released()[0]):
            if (online_button):
                # Logic for selecting different menus
                running = False
                return "online"
            if (back_button):
                running = False
                return "main_menu"
        pygame.display.update()
    return "main_menu"