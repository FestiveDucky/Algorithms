import math
import random

import pygame, pygame.gfxdraw, time
from math import *

colors = [(230, 25, 75), (245, 130, 48), (255, 225, 25), (210, 245, 60), (60, 180, 75), (70, 240, 240), (0, 130, 200),
          (145, 30, 180),
          (240, 50, 230)]
# (128, 128, 128), (255, 255, 255)
LINE_COLOR = (255, 255, 255)

LINE_THICKNESS = 2


class Point(pygame.sprite.Sprite):
    def __init__(self, coords, group):
        super().__init__(group)
        self.coords = coords
        self.selected = False
        self.rect = pygame.Rect(self.coords[0] - 10, self.coords[1] - 10, 20, 20)

    def update(self, display):
        if self.selected:
            pygame.draw.circle(display, (0, 255, 0), self.coords, LINE_THICKNESS * 2)
        else:
            pygame.draw.circle(display, (100, 100, 100), self.coords, LINE_THICKNESS * 2)

    def setCoords(self, coords):
        self.coords = coords
        self.rect = pygame.Rect(self.coords[0] - 10, self.coords[1] - 10, 20, 20)

    def getCoords(self):
        return self.coords


class BezierCurve:
    def __init__(self, points, display):
        assert len(points) > 2
        self.points = points
        self.display = display
        self.point_group = pygame.sprite.LayeredUpdates()
        self.point_classes = [Point(coords, self.point_group) for coords in self.points]
        self.bezier_points = []

    def BezierPoint(self, t, points, drawLines, drawPoints, total_points):
        new_points = []
        for i in range(len(points) - 1):
            if drawLines:
                self.drawThickLine(colors[abs(len(points) - total_points)], points[i], points[i + 1])
                # pygame.draw.aaline(self.display, colors[abs(len(points) - total_points)], points[i],
                #                    points[i + 1])
            new_points.append(self.pointOnLine(points[i], points[i + 1], t))
            if drawPoints:
                pygame.draw.circle(self.display, colors[abs(len(points) - total_points)], points[i], LINE_THICKNESS * 2)

        if drawPoints:
            pygame.draw.circle(self.display, colors[abs(len(points) - total_points)], points[-1], LINE_THICKNESS * 2)

        if len(new_points) != 1:
            return self.BezierPoint(t, new_points, drawLines, drawPoints, total_points)
        else:
            if drawPoints:
                pygame.draw.circle(self.display, LINE_COLOR, new_points[0], LINE_THICKNESS * 2)
            return new_points[0]

    def calculateBezierCurve(self, precision, drawPoints, drawCurve, drawLerps, pause, drawCircle, drawVectors=False):
        self.bezier_points = []
        for i in range(precision + 1):

            events()

            if pause != 0:
                pygame.display.update()
                time.sleep(pause)
                self.display.fill((0, 0, 0))

            p = self.BezierPoint(i / precision, self.points, drawLerps, pause != 0, len(self.points))
            self.bezier_points.append(p)

            if pause != 0:
                self.reDraw(i, drawCurve, drawPoints)

            if drawCircle:
                r = self.curvatureRadius(i / precision)
                if r is not None:
                    pygame.draw.circle(self.display, LINE_COLOR, (p[0], p[1] + r), r, width=1)
            if drawVectors:
                self.firstDerivativeV2(i / precision)
                self.drawThickLine((0, 255, 255), self.bezier_points[i], self.firstDerivative(i / precision))
                self.drawThickLine((0, 0, 255), self.bezier_points[i], self.secondDerivative(i / precision))
            if drawPoints:
                pygame.draw.circle(self.display, (0, 255, 0), p, LINE_THICKNESS)
            if drawCurve:
                if i != 0:
                    self.drawThickLine(LINE_COLOR, self.bezier_points[i - 1], self.bezier_points[i])
                    # pygame.draw.aaline(self.display, LINE_COLOR, self.bezier_points[i - 1], self.bezier_points[i])

    def reDraw(self, ind, dC, dP):
        for i in range(ind):
            if dP:
                pygame.draw.circle(self.display, (0, 255, 0), self.bezier_points[i], LINE_THICKNESS)
            if dC:
                if i != 0:
                    self.drawThickLine(LINE_COLOR, self.bezier_points[i - 1], self.bezier_points[i])
                    # pygame.draw.aaline(self.display, LINE_COLOR, self.bezier_points[i - 1], self.bezier_points[i])

    def setNewPoints(self):
        old_points = self.points[:]
        self.points = [point.getCoords() for point in self.point_classes]
        if old_points == self.points:
            return False
        return True

    def drawThickLine(self, color, p1, p2):
        # Not my code, found on the internet to draw thicker lines
        center_L1 = self.pointOnLine(p1, p2, 0.5)
        length = math.dist(p1, p2)
        thickness = LINE_THICKNESS
        angle = atan2(p1[1] - p2[1], p1[0] - p2[0])
        UL = (center_L1[0] + (length / 2.) * cos(angle) - (thickness / 2.) * sin(angle),
              center_L1[1] + (thickness / 2.) * cos(angle) + (length / 2.) * sin(angle))
        UR = (center_L1[0] - (length / 2.) * cos(angle) - (thickness / 2.) * sin(angle),
              center_L1[1] + (thickness / 2.) * cos(angle) - (length / 2.) * sin(angle))
        BL = (center_L1[0] + (length / 2.) * cos(angle) + (thickness / 2.) * sin(angle),
              center_L1[1] - (thickness / 2.) * cos(angle) + (length / 2.) * sin(angle))
        BR = (center_L1[0] - (length / 2.) * cos(angle) + (thickness / 2.) * sin(angle),
              center_L1[1] - (thickness / 2.) * cos(angle) - (length / 2.) * sin(angle))

        pygame.gfxdraw.aapolygon(self.display, (UL, UR, BR, BL), color)
        pygame.gfxdraw.filled_polygon(self.display, (UL, UR, BR, BL), color)

    def addPoint(self, p):
        self.point_classes.append(Point(p, self.point_group))

    def removePoint(self):
        self.point_group.remove(self.point_classes.pop())

    @staticmethod
    def pointOnLine(p1, p2, t):
        return (p2[0] - p1[0]) * t + p1[0], (p2[1] - p1[1]) * t + p1[1]

    def firstDerivative(self, t):
        final_vector = [0, 0]
        n = len(self.points) - 1
        for i in range(n):
            scalar = self.bValue(n - 1, i, t) * n * t
            final_vector[0] += scalar * (self.points[i + 1][0] - self.points[i][0])
            final_vector[1] += scalar * (self.points[i + 1][1] - self.points[i][1])
        return tuple(final_vector)

    def firstDerivativeV2(self, t):
        print("FINDING DERIVATIVE", t)
        final_vector = [0, 0]
        n = len(self.points) - 1
        for i in range(n):
            scalar = self.bValue(n - 2, i, t) * n * t
            print(scalar)
            final_vector[0] += scalar * (self.points[i + 1][0] - self.points[i][0])
            final_vector[1] += scalar * (self.points[i + 1][1] - self.points[i][1])
        return tuple(final_vector)

    def secondDerivative(self, t):
        final_vector = [0, 0]
        n = len(self.points) - 1
        for i in range(n - 1):
            scalar = self.bValue(n - 2, i, t) * n * (n - 1)
            final_vector[0] += scalar * (self.points[i + 2][0] - 2 * self.points[i + 1][0] + self.points[i][0])
            final_vector[1] += scalar * (self.points[i + 2][1] - 2 * self.points[i + 1][1] + self.points[i][1])
        return tuple(final_vector)

    def curvatureRadius(self, t):
        f = self.firstDerivative(t)
        s = self.secondDerivative(t)
        numerator = abs(f[0] * s[1] - f[1] * s[0])
        denominator = ((f[0] ** 2) + (f[1] ** 2)) ** (1.5)
        if denominator == 0 or numerator == 0:
            print("Undefined Curvature (A line)")
        else:
            k = numerator / denominator
            return 1. / k

    @staticmethod
    def bValue(n, i, t):
        # n is the degree of the bezier curve meaning n + 1 is the number of control points\
        # Formulas found here https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/Bezier/bezier-der.html
        return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))


def events(nested=False):
    while True:
        ev = pygame.event.get()
        for e in ev:
            if e.type == pygame.QUIT:
                pygame.quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if not nested:
                        events(True)
                    else:
                        return
        if not nested:
            return
