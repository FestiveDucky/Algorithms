import pygame, os, sys, time, cv2
from random import choice as ch
from poissicDisc import *

sys.setrecursionlimit(15000)


def redrawMap(points, SIZE, thickness, gamedisplay):
    for point in points:
        pygame.draw.circle(gamedisplay, (255, 255, 255), (point[1], point[0]), SIZE, thickness)


# TODO add image export
if __name__ == '__main__':
    run_voronoi = True
    load_image = True
    fullscreen = True
    move = True

    if load_image:
        image = cv2.imread("Screenshot_1.png")
        print(image.shape)
    else:
        image = None

    # Titles the game
    pygame.display.set_caption('Sampling')
    clock = pygame.time.Clock()

    if fullscreen:
        WIDTH = 1920
        HEIGHT = 1080
    else:
        WIDTH = 1001
        HEIGHT = 560

    start_center = True

    pointRadius = 2
    thickness = 2
    innerCircleRadius = 3
    outerCircleRadius = 4
    candidateSamples = 10
    border_point_radius = 80
    border_points = None
    draw_border_points = False
    starting_points = None
    display_sampling = False
    draw_sampling = True
    color_sampling = False

    if move:
        x = 1920
        y = 30
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

    if fullscreen:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        gamedisplay = pygame.display.set_mode((WIDTH, HEIGHT))

    start = time.time()
    sampling = Sampling(0, 0, WIDTH, HEIGHT, candidateSamples, innerCircleRadius, outerCircleRadius, thickness,
                        pointRadius, gamedisplay, display_sampling, border_points, starting_points, start_center,
                        border_point_radius, draw_sampling, image, color_sampling)
    points = sampling.getPoints()
    # print(f"Time: {time.time() - start}")

    # temp
    sampling.draw(None, True)
    if draw_border_points:
        for point in border_points:
            pygame.draw.circle(gamedisplay, (0, 0, 255), (point[0], point[1]), border_point_radius, 3)

    if run_voronoi:
        sampling.voronoiDiagram()

    FPS = 20
    gameRunning = True

    while gameRunning:
        clock.tick(FPS)
        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False

        """# Clearing the display
        gamedisplay.fill((0, 0, 0))

        # Drawing to the screen
        sampling.draw(None, True)
        if draw_border_points:
            for point in border_points:
                pygame.draw.circle(gamedisplay, (0, 0, 255), (point[0], point[1]), border_point_radius, 3)
        # redrawMap(points, pointRadius, thickness, gamedisplay)

        # Updating the display
        pygame.display.update()"""
