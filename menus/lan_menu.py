import pygame

from menus.auto_aspr import Screen

def lan_screen(Screen):
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
        host_button = Screen.menu_button_rect((0, 255, 0),     (0.05, 0.6, 0.4, 0.7))
        connect_button = Screen.menu_button_rect((96, 102, 2), (0.05, 0.35, 0.4, 0.45))
        back_button = Screen.menu_button_rect((0, 0, 255),     (0.05, 0.1, 0.2, 0.2))
        if (pygame.mouse.get_just_released()[0]):
            if (host_button):
                running = False
                return "host" # exit menu logic 
            if (connect_button):
                running = False
                return "connect" # exit menu logic
            if (back_button):
                running = False
                return "play"
        pygame.display.update()
    return "main_menu"