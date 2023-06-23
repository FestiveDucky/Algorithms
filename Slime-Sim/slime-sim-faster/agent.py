import datetime
import time

import pygame, math, random


def calculateNewCoords(coords, speed, angle_in_degrees):
    coords = (round(coords[0], 5), round(coords[1], 5))
    # coords = tuple(map(lambda x: round(x, 5), coords))
    new_x = coords[1] + (speed*math.cos(math.radians(angle_in_degrees)))
    new_y = coords[0] + (speed*math.sin(math.radians(angle_in_degrees)))
    return new_y, new_x


class Agent(pygame.sprite.Sprite):
    def __init__(self, group, coords, speed):
        super().__init__(group)
        self.coords = coords
        self.trigCoords = coords
        self.speed = speed
        self.angle = random.randint(1, 360)

    def adjust(self, screen):
        values = []
        n = 0
        # angles = [-40, -20, 0, 20, 40]
        angles = [random.randint(-50, -30), 0, random.randint(30, 50)]
        # angles = [-50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50]
        for i in angles:
            new_angle = self.angle + i
            if new_angle < 0:
                new_angle += 360
            elif new_angle >= 360:
                new_angle -= 360

            next_trig_coords = calculateNewCoords(self.trigCoords, 2, new_angle)
            next_coords = (round(next_trig_coords[0]), round(next_trig_coords[1]))
            # next_coords = tuple(map(round, next_trig_coords))

            outOfBounds = False
            if screen.tile_height <= next_coords[0] or next_coords[0] <= -1 or -1 >= next_coords[1] or next_coords[1] >= screen.tile_length:
                outOfBounds = True
                n += 1

            values.append([outOfBounds, new_angle, next_trig_coords, next_coords])
        if n == len(angles):
            self.move(screen)
        else:
            best = None
            # print("----------------------")
            for i in range(len(angles)):
                if not values[i][0]:
                    # print(screen.board[values[i][3][0]][values[i][3][1]], values[i][3], values[i][1])
                    if best is None:
                        best = i
                    elif screen.board[values[i][3][0]][values[i][3][1]] > screen.board[values[best][3][0]][values[best][3][1]]:
                        best = i
                    elif screen.board[values[i][3][0]][values[i][3][1]] == screen.board[values[best][3][0]][values[best][3][1]]:
                        if values[i][1] == self.angle:
                            best = i

            self.angle = values[best][1]
            self.move(screen, values[best][2])

    def move(self, screen, package=None):
        if package is None:
            next_trig_coords = calculateNewCoords(self.trigCoords, self.speed, self.angle)

            # next_coords = tuple(map(round, next_trig_coords))
        else:
            # Get midpoint (WORKS ONLY FOR SPEED OF 1)
            next_trig_coords = ((package[0] + self.trigCoords[0]) / 2, (package[1] + self.trigCoords[1]) / 2)
        next_coords = (round(next_trig_coords[0]), round(next_trig_coords[1]))

        angle_of_change = 20

        if screen.tile_height <= next_coords[0] or next_coords[0] <= -1 or -1 >= next_coords[1] or next_coords[1] >= screen.tile_length:
            if screen.tile_height <= next_coords[0] or next_coords[0] <= -1:
                self.angle = 360 - self.angle + random.randint(-angle_of_change, angle_of_change)
            if -1 >= next_coords[1] or next_coords[1] >= screen.tile_length:
                self.angle = 180 - self.angle + random.randint(-angle_of_change, angle_of_change)

            if self.angle < 0:
                self.angle += 360
            elif self.angle >= 360:
                self.angle -= 360
            return self.move(screen)

        self.trigCoords = next_trig_coords
        self.coords = next_coords
        screen.board[next_coords[0]][next_coords[1]] = 1
        # screen.tiles_dict[(next_coords[0], next_coords[1])].update(screen)

    def update(self, screen):
        # print("First", self.angle)
        self.adjust(screen)
        # self.move(screen)
        # print("Second", self.angle)

