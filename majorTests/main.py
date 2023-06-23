import pygame, os, sys, time
from random import choice as ch
from poissicDisc import *

sys.setrecursionlimit(15000)


def redrawMap(points, SIZE, gamedisplay):
    for point in points:
        pygame.draw.circle(gamedisplay, (255, 255, 255), (point[1], point[0]), SIZE)


if __name__ == '__main__':

    solution = False
    fullscreen = False
    move = False

    # Titles the game
    pygame.display.set_caption('Sampling')
    clock = pygame.time.Clock()

    if fullscreen:
        WIDTH = 1920
        HEIGHT = 1080
    else:
        WIDTH = 1000
        HEIGHT = 560

    pointRadius = 1
    innerCircleRadius = 5
    outerCircleRadius = 10
    candidateSamples = 10000

    if move:
        x = 1920
        y = 30
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    if fullscreen:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT))

    start = time.time()
    sampling = Sampling(WIDTH, HEIGHT, candidateSamples, innerCircleRadius, outerCircleRadius, gamedisplay, pointRadius)
    points = sampling.getPoints()
    print(f"Time: {time.time() - start}")
    # 222.17 (10)
    # 108.41 (5)



    FPS = 20
    gameRunning = True

    while gameRunning:
        clock.tick(FPS)
        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False

        # Clearing the display
        gamedisplay.fill((0, 0, 0))

        # Drawing to the screen
        redrawMap(points, pointRadius, gamedisplay)

        # Updating the display
        pygame.display.update()
