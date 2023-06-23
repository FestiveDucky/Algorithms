import os
import time

from screen import *

# TODO add a follow mechanism and add cooler color stuff


def tick():
    # start = time.time()
    screen.move()
    # print(f"Move Time - {time.time() - start}")

    # start = time.time()
    screen.average()
    # print(f"Blur Time - {time.time() - start}")


    # time.sleep(1)


if __name__ == '__main__':
    pygame.init()

    fullscreen = True
    raspberrypi = False
    move = False
    agents = 4000
    scale = 8

    pygame.display.set_caption("Slime Simulation")
    clock = pygame.time.Clock()

    if move:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{1920},{30}"
    if not raspberrypi:

        if fullscreen:

            LENGTH = 1920
            HEIGHT = 1080
            gamedisplay = pygame.display.set_mode((LENGTH, HEIGHT), pygame.FULLSCREEN)
        else:

            LENGTH = 1000
            HEIGHT = 560
            gamedisplay = pygame.display.set_mode((LENGTH, HEIGHT))
    else:

        LENGTH = 800
        HEIGHT = 480
        gamedisplay = pygame.display.set_mode((LENGTH, HEIGHT))
        # gamedisplay = pygame.display.set_mode((LENGTH, HEIGHT), pygame.FULLSCREEN)

    color_decrease = 0
    speed = 1
    FPS = 600
    # 40
    gameRunning = True

    screen = Screen(agents, LENGTH, HEIGHT, scale, speed, gamedisplay)
    mousePressed = False

    while gameRunning:
        clock.tick_busy_loop(FPS)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
            elif e.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
                # mousex, mousey = e.pos
                # pointsClicked = screen.tile_group.get_sprites_at((mousex, mousey))
                # if len(pointsClicked) > 0:
                #     screen.board[pointsClicked[0].coords[0]][pointsClicked[0].coords[1]] = 1
            # elif e.type == pygame.MOUSEMOTION:
            #     if mousePressed:
            #         mousex, mousey = e.pos
            #         pointsClicked = screen.tile_group.get_sprites_at((mousex, mousey))
            #         if len(pointsClicked) > 0:
            #             screen.board[pointsClicked[0].coords[0]][pointsClicked[0].coords[1]] = 1
            elif e.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    if screen.following is None:
                        screen.following = 0
                    else:
                        screen.following -= 1
                        if screen.following < 0:
                            screen.following = agents-1
                elif keys[pygame.K_RIGHT]:
                    if screen.following is None:
                        screen.following = 0
                    else:
                        screen.following += 1
                        if screen.following > agents-1:
                            screen.following = 0
                elif keys[pygame.K_SPACE]:
                    screen.following = None

        if mousePressed:
            mousex, mousey = pygame.mouse.get_pos()
            pointsClicked = screen.tile_group.get_sprites_at((mousex, mousey))
            if len(pointsClicked) > 0:
                screen.board[pointsClicked[0].coords[0]][pointsClicked[0].coords[1]] = 1

        start = time.time()
        # Update Tick
        tick()

        print(f"Time - {time.time() - start}")
        # Renewing the display
        pygame.display.update()
        # gamedisplay.fill((0, 0, 0))
    pygame.quit()