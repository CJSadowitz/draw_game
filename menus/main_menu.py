import pygame


def title_screen(Screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    Screen.toggle_fullscreen()
        # Play_button
        play_button = Screen.menu_button_rect((255, 0, 0), (0.25, 0.25, 0.75, 0.75))
        if (pygame.mouse.get_just_released()[0]):
            if (play_button):
                # Logic for selecting different menus
                running = False
                return "play"

        pygame.display.update()
    return "main_menu"


