import math
import os, time
from boid import *

# TODO Instead of getting average angle of neighboring boids, get your angle too them and get the average of that so that you move towards them not in the same direction as them, also if too close add negative angle


def getNeighbors(b):
    for i in range(len(b)):
        for j in range(i, len(b)):
            # distance between boids
            dis = math.dist(b[i].coords, b[j].coords)
            # if within distance and in front of boid
            det = 30
            if det >= dis > math.dist(b[j].coords, calculateNewCoords(b[i].coords, dis, b[i].angle)) > 0:
                b[i].neighbors.append((b[j], dis))
                b[i].average += reverseAngle(b[i].coords, b[j].coords)
                # b[i].average += b[j].angle
            if det >= dis > math.dist(b[i].coords, calculateNewCoords(b[j].coords, dis, b[j].angle)) > 0:
                b[j].neighbors.append((b[i], dis))
                b[j].average += reverseAngle(b[j].coords, b[i].coords)
                # b[j].average += b[i].angle


if __name__ == '__main__':
    pygame.init()

    fullscreen = False
    move = False

    boids = 100
    scale = 10

    pygame.display.set_caption("Boid Simulation")
    clock = pygame.time.Clock()

    if move:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{1920},{30}"
    if fullscreen:
        LENGTH = 1920
        HEIGHT = 1080
        gamedisplay = pygame.display.set_mode((LENGTH, HEIGHT), pygame.FULLSCREEN)
    else:
        LENGTH = 1000
        HEIGHT = 560
        gamedisplay = pygame.display.set_mode((LENGTH, HEIGHT))

    FPS = 400
    # 40

    gameRunning = True

    boids_group = pygame.sprite.Group()
    boids_list = [Boid(boids_group, (200, 200), random.randint(0, 359), scale) for x in range(boids)]

    while gameRunning:
        clock.tick(FPS)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                gameRunning = False
        start = time.time()

        # Update Tick
        boids_group.update(HEIGHT, LENGTH)
        getNeighbors(boids_list)

        # Drawing to screen
        boids_group.draw(gamedisplay)

        # print(f"Time - {time.time() - start}")
        # Renewing the display
        pygame.display.update()
        gamedisplay.fill((0, 0, 0))
    pygame.quit()