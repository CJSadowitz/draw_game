import pygame

from menus.auto_aspr import Screen

def title_screen():
    Screen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    Screen.toggle_fullscreen()
        Screen.draw_rect((0, 0, 0), (0, 0, 1, 1))
        Screen.draw_rect((255,0,0), (0.25, 0.25, 0.75, 0.75))
        pygame.display.update()
    pass