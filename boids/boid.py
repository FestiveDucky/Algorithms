import pygame.sprite
import math
import random


def calculateNewCoords(coords, speed, angle_in_degrees):
    coords = tuple(map(lambda x: round(x, 5), coords))
    new_x = coords[1] + (speed * math.cos(math.radians(angle_in_degrees)))
    new_y = coords[0] + (speed * math.sin(math.radians(angle_in_degrees)))
    return new_y, new_x


def reverseAngle(coords1, coords2):
    coords1 = tuple(map(lambda x: round(x, 5), coords1))
    coords2 = tuple(map(lambda x: round(x, 5), coords2))
    if coords2[1] - coords1[1] == 0:
        if coords2[0]-coords1[0] > 0:
            return 90
        else:
            return 270
    elif coords2[0]-coords1[0] == 0:
        if coords2[1]-coords1[1] > 0:
            return 0
        else:
            return 180

    return math.degrees(math.atan((coords2[0]-coords1[0])/(coords2[1] - coords1[1])))


class Boid(pygame.sprite.Sprite):
    def __init__(self, group, coords, angle, scale):
        super().__init__(group)

        self.coords = coords
        self.neighbors = []
        self.decimal_coords = coords
        self.angle = angle
        self.average = 0
        self.image = pygame.Surface((scale, scale))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(x=self.coords[1], y=self.coords[0] * scale)

    def move(self, height, length):
        # print(self.angle)
        next_decimal_coords = calculateNewCoords(self.decimal_coords, 0.5, self.angle)
        next_coords = tuple(map(round, next_decimal_coords))

        angle_of_change = 20

        if height <= next_coords[0] or next_coords[0] <= -1 or -1 >= next_coords[1] or next_coords[1] >= length:
            if height <= next_coords[0] or next_coords[0] <= -1:
                self.angle = 360 - self.angle + random.randint(-angle_of_change, angle_of_change)
            if -1 >= next_coords[1] or next_coords[1] >= length:
                self.angle = 180 - self.angle + random.randint(-angle_of_change, angle_of_change)

            if self.angle < 0:
                self.angle = 0
            elif self.angle >= 360:
                self.angle -= 360
            return self.move(height, length)

        self.decimal_coords = next_decimal_coords
        self.coords = next_coords
        self.rect.x = next_coords[1]
        self.rect.y = next_coords[0]

        # new angle
        if len(self.neighbors) > 0:
            # self.angle = (self.average + self.angle) / (len(self.neighbors) + 1)
            self.angle = ((self.average / len(self.neighbors)) + self.angle) / 2

        self.neighbors = []
        self.average = 0

    def update(self, HEIGHT, LENGTH):
        self.move(HEIGHT, LENGTH)


class BoidGroup:
    def __init__(self, cm):
        self.center_of_mass = cm
        self.boids = []

