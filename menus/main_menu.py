import pygame


def title_screen(Screen):
    running = True
    while running:
        Screen.draw_rect((0, 0, 0), (0, 0, 1, 1))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    Screen.toggle_fullscreen()
        # Play_button
        play_button = Screen.menu_button_rect((255, 0, 0),       (0.05, 0.6, 0.4, 0.7))
        settings_button = Screen.menu_button_rect((255, 0, 255), (0.05, 0.35, 0.4, 0.45))
        quit_button = Screen.menu_button_rect((255, 255, 255),   (0.05, 0.1, 0.2, 0.2))
        if (pygame.mouse.get_just_released()[0]):
            if (play_button):
                running = False
                return "play"
            if (quit_button):
                running = False
                return "quit"
            if (settings_button):
                running = False
                return "settings"

        pygame.display.update()
    return "main_menu"


