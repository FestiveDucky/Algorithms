import os
import time

import pygame.sprite

from button import *


if __name__ == '__main__':
    pygame.init()

    fullscreen = False
    move = False

    # Titles the game
    pygame.display.set_caption('Button test')
    clock = pygame.time.Clock()

    if fullscreen:
        WIDTH = 1920
        HEIGHT = 1080
    else:
        WIDTH = 1001
        HEIGHT = 560
    if move:
        x = 1920
        y = 30
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    if fullscreen:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT))

    gamedisplay.fill((14, 25, 36))

    test_class = pygame.sprite.LayeredUpdates()
    b = Button(test_class, gamedisplay, "Draw curve", (WIDTH / 2, HEIGHT / 2))

    b.draw()
    pygame.display.update()

    FPS = 20
    gameRunning = True
    while gameRunning:
        clock.tick(FPS)

        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = e.pos
                buttons = test_class.get_sprites_at((mousex, mousey))
                if len(buttons) != 0:
                    buttons[0].pressed()
