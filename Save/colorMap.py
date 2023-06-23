import time, pygame, threading
from multiprocessing import Process, Value, Array, Manager, Queue, Pool
from random import choice as ch

WALL = 1
START = 5
END = 6


class Cell(pygame.sprite.Sprite):
    def __init__(self, y, x, group, size, borderless, path):
        super().__init__(group)
        self.coords = (y, x)
        self.image = pygame.Surface((size, size))
        self.path = path
        self.colors = None
        self.image.fill((255, 255, 255))
        # self.image = wallImg
        self.size = size
        if not borderless:
            self.size += 1
        self.rect = self.image.get_rect(x=x * self.size, y=y * self.size)

    def update(self, change, colorType):
        if change:
            self.image.fill(self.colors[colorType])
        else:
            self.image.fill((255, 255, 255))


class Scan(threading.Thread):
    def __init__(self, master, map, size, borderless, cPoint, p):
        super().__init__()
        self.master = master
        self.map = map
        self.size = size
        self.borderless = borderless
        self.cPoint = cPoint
        self.p = p
        self.master.count += 1
        self.start()

    def run(self):
        currentPoint = self.cPoint
        path = self.p
        while True:
            surrPoints = self.master.surroundingPoints(currentPoint, 1)
            actualMoves = []
            for point in surrPoints:
                y, x = point
                if self.map.map[y, x] not in [WALL, START, END] and (y, x) not in self.master.done:
                    actualMoves.append(point)
            if len(actualMoves) > 0:
                point = ch(actualMoves)
                self.master.done.append(point)
                if len(actualMoves) > 1:
                    Scan(self.master, self.map, self.size, self.borderless, currentPoint, path[:])
                path.append(point)
                if len(path) - 1 > self.master.farthest:
                    self.master.farthest = len(path) - 1
                self.master.points[point] = Cell(point[0], point[1], self.master.pointGroup, self.size, self.borderless,
                                                 path[:])
                currentPoint = point
            else:
                break
        self.master.count -= 1


class ColorMap():
    def __init__(self, map, size, borderless):
        self.points = {}
        self.farthest = 0
        self.count = 0
        self.done = []
        self.pointGroup = pygame.sprite.LayeredUpdates()
        self.colorMapVeryOld(map, size, borderless, map.start, [map.start])

    def surroundingPoints(self, coords, distance):
        pointy, pointx = coords
        return [(pointy, pointx - distance), (pointy - distance, pointx), (pointy, pointx + distance),
                (pointy + distance, pointx)]

    def getPoints(self):
        return self.points, self.pointGroup

    def colorMapNew(self, map, size, borderless, cPoint, p):
        self.farthest, self.points = getPointsControl(map, cPoint, p)

        for point in self.points:
            self.points[point] = Cell(point[0], point[1], self.pointGroup, size, borderless, self.points[point][:])

        coefficient = 1400 / self.farthest
        print(coefficient, self.farthest)
        colors = ['Yellow', 'Orange', 'Green', 'Blue', 'Purple', 'Red']
        colorNums = [0, 255, 510, 765, 1020, 1275, 1530]
        print(f"Distances per color: {int(255 / coefficient)}")
        for i in range(6):
            print(f"{colors[i]}: {int(colorNums[i] / coefficient) + 1} - {int(colorNums[i + 1] / coefficient)}")
        self.getColors(coefficient)

    def getColors(self, coefficient):
        for point in self.points:
            self.points[point].colors = [self.getColor1(int((len(self.points[point].path) - 1) * coefficient)),
                                         self.getColor2(len(self.points[point].path) - 1, coefficient)]

    def colorMapOld(self, map, size, borderless, cPoint, p):
        currentPoint = cPoint
        path = p
        while True:
            surrPoints = self.surroundingPoints(currentPoint, 1)
            actualMoves = []
            for point in surrPoints:
                y, x = point
                if map.map[y, x] not in [WALL, START, END] and (y, x) not in self.done:
                    actualMoves.append(point)
            if len(actualMoves) > 0:
                point = ch(actualMoves)
                self.done.append(point)
                if len(actualMoves) > 1:
                    Scan(self, map, size, borderless, currentPoint, path[:])
                    # self.colorMapNew(map, size, borderless, currentPoint, path[:])
                path.append(point)
                if len(path) - 1 > self.farthest:
                    self.farthest = len(path) - 1
                self.points[point] = Cell(point[0], point[1], self.pointGroup, size, borderless, path[:])
                currentPoint = point
            else:
                break

    def colorMapVeryOld(self, map, size, borderless, cPoint, p):
        currentPoint = cPoint
        done = []
        intersections = []
        path = p
        while True:
            while True:

                surrPoints = self.surroundingPoints(currentPoint, 1)
                actualMoves = []
                for point in surrPoints:
                    y, x = point
                    if map.map[y, x] not in [WALL, START, END] and (y, x) not in done:
                        actualMoves.append(point)

                if len(actualMoves) > 0:
                    if len(actualMoves) > 1:
                        intersections.append(currentPoint)
                    point = ch(actualMoves)
                    path.append(point)
                    done.append(point)
                    if len(path) - 1 > self.farthest:
                        self.farthest = len(path) - 1
                    self.points[point] = Cell(point[0], point[1], self.pointGroup, size, borderless, path[:])
                    currentPoint = point
                else:
                    break
            if len(intersections) > 0:
                currentPoint = intersections[-1]

                path = path[:path.index(currentPoint) + 1]
                intersections.pop()
            else:
                path.pop()
                if len(path) == 0:
                    break
                currentPoint = path[-1]

        coefficient = 1400 / self.farthest
        print(coefficient, self.farthest)
        colors = ['Yellow', 'Orange', 'Green', 'Blue', 'Purple', 'Red']
        colorNums = [0, 255, 510, 765, 1020, 1275, 1530]
        print(f"Distances per color: {int(255 / coefficient)}")
        for i in range(6):
            print(f"{colors[i]}: {int(colorNums[i] / coefficient) + 1} - {int(colorNums[i + 1] / coefficient)}")

        for point in self.points:
            self.points[point].colors = [self.getColor1(int((len(self.points[point].path) - 1) * coefficient)),
                                         self.getColor2(len(self.points[point].path) - 1, coefficient)]

    def getColor1(self, dist):
        # dist = dist - (int(dist / 1530) * 1530)
        color = [255, 0, 0]
        if dist <= 255:
            # Increase green
            color[1] = dist
        elif dist <= 510:
            # Decrease red
            color[0] = 510 - dist
            color[1] = 255
        elif dist <= 765:
            # Increase blue
            color[0] = 0
            color[1] = 255
            color[2] = dist - 510
        elif dist <= 1020:
            # Decrease green
            color[0] = 0
            color[1] = 1020 - dist
            color[2] = 255
        elif dist <= 1275:
            # Increase red
            color[0] = dist - 1020
            color[1] = 0
            color[2] = 255
        elif dist <= 1530:
            # Decrease blue
            color[0] = 255
            color[1] = 0
            color[2] = 1530 - dist

        return tuple(color)

    def getColor2(self, dist, coefficient):
        # dist = dist - (int(dist / 1530) * 1530)
        colorNums = [255, 510, 765, 1020, 1275, 1530]
        for color in range(len(colorNums)):
            colorNums[color] = int(colorNums[color] / coefficient)
        color = [0, 0, 0]
        if dist <= colorNums[0]:
            # Yellow
            color = (255, 255, 0)
        elif dist <= colorNums[1]:
            # Orange
            color = (255, 150, 0)
        elif dist <= colorNums[2]:
            # Green
            color = (0, 255, 0)
        elif dist <= colorNums[3]:
            # Blue
            color = (0, 0, 255)
        elif dist <= colorNums[4]:
            # Purple
            color = (150, 0, 255)
        elif dist <= colorNums[5]:
            # Red
            color = (255, 0, 0)

        return tuple(color)


def slowColorDraw(SIZE, originalSize, points, gamedisplay, colorType):
    for point in points:
        pygame.draw.rect(gamedisplay, points[point].colors[colorType],
                         pygame.Rect(SIZE * point[1], SIZE * point[0], originalSize, originalSize))
        # time.sleep(0.1)
        pygame.display.update()
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()


def getPointsControl(map, cPoint, p):
    with Manager() as manager:
        done = manager.list()
        points = manager.dict()
        farthest = manager.Value('i', 0)
        agents = 1
        with Pool(processes=agents) as pool:
            pool.apply(func=getPoints, args=(map, cPoint, p, done, points, farthest))
            # getPoints(map.map, cPoint, p, done, points, farthest)

        return farthest.get(), points.copy()


def getPoints(map, cPoint, pa, d, po, f):
    done = d
    farthest = f
    points = po
    currentPoint = cPoint
    path = pa
    while True:
        pointy, pointx = currentPoint
        surrPoints = [(pointy, pointx - 1), (pointy - 1, pointx), (pointy, pointx + 1), (pointy + 1, pointx)]
        actualMoves = []
        for point in surrPoints:
            y, x = point
            if map[y, x] not in [WALL, START, END] and (y, x) not in done:
                actualMoves.append(point)
        if len(actualMoves) > 0:
            point = ch(actualMoves)
            done.append(point)
            if len(actualMoves) > 1:
                # p = Process(target=getPoints, args=(map, currentPoint, path[:], done, points, farthest))
                # p.start()
                # p.join()
                getPoints(map, currentPoint, path[:], done, points, farthest)
            path.append(point)
            if len(path) - 1 > farthest.get():
                farthest.set(len(path) - 1)

            points[point] = path[:]
            currentPoint = point
        else:
            break


def addColors(master):
    coefficient = 1400 / master.farthest
    print(coefficient, master.farthest)
    colors = ['Yellow', 'Orange', 'Green', 'Blue', 'Purple', 'Red']
    colorNums = [0, 255, 510, 765, 1020, 1275, 1530]
    print(f"Distances per color: {int(255 / coefficient)}")
    for i in range(6):
        print(f"{colors[i]}: {int(colorNums[i] / coefficient) + 1} - {int(colorNums[i + 1] / coefficient)}")
    for point in master.points:
        master.points[point].colors = [master.getColor1(int((len(master.points[point].path) - 1) * coefficient)),
                                       master.getColor2(len(master.points[point].path) - 1, coefficient)]
