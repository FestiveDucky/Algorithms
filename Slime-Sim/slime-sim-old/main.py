import os
from screen import *

# TODO add any tile next to a colored tile to the active tiles, make an option for agents not remove each other, color agents, MAKE FASTER


def tick():
    start = time.time()
    screen.average(color_decrease)
    print(f"Blur Time - {time.time() - start}")

    start = time.time()
    screen.move()
    print(f"Move Time - {time.time() - start}")
    # time.sleep(1)


if __name__ == '__main__':
    pygame.init()

    fullscreen = False
    raspberrypi = False
    move = False
    agents = 1
    scale = 10

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
    speed = 1000
    FPS = 400
    # 40

    gameRunning = True

    screen = Screen(agents, LENGTH, HEIGHT, scale, speed)
    tiles = screen.getTiles()

    while gameRunning:
        clock.tick(FPS)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False

            # elif e.type == pygame.KEYDOWN:
            #     keys = pygame.key.get_pressed()
            #     if keys[pygame.K_SPACE]:
            #         screen.average()
            #     elif keys[pygame.K_w]:
            #         screen.decrease(color_decrease)

        start = time.time()
        # Update Tick
        tick()

        # Drawing to screen
        active_coords = screen.getActiveCoords()
        for coords in active_coords:
            gamedisplay.blit(tiles[coords].image, tiles[coords].rect)

        print(f"Time - {time.time() - start}")
        # Renewing the display
        pygame.display.update()
        gamedisplay.fill((0, 0, 0))
    pygame.quit()