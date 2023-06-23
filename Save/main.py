import pygame, os, sys
from random import choice as ch
from player import *
from colorMap import *
from menus import *
from mazeMap import *
from AstarNonDiagonal import *

sys.setrecursionlimit(15000)
# TODO ability to adjust coefficient, also make it automatic and color delay adjustment, add soemthing that tells you color distances for color type 2, adjust colors for color type 2, add sprites for start + end (size of 64)
NOTHING = 0
WALL = 1
PLAYER = 4
START = 5
END = 6
PATH = 8
TEMPORARYWALL = 9


def redrawMap(map, SIZE, originalSize, path, solution, gamedisplay):
    for y in range(0, len(map.map)):
        for x in range(0, len(map.map[y])):
            if map.map[y, x] not in [WALL, NOTHING]:
                values = {START: (0, 255, 0), END: (255, 0, 0)}
                pygame.draw.rect(gamedisplay, values[map.map[y, x]],
                                 pygame.Rect(SIZE * x, SIZE * y, originalSize, originalSize))

    if solution:
        for coord in path:
            if coord not in [map.start, map.end]:
                # (33, 111, 255)
                pygame.draw.rect(gamedisplay, (0,0,0),
                                 pygame.Rect(SIZE * coord[1], SIZE * coord[0], originalSize, originalSize))


if __name__ == '__main__':

    # Controls :
    # 'r' - shows you the solution of the maze
    # 'z' - shows you the distances certain parts of the maze are away from you (Darker = farther away except for pink which is the farthest away)
    # WASD to control character who is purple in color

    # Higher = Faster (Default is 20)
    player_speed = 20
    # Size of the pixels in the maze (the smaller the size the more you can fit meaning a larger maze)
    SIZE = 20

    solution = False
    colorize = False
    display = True
    borderless = True
    fullscreen = True
    move = False

    # Titles the game
    pygame.display.set_caption('Maze')
    clock = pygame.time.Clock()
    # For right now I will keep width and height at 1000 x 560 but we can change it later
    if fullscreen:
        WIDTH = 1920
        HEIGHT = 1080
    else:
        WIDTH = 1000
        HEIGHT = 560

    colorType = 0
    if move:
        x = 1920
        y = 30
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
    if fullscreen:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT))
    gameRunning = True
    pathToFinish = None
    start = time.time()
    map = Maze(HEIGHT, WIDTH, SIZE, gamedisplay, display, borderless)
    print("Maze time:", time.time() - start)
    start = time.time()
    coloredMap = ColorMap(map, SIZE, borderless)
    coloredPoints, coloredPointsGroup = coloredMap.getPoints()
    print("Color time:", time.time() - start)

    originalSize = SIZE

    if not borderless:
        SIZE += 1

    player = Player(map.start[1], map.start[0], SIZE, borderless)

    while gameRunning:
        clock.tick(player_speed)
        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    if solution:
                        solution = False
                    else:
                        algorithm = Astar(map.map, False, (player.x, player.y))
                        pathToFinish = algorithm.getFinalPath()
                        solution = True
                elif e.key == pygame.K_z:
                    if colorize:
                        colorize = False
                    else:
                        colorize = True
                        slowColorDraw(SIZE, originalSize, coloredPoints, gamedisplay, colorType)
                    coloredPointsGroup.update(colorize, colorType)
                elif e.key == pygame.K_ESCAPE:
                    colorType = pauseMenu(colorType)
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = e.pos
                pointsClicked = coloredPointsGroup.get_sprites_at((mousex, mousey))
                if len(pointsClicked) > 0:
                    print(len(pointsClicked[0].path) - 1, pointsClicked[0].coords)

        # Clearing the display
        gamedisplay.fill((0, 0, 0))

        # Update Player
        player.update(map.map)

        # Drawing to the screen
        coloredPointsGroup.draw(gamedisplay)
        redrawMap(map, SIZE, originalSize, pathToFinish, solution, gamedisplay)
        map.walls.draw(gamedisplay)
        gamedisplay.blit(player.image, player.rect)

        # Updating the display
        pygame.display.update()
