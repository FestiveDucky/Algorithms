import random
from random import choice as ch
from random import randint as ri
from random import randrange as rr

import time
import numpy as np
import pygame

# TODO add feature that removes borders between pixels
NOTHING = 0
WALL = 1
SEEKER = 2
HUNTER = 3
PLAYER = 4
START = 5
END = 6
PATH = 8
TEMPORARYWALL = 9

# wallImg = pygame.image.load(r"images4\BLOCKS\New Piskel (2) (1) (4) (1) (1).png")


class Wall(pygame.sprite.Sprite):
    def __init__(self, y, x, group, size, borderless):
        super().__init__(group)
        self.coords = (y, x)
        self.image = pygame.Surface((size, size))
        self.image.fill((50, 50, 50))
        # self.image = wallImg
        self.size = size
        if not borderless:
            self.size += 1
        self.rect = self.image.get_rect(x=x * self.size, y=y * self.size)

    def update(self, y, x):
        if x is None:
            x = self.coords[1]
        if y is None:
            y = self.coords[0]
        if self.coords == (y, x):
            self.kill()


def checkEvents():
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()


class Maze:
    def __init__(self, BOARDHEIGHT, BOARDWIDTH, SIZE, gamedisplay, display, borderless):
        self.SIZE = SIZE
        self.originalSize = SIZE
        if not borderless:
            self.SIZE += 1
        self.HEIGHT = BOARDHEIGHT // self.SIZE
        self.WIDTH = BOARDWIDTH // self.SIZE

        self.map = np.ones((self.HEIGHT, self.WIDTH))
        self.walls = pygame.sprite.Group()
        self.gamedisplay = gamedisplay
        self.start = None
        self.end = None
        self.display = display
        self.borderless = borderless

        r = False
        if r:
            for i in range(self.HEIGHT):
                for j in range(self.WIDTH):
                    if random.random() < 0.6:
                        self.map[i][j] = 0
        else:
            self.createMaze()

    def updateDisplay(self, y, x, entire=False, bypass=False):
        if self.display or bypass:
            if not entire:
                values = {NOTHING: (50, 50, 50), WALL: (50, 50, 50), PATH: (255, 255, 255),
                          TEMPORARYWALL: (100, 100, 100), START: (0, 255, 0), END: (255, 0, 0)}
                pygame.draw.rect(self.gamedisplay, values[self.map[y, x]],
                                 pygame.Rect(self.SIZE * x, self.SIZE * y, self.originalSize, self.originalSize))
            else:
                self.gamedisplay.fill((0, 0, 0))
                for y in range(0, len(self.map)):
                    for x in range(0, len(self.map[y])):
                        values = {NOTHING: (50, 50, 50), WALL: (50, 50, 50), PATH: (255, 255, 255),
                                  TEMPORARYWALL: (100, 100, 100), START: (0, 255, 0), END: (255, 0, 0)}
                        pygame.draw.rect(self.gamedisplay, values[self.map[y, x]],
                                         pygame.Rect(self.SIZE * x, self.SIZE * y, self.originalSize, self.originalSize))
            pygame.display.update()

    def createMaze(self):
        self.map[1:self.HEIGHT - 1, 1:self.WIDTH - 1] = np.full((self.HEIGHT - 2, self.WIDTH - 2), 9)

        for y in range(1, len(self.map) - 1):
            for x in range(1, len(self.map[y]) - 1):
                if x % 2 and y % 2:
                    self.map[y, x] = 0
        self.updateDisplay(None, None, True)

        # self.algorithm1(self.HEIGHT, self.WIDTH)
        # self.algorithm2()
        self.algorithm2fast()

        self.cleanMap()

        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[y])):
                if self.map[y, x] == TEMPORARYWALL:
                    self.map[y, x] = WALL
                elif self.map[y, x] == NOTHING:
                    self.map[y, x] = WALL
                elif self.map[y, x] == PATH:
                    self.map[y, x] = NOTHING

                if self.map[y, x] == WALL:
                    Wall(y, x, self.walls, self.originalSize, self.borderless)

        self.addStartAndEnd()
        self.updateDisplay(None, None, True, True)

    def algorithm1(self, sizey, sizex):
        while True:
            startx = ri(0, sizex - 1)
            starty = ri(0, sizey - 1)
            if not self.isCorner(starty, startx) and self.map[starty, startx] not in [WALL, TEMPORARYWALL]:
                break
        self.start = (starty, startx)
        self.map[starty, startx] = START

        path = [self.start]
        currentPoint = self.start
        while True:
            checkEvents()
            # time.sleep(0.1)
            availablePoints = self.checkAvailablePoints(currentPoint, 2, [NOTHING])
            if len(availablePoints) != 0:
                previousPoint = currentPoint
                currentPoint = ch(availablePoints)

                y1, x1 = previousPoint
                y2, x2 = currentPoint

                y3 = (y2 + y1) // 2
                x3 = (x2 + x1) // 2
                self.map[y3, x3] = PATH
                self.map[currentPoint[0], currentPoint[1]] = PATH
                path.insert(0, currentPoint)
                self.updateDisplay(y3, x3)
                self.updateDisplay(currentPoint[0], currentPoint[1])
            else:
                newPath = path[:]
                for point in path:
                    newAvailablePoints = self.checkAvailablePoints(point, 2, [NOTHING])
                    if len(newAvailablePoints) != 0:
                        previousPoint = point
                        currentPoint = ch(newAvailablePoints)
                        y1, x1 = previousPoint
                        y2, x2 = currentPoint

                        y3 = (y2 + y1) // 2
                        x3 = (x2 + x1) // 2
                        self.map[y3, x3] = PATH
                        self.map[currentPoint[0], currentPoint[1]] = PATH
                        newPath.insert(0, currentPoint)
                        self.updateDisplay(y3, x3)
                        self.updateDisplay(currentPoint[0], currentPoint[1])
                        break
                    else:
                        newPath.remove(point)

                if len(newPath) == 0:
                    break
                else:
                    path = newPath

        endy, endx = self.farthestPoint(starty, startx)
        self.map[endy, endx] = END
        self.end = (endy, endx)

    def algorithm2(self):
        emptyPoints = []
        for y in range(1, len(self.map) - 1):
            for x in range(1, len(self.map[y]) - 1):
                if self.map[y, x] == NOTHING:
                    emptyPoints.append((y, x))
        self.start = ch(emptyPoints)
        emptyPoints.remove(self.start)
        self.map[self.start[0], self.start[1]] = PATH
        self.updateDisplay(self.start[0], self.start[1])

        while True:
            checkEvents()
            try:
                currentPoint = ch(emptyPoints)
            except:
                break
            emptyPoints.remove(currentPoint)
            self.map[currentPoint[0], currentPoint[1]] = PATH
            self.updateDisplay(currentPoint[0], currentPoint[1])
            path = [currentPoint]
            midPoints = [(None)]

            while True:
                # time.sleep(0.05)
                # self.checkEvents()
                availablePoints = self.checkAvailablePoints(currentPoint, 2, [NOTHING, PATH])
                previousPoint = currentPoint
                currentPoint = ch(availablePoints)
                if currentPoint not in path:
                    if currentPoint in emptyPoints:
                        emptyPoints.remove(currentPoint)
                    y1, x1 = previousPoint
                    y2, x2 = currentPoint

                    y3 = (y2 + y1) // 2
                    x3 = (x2 + x1) // 2
                    self.map[y3, x3] = PATH
                    self.updateDisplay(y3, x3)
                    if self.map[currentPoint[0], currentPoint[1]] == PATH:
                        break
                    self.map[y2, x2] = PATH
                    self.updateDisplay(currentPoint[0], currentPoint[1])

                    path.insert(0, currentPoint)
                    midPoints.insert(0, (y3, x3))
                else:
                    for pointIndex in range(len(path)):
                        if path[pointIndex] != currentPoint:
                            self.map[path[pointIndex][0], path[pointIndex][1]] = NOTHING
                            self.map[midPoints[pointIndex][0], midPoints[pointIndex][1]] = TEMPORARYWALL
                            self.updateDisplay(path[pointIndex][0], path[pointIndex][1])
                            self.updateDisplay(midPoints[pointIndex][0], midPoints[pointIndex][1])
                            emptyPoints.append((path[pointIndex][0], path[pointIndex][1]))
                        else:
                            break
                    midPoints = midPoints[path.index(currentPoint):]
                    path = path[path.index(currentPoint):]

    def algorithm2fast(self):
        emptyPoints = []
        for y in range(1, len(self.map) - 1):
            for x in range(1, len(self.map[y]) - 1):
                if self.map[y, x] == NOTHING:
                    emptyPoints.append((y, x))
        val1 = self.HEIGHT // 2
        if val1 % 2 != 0: val1 += 1
        firstPathCountLimit = rr(val1, self.WIDTH * 3, 2)
        first = True
        while True:
            checkEvents()
            try:
                currentPoint = ch(emptyPoints)
            except:
                break
            emptyPoints.remove(currentPoint)
            self.map[currentPoint[0], currentPoint[1]] = PATH
            self.updateDisplay(currentPoint[0], currentPoint[1])
            path = [currentPoint]
            midPoints = [(None)]
            if first:
                self.start = currentPoint
                self.map[self.start[0], self.start[1]] = PATH
                self.updateDisplay(self.start[0], self.start[1])
            while True:
                # time.sleep(0.05)
                checkEvents()
                availablePoints = self.checkAvailablePoints(currentPoint, 2, [NOTHING, PATH])
                previousPoint = currentPoint
                currentPoint = ch(availablePoints)
                if currentPoint not in path:
                    if currentPoint in emptyPoints:
                        emptyPoints.remove(currentPoint)
                    y1, x1 = previousPoint
                    y2, x2 = currentPoint

                    y3 = (y2 + y1) // 2
                    x3 = (x2 + x1) // 2
                    self.map[y3, x3] = PATH
                    self.updateDisplay(y3, x3)
                    if self.map[currentPoint[0], currentPoint[1]] == PATH:
                        break
                    self.map[y2, x2] = PATH
                    self.updateDisplay(currentPoint[0], currentPoint[1])

                    path.insert(0, currentPoint)
                    midPoints.insert(0, (y3, x3))
                    if len(path) + len(midPoints) >= firstPathCountLimit and first:
                        break
                else:
                    for pointIndex in range(len(path)):
                        if path[pointIndex] != currentPoint:
                            self.map[path[pointIndex][0], path[pointIndex][1]] = NOTHING
                            self.map[midPoints[pointIndex][0], midPoints[pointIndex][1]] = TEMPORARYWALL
                            self.updateDisplay(path[pointIndex][0], path[pointIndex][1])
                            self.updateDisplay(midPoints[pointIndex][0], midPoints[pointIndex][1])
                            emptyPoints.append((path[pointIndex][0], path[pointIndex][1]))
                        else:
                            break
                    midPoints = midPoints[path.index(currentPoint):]
                    path = path[path.index(currentPoint):]
            first = False

    def checkAvailablePoints(self, point, distance, toCheck):
        pointy, pointx = point
        surroundingPoints = [(pointy, pointx - distance), (pointy - distance, pointx), (pointy, pointx + distance),
                             (pointy + distance, pointx)]
        availablePoints = []
        for y, x in surroundingPoints:
            if self.HEIGHT > y > -1 and self.WIDTH > x > -1:
                if self.map[y, x] in toCheck:
                    y1, x1 = point
                    y2, x2 = y, x

                    y3 = (y2 + y1) // 2
                    x3 = (x2 + x1) // 2
                    if self.map[y3, x3] != PATH:
                        availablePoints.append((y, x))
        return availablePoints

    def isCorner(self, y, x):
        return (y, x) in [(0, 0), (self.HEIGHT - 1, 0), (0, self.WIDTH - 1), (self.HEIGHT - 1, self.WIDTH - 1)]

    def addStartAndEnd(self):
        self.end = self.farthestPoint(self.start[0], self.start[1])
        self.map[self.end[0], self.end[1]] = END
        self.map[self.start[0], self.start[1]] = START
        self.walls.update(self.end[0], self.end[1])

    def farthestPoint(self, starty, startx):
        farthestroomlist = [[0, (0, 0)]]
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                disy = abs(starty - y)
                disx = abs(startx - x)
                if disy + disx > farthestroomlist[0][0] and not self.isCorner(y, x):
                    farthestroomlist = [[disy + disx, (y, x)]]
                elif disy + disx == farthestroomlist[0][0] and not self.isCorner(y, x):
                    farthestroomlist.append([disy + disx, (y, x)])
                else:
                    pass
        whichChosenPoint = ri(0, len(farthestroomlist) - 1)
        chosenPoint = farthestroomlist[whichChosenPoint][1]
        return chosenPoint

    def cleanMap(self):
        emptyMap = np.ones((self.HEIGHT, self.WIDTH))
        emptyMap[1:self.HEIGHT - 1, 1:self.WIDTH - 1] = np.full((self.HEIGHT - 2, self.WIDTH - 2), 9)
        if np.array_equal(self.map[self.HEIGHT - 2], emptyMap[1]):
            self.map = np.delete(self.map, self.HEIGHT - 2, 0)
            emptyMap = np.delete(emptyMap, self.HEIGHT - 2, 0)
            self.HEIGHT -= 1
            self.walls.update(self.HEIGHT, None)

        if np.array_equal(self.map[:, -2], emptyMap[:, 1]):
            self.map = np.delete(self.map, -2, 1)
            self.WIDTH -= 1
            self.walls.update(None, 1)
