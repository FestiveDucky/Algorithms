import pygame, os, sys
from random import choice as ch
from player import *
from colorMap import *
from menus import *
from victory import *
from mazeMap import *
from AstarNonDiagonal import *
# TODO add timer, add hunter
# TODO LATER add ability to click on point for more info and also to find fastest route to that point

# Constants
NOTHING = 0
WALL = 1
PLAYER = 4
START = 5
END = 6
PATH = 8
TEMPORARYWALL = 9


def redrawMap(map, SIZE, originalSize, path, solution, gamedisplay, darkMode, colorize):
    """redrawMap() -> Draws the start, end and empty spaces"""
    for y in range(0, len(map.map)):
        for x in range(0, len(map.map[y])):
            if not darkMode or colorize:
                exclusion = [WALL, NOTHING]
            else:
                exclusion = [WALL]
            if map.map[y, x] not in exclusion:
                values = {START: (0, 255, 0), END: (255, 0, 0), NOTHING: (75, 75, 75)}
                pygame.draw.rect(gamedisplay, values[map.map[y, x]],
                                 pygame.Rect(SIZE * x, SIZE * y, originalSize, originalSize))

    if solution:
        for coord in path:
            if coord not in [map.start, map.end]:
                # (33, 111, 255)
                if not darkMode:
                    color = (50, 50, 50)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(gamedisplay, color,
                                 pygame.Rect(SIZE * coord[1], SIZE * coord[0], originalSize, originalSize))


def grabBoolean(file):
    """grabBoolean() -> gets a boolean from a setting in a txt file"""
    return {"true": True, "false": False}[file.readline().strip().split()[-1].lower()]


if __name__ == '__main__':
    # Grab the settings from the file
    with open("settings.txt", "r") as f:
        SIZE = int(f.readline().strip().split()[-1])
        player_speed = int(f.readline().strip().split()[-1])
        darkMode = grabBoolean(f)
        fastMode = grabBoolean(f)
        fullscreen = grabBoolean(f)
        cheats = grabBoolean(f)

    solution = False
    colorize = False
    display = True
    borderless = True
    miniScreen = False
    move = False

    # Titles the game
    pygame.display.set_caption('Maze Practice')
    clock = pygame.time.Clock()
    # Screen size settings
    if fullscreen:
        WIDTH = 1920
        HEIGHT = 1080
    elif miniScreen:
        WIDTH = 1000
        HEIGHT = 560
    else:
        WIDTH = 1920
        HEIGHT = 1050

    colorType = 0
    # Moves the screen if requested
    if move:
        x = 1920
        y = 30
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    # Sets the game to fullscreen if requested
    if fullscreen:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT))

    gameRunning = True
    pathToFinish = None
    start = time.time()
    map = Maze(HEIGHT, WIDTH, SIZE, gamedisplay, display, borderless, darkMode)
    print("Maze time:", time.time() - start)
    # Doesn't do a color map if fast load is enabled
    if not fastMode:
        start = time.time()
        coloredMap = ColorMap(map, SIZE, borderless)
        coloredPoints, coloredPointsGroup = coloredMap.getPoints()
        print("Color time:", time.time() - start)

    originalSize = SIZE

    if not borderless:
        SIZE += 1

    # Creates the player character
    player = Player(map.start[1], map.start[0], SIZE, borderless)

    # Starts the game loop
    while gameRunning:
        # Tick speed
        clock.tick(player_speed)

        # Checking events
        events = pygame.event.get()
        for e in events:
            # If you close the game
            if e.type == pygame.QUIT:
                gameRunning = False

            if e.type == pygame.KEYDOWN:
                # Shows the path to the end
                if e.key == pygame.K_r and cheats:
                    if solution:
                        solution = False
                    else:
                        algorithm = Astar(map.map, False, (player.x, player.y))
                        pathToFinish = algorithm.getFinalPath()
                        solution = True
                # Shows the color map
                elif e.key == pygame.K_z and not fastMode and cheats:
                    if colorize:
                        colorize = False
                    else:
                        colorize = True
                        slowColorDraw(SIZE, originalSize, coloredPoints, gamedisplay, colorType)
                    coloredPointsGroup.update(colorize, colorType)
                # Pauses the game
                elif e.key == pygame.K_ESCAPE:
                    colorType = pauseMenu(colorType)
            # Gives info if you click on a point
            elif e.type == pygame.MOUSEBUTTONDOWN and not fastMode:
                mousex, mousey = e.pos
                pointsClicked = coloredPointsGroup.get_sprites_at((mousex, mousey))
                if len(pointsClicked) > 0:
                    print(len(pointsClicked[0].path) - 1, pointsClicked[0].coords)

        # Clearing the display
        gamedisplay.fill((0, 0, 0))

        # Update Player
        player.update(map.map)

        # Drawing to the screen
        if not fastMode:
            coloredPointsGroup.draw(gamedisplay)
        redrawMap(map, SIZE, originalSize, pathToFinish, solution, gamedisplay, darkMode, colorize)
        map.walls.draw(gamedisplay)
        gamedisplay.blit(player.image, player.rect)

        # Updating the display
        pygame.display.update()

        # Checks if the player has won
        if (player.y, player.x) == map.end:
            victoryMenu()
            gameRunning = False
