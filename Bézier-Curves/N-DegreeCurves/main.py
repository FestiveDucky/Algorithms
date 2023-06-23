import pygame, os, sys, time, pygame.gfxdraw
from drawing import *
from random import randint as ri

sys.setrecursionlimit(15000)

# Add seperate drawer, add color change for different points and distances, add circle based of curvature

# Create menu, for curve editor (has ability to add/remove points and move points), infintie curve (generates curve infinitely), infinite curve with curvature circles, infinite curve with bounding boxes
if __name__ == '__main__':
    fullscreen = True
    move = False

    # Titles the game
    pygame.display.set_caption('Bézier Curves')
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

    precision = 200
    speed = 0.02

    points = [(100, 100), (200, 50), (300, 200), (200, 250)]
    cbc = BezierCurve(points, gamedisplay)

    cbc.calculateBezierCurve(30, False, True, False, 0, False)
    cbc.point_group.update(gamedisplay)

    pygame.display.update()

    FPS = 20
    gameRunning = True
    moving_point = None

    while gameRunning:
        clock.tick(FPS)
        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = e.pos
                pointsClicked = cbc.point_group.get_sprites_at((mousex, mousey))
                if len(pointsClicked) > 0:
                    pointsClicked[0].selected = True
                    moving_point = pointsClicked[0]
            elif e.type == pygame.MOUSEMOTION:
                mousex, mousey = e.pos
                if moving_point is not None:
                    moving_point.setCoords((mousex, mousey))
            elif e.type == pygame.MOUSEBUTTONUP:
                if moving_point is not None:
                    moving_point.selected = False
                    moving_point = None
                cbc.point_group.update(gamedisplay)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    cbc.calculateBezierCurve(precision, False, True, True, speed, False)
                    gamedisplay.fill((0, 0, 0))
                    cbc.calculateBezierCurve(precision, False, True, False, 0, False)
                    cbc.point_group.update(gamedisplay)
                elif e.key == pygame.K_c:
                    cbc.calculateBezierCurve(precision, False, True, True, speed, True)
                    gamedisplay.fill((0, 0, 0))
                    cbc.calculateBezierCurve(precision, False, True, False, 0, False)
                    cbc.point_group.update(gamedisplay)
                elif e.key == pygame.K_p:
                    cbc.addPoint((ri(100, WIDTH - 100), ri(100, HEIGHT - 100)))
                elif e.key == pygame.K_r:
                    cbc.removePoint()
                elif e.key == pygame.K_UP:
                    speed += 0.01
                elif e.key == pygame.K_DOWN and speed > 0.01:
                    speed -= 0.01

        # Changes
        update = cbc.setNewPoints()

        # Drawing to the screen
        if update:
            gamedisplay.fill((0, 0, 0))
            cbc.calculateBezierCurve(precision, False, True, False, 0, False)
            cbc.point_group.update(gamedisplay)

        # Updating the display
        pygame.display.update()
