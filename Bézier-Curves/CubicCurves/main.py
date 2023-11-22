import pygame, os, sys, time, pygame.gfxdraw, ctypes
from drawing import *
from random import randint as ri


if __name__ == '__main__':
    pygame.init()

    fullscreen = True
    move = False

    # Titles the game
    pygame.display.set_caption('Bézier Curves')
    clock = pygame.time.Clock()

    if fullscreen:
        ctypes.windll.user32.SetProcessDPIAware()
        WIDTH = 2880
        HEIGHT = 1800
        # WIDTH = 1920
        # HEIGHT = 1080
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

    precision = 120
    # speed = 0
    speed = 0.005
    show_segments = False
    show_mid_line = False
    draw_lerps = False
    draw_curve = True
    draw_points = False
    draw_circle = False
    new_draw_type = False
    draw_vectors = False
    draw_bounding_boxes = False
    allign_segments = False
    miror_segments = False
    hide_points = False

    points = [(WIDTH//2, HEIGHT//2), (ri(100, WIDTH - 200), ri(100, HEIGHT - 100)),
              (ri(100, WIDTH - 200), ri(100, HEIGHT - 100)), (ri(100, WIDTH - 200), ri(100, HEIGHT - 100))]
    c = Curve(points, gamedisplay, precision)

    gamedisplay.fill((14, 25, 36))
    values = [draw_lerps, show_segments, show_mid_line, draw_points, draw_curve, draw_circle, draw_vectors, draw_bounding_boxes, new_draw_type, allign_segments, miror_segments ,hide_points]
    menu = Menu(gamedisplay, WIDTH, HEIGHT, values)
    menu.draw()

    c.draw(draw_points, draw_curve, False, 0, False, show_segments, show_mid_line, False, draw_bounding_boxes, hide_points)
    c.updatePoints()

    pygame.display.update()

    FPS = 20
    gameRunning = True

    infinite_curve = Curve(points, gamedisplay, precision)
    moving_point = None

    while gameRunning:
        clock.tick(FPS)

        update = False

        # Checking events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = e.pos

                pointsClicked = c.getPointsClicked(mousex, mousey)
                if len(pointsClicked) > 0:
                    pointsClicked[0].selected = True
                    moving_point = pointsClicked[0]

                buttonsClicked = menu.button_group.get_sprites_at((mousex, mousey))
                if len(buttonsClicked) > 0:
                    buttonsClicked[0].pressed()
                    values = menu.getValues()
                    draw_lerps, show_segments, show_mid_line, draw_points, draw_curve, draw_circle, draw_vectors, draw_bounding_boxes, new_draw_type, allign_segments, miror_segments, hide_points = values

                    if miror_segments and buttonsClicked[0] == menu.buttons[10]:
                        allign_segments = False
                        menu.buttons[9].set(False)
                    elif allign_segments:
                        miror_segments = False
                        menu.buttons[10].set(False)

                    update = True

            elif e.type == pygame.MOUSEMOTION:
                mousex, mousey = e.pos
                if moving_point is not None:
                    if mousex > WIDTH - 200:
                        mousex = WIDTH - 200
                    old_pos = moving_point.getCoords()
                    vector = (mousex - old_pos[0], mousey - old_pos[1])
                    moving_point.setCoords((mousex, mousey))

                    if allign_segments:
                        c.allignSegments(moving_point, vector)

                    if miror_segments:
                        c.allignSegments(moving_point, vector, True)

                    update = c.setPoints()
            elif e.type == pygame.MOUSEBUTTONUP:
                if moving_point is not None:
                    moving_point.selected = False
                    moving_point = None
                if not hide_points:
                    c.updatePoints()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    if new_draw_type:
                        c.draw2(draw_points, draw_curve, draw_lerps, speed, draw_circle, draw_vectors, hide_points)
                    else:
                        c.draw(draw_points, draw_curve, draw_lerps, speed, draw_circle, show_segments, show_mid_line, draw_vectors, draw_bounding_boxes, hide_points)
                    update = True
                elif e.key == pygame.K_p:
                    c.addCurve(
                        [(ri(100, WIDTH - 200), ri(100, HEIGHT - 100)), (ri(100, WIDTH - 200), ri(100, HEIGHT - 100)),
                         (ri(100, WIDTH - 200), ri(100, HEIGHT - 100))])
                    update = True
                elif e.key == pygame.K_r:
                    c.removeCurve()
                    update = True
                elif e.key == pygame.K_UP:
                    speed += 0.01
                elif e.key == pygame.K_DOWN and speed > 0.01:
                    speed -= 0.01
                elif e.key == pygame.K_i:
                    infinite_curve.start(menu, WIDTH, HEIGHT, values)

                    # Set new values
                    values = menu.getValues()
                    draw_lerps, show_segments, show_mid_line, draw_points, draw_curve, draw_circle, draw_vectors, draw_bounding_boxes, new_draw_type, allign_segments, miror_segments, hide_points = values

                    update = True

        # Drawing to the screen
        if update:
            gamedisplay.fill((14, 25, 36))
            menu.draw()
            c.draw(draw_points, draw_curve, False, 0, False, show_segments, show_mid_line, False, draw_bounding_boxes, hide_points)
            if not hide_points:
                c.updatePoints()

        # Updating the display
        pygame.display.update()
