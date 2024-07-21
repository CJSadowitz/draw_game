import pygame

from menus.auto_aspr import Screen

def lan_lobby_screen(Screen):
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
        
        back_button = Screen.menu_button_rect((127, 25, 255),     (0.05, 0.1, 0.2, 0.2))
        if (pygame.mouse.get_just_released()[0]):
            if (back_button):
                running = False
                return "lan"
        pygame.display.update()
    return "main_menu"