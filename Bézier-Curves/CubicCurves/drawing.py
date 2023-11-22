import math
import random
import ctypes


from button import *
from random import randint as ri
import pygame, pygame.gfxdraw, time
from math import *

# colors = [(230, 25, 75), (245, 130, 48), (255, 225, 25), (210, 245, 60), (60, 180, 75), (70, 240, 240), (0, 130, 200),
#           (145, 30, 180),
#           (240, 50, 230)]

colors = [(217, 15, 73), (182, 158, 60), (13, 192, 128)]

# (128, 128, 128), (255, 255, 255)
LINE_COLOR = (42, 150, 204)

LINE_THICKNESS = 2


class Point(pygame.sprite.Sprite):
    def __init__(self, coords, group):
        super().__init__(group)
        self.coords = coords
        self.selected = False
        self.rect = pygame.Rect(self.coords[0] - 10, self.coords[1] - 10, 20, 20)

    def update(self, display, special=False):
        if not special:
            if self.selected:
                pygame.draw.circle(display, (0, 255, 0), self.coords, LINE_THICKNESS * 2)
            else:
                pygame.draw.circle(display, (255, 255, 255), self.coords, LINE_THICKNESS * 2)
        else:
            pygame.draw.circle(display, colors[0], self.coords, LINE_THICKNESS * 2)

    def setCoords(self, coords):
        self.coords = coords
        self.rect = pygame.Rect(self.coords[0] - 10, self.coords[1] - 10, 20, 20)

    def getCoords(self):
        return self.coords


class CubicBezierCurve:
    def __init__(self, points, display):
        assert len(points) == 4
        self.points = []
        self.display = display
        self.point_group = pygame.sprite.LayeredUpdates()
        self.point_classes = points
        self.bezier_points = []

        self.setNewPoints()

    def BezierPoint(self, t, points, drawLines, total_points, animation):
        new_points = []
        for i in range(len(points) - 1):
            # Drawing the lerps
            if drawLines:
                self.drawThickLine(self.display, colors[abs(len(points) - total_points)], points[i], points[i + 1])

                # Drawing the points on the lines
                pygame.draw.circle(self.display, colors[abs(len(points) - total_points)], points[i], LINE_THICKNESS * 2)

            # Saving the new point
            new_points.append(self.pointOnLine(points[i], points[i + 1], t))

        # Drawing the extra point we missed
        if drawLines:
            pygame.draw.circle(self.display, colors[abs(len(points) - total_points)], points[-1], LINE_THICKNESS * 2)

        if len(new_points) != 1:
            # Running again until we reach the final point
            return self.BezierPoint(t, new_points, drawLines, total_points, animation)
        else:
            # Draw the final point
            if animation:
                pygame.draw.circle(self.display, LINE_COLOR, new_points[0], LINE_THICKNESS * 2)
            return new_points[0]

    def calculateBezierCurve(self, precision, drawPoints, drawCurve, drawLerps, pause, drawCircle, drawVectors,
                             hidePoints, redrawCurves=None, pointG=None):
        if redrawCurves is None:
            redrawCurves = []
        self.bezier_points = []
        for i in range(precision + 1):

            events()

            if pause != 0:
                pygame.display.update()
                time.sleep(pause)
                if i != precision:
                    self.display.fill((14, 25, 36))

            p = self.BezierPoint(i / precision, self.points, drawLerps, len(self.points), pause != 0)
            self.bezier_points.append(p)

            if pause != 0:
                self.reDraw(i, drawCurve, drawPoints)
                for c in redrawCurves:
                    c.calculateBezierCurve(precision, drawPoints, drawCurve, False, 0, False, False, hidePoints)
                if drawLerps:
                    pointG.update(self.display, True)
                elif not hidePoints:
                    pointG.update(self.display)

            if drawCircle:
                r = self.curvatureRadius(i / precision)
                d1 = self.firstDerivative(i / precision)
                if r is not None:
                    # Circle on inside
                    d1 = (-d1[1] + p[0], d1[0] + p[1])
                    # Circle on outside
                    # d1 = (d1[1] + p[0], -d1[0] + p[1])
                    d = r / math.dist(p, d1)
                    p1 = ((1 - d) * p[0] + d * d1[0], (1 - d) * p[1] + d * d1[1])
                    pygame.draw.circle(self.display, LINE_COLOR, p1, abs(r), width=1)

            if drawVectors:
                d1 = self.firstDerivative(i / precision)
                d2 = self.secondDerivative(i / precision)
                p2 = (d1[0] * 0.2 + p[0], d1[1] * 0.2 + p[1])
                p3 = (d2[0] * 0.05 + p2[0], d2[1] * 0.05 + p2[1])
                self.drawThickLine(self.display, (134,30,63), p, p2)
                self.drawThickLine(self.display, (98, 44, 156), p2, p3)

            if drawPoints:
                pygame.draw.circle(self.display, (0, 255, 0), p, LINE_THICKNESS)

            if drawCurve:
                if i != 0:
                    self.drawThickLine(self.display, LINE_COLOR, self.bezier_points[i - 1], self.bezier_points[i])

    def reDraw(self, ind, dC, dP):
        for i in range(ind):
            if dP:
                pygame.draw.circle(self.display, (0, 255, 0), self.bezier_points[i], LINE_THICKNESS)
            if dC:
                if i != 0:
                    self.drawThickLine(self.display, LINE_COLOR, self.bezier_points[i - 1], self.bezier_points[i])

    def setNewPoints(self):
        old_points = self.points[:]
        self.points = [point.getCoords() for point in self.point_classes]
        if old_points == self.points:
            return False
        return True

    def secondDerivative(self, t):
        final_vector = [0, 0]
        final_vector[0] += self.points[0][0] * (-6. * t + 6)
        final_vector[1] += self.points[0][1] * (-6. * t + 6)
        final_vector[0] += self.points[1][0] * (18 * t - 12)
        final_vector[1] += self.points[1][1] * (18 * t - 12)
        final_vector[0] += self.points[2][0] * (-18 * t + 6)
        final_vector[1] += self.points[2][1] * (-18 * t + 6)
        final_vector[0] += self.points[3][0] * (6 * t)
        final_vector[1] += self.points[3][1] * (6 * t)
        return tuple(final_vector)

    def firstDerivative(self, t):
        # stackoverflow.com/questions/4089443/find-the-tangent-of-a-point-on-a-bezier-curve
        final_vector = [0, 0]
        final_vector[0] += 3. * ((1 - t) ** 2) * (self.points[1][0] - self.points[0][0])
        final_vector[1] += 3. * ((1 - t) ** 2) * (self.points[1][1] - self.points[0][1])
        final_vector[0] += 6. * t * (1 - t) * (self.points[2][0] - self.points[1][0])
        final_vector[1] += 6. * t * (1 - t) * (self.points[2][1] - self.points[1][1])
        final_vector[0] += 3. * t ** 2 * (self.points[3][0] - self.points[2][0])
        final_vector[1] += 3. * t ** 2 * (self.points[3][1] - self.points[2][1])
        return tuple(final_vector)

    def curvatureRadius(self, t):
        f = self.firstDerivative(t)
        s = self.secondDerivative(t)
        # numerator = abs(f[0] * s[1] - f[1] * s[0])
        numerator = f[0] * s[1] - f[1] * s[0]
        flip = False
        if numerator < 0:
            flip = True
            numerator = abs(numerator)
        denominator = ((f[0] ** 2) + (f[1] ** 2)) ** (1.5)
        if denominator == 0 or numerator == 0:
            print("Undefined Curvature (A line)")
        else:

            k = numerator / denominator
            if flip:
                return -(1. / k)
            return 1. / k

    def boundingBox(self, draw=True):
        xRoots = self.quadraticFormula(
            -3 * self.points[0][0] + 9 * self.points[1][0] - 9 * self.points[2][0] + 3 * self.points[3][0],
            6 * self.points[0][0] - 12 * self.points[1][0] + 6 * self.points[2][0],
            -3 * self.points[0][0] + 3 * self.points[1][0])
        yRoots = self.quadraticFormula(
            -3 * self.points[0][1] + 9 * self.points[1][1] - 9 * self.points[2][1] + 3 * self.points[3][1],
            6 * self.points[0][1] - 12 * self.points[1][1] + 6 * self.points[2][1],
            -3 * self.points[0][1] + 3 * self.points[1][1])

        t_values = [0, 1]
        if xRoots is not None:
            if 0 < xRoots[0] < 1:
                t_values.append(xRoots[0])
            if 0 < xRoots[1] < 1:
                t_values.append(xRoots[1])
        if yRoots is not None:
            if 0 < yRoots[0] < 1:
                t_values.append(yRoots[0])
            if 0 < yRoots[1] < 1:
                t_values.append(yRoots[1])

        points = [self.BezierPoint(t, self.points, False, 4, False) for t in t_values]
        xValues = list(map(lambda x: x[0], points))
        xBounds = [max(xValues), min(xValues)]
        yValues = list(map(lambda x: x[1], points))
        yBounds = [max(yValues), min(yValues)]

        if draw:
            pygame.draw.rect(self.display, (150, 150, 150),
                             pygame.Rect(xBounds[1], yBounds[1], xBounds[0] - xBounds[1], yBounds[0] - yBounds[1]), 1)
        else:
            return xBounds + yBounds

    @staticmethod
    def quadraticFormula(a, b, c):
        if b ** 2 - 4 * a * c < 0:
            return
        d = math.sqrt(b ** 2 - 4 * a * c)
        return (-b + d) / (2 * a), (-b - d) / (2 * a)

    @staticmethod
    def drawThickLine(display, color, p1, p2):
        # Not my code, found on the internet to draw thicker lines
        center_L1 = CubicBezierCurve.pointOnLine(p1, p2, 0.5)
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

        pygame.gfxdraw.aapolygon(display, (UL, UR, BR, BL), color)
        pygame.gfxdraw.filled_polygon(display, (UL, UR, BR, BL), color)

    def drawVector(self, display, color, p1, p2):
        self.drawThickLine(display, color, p1, p2)

        vector = (p2[0] - p1[0], p2[1] - p1[1])
        vector = p2

        theta = math.pi / 4
        f1 = [0, 0]

        f1[0] += math.cos(theta) * vector[0]
        f1[0] += math.sin(theta) * vector[1]
        f1[1] += math.sin(theta) * vector[0]
        f1[1] += math.cos(theta) * vector[1]

        theta = 7 * math.pi/4
        f2 = [0, 0]

        f2[0] += math.cos(theta) * vector[0]
        f2[0] += math.sin(theta) * vector[1]
        f2[1] += math.sin(theta) * vector[0]
        f2[1] += math.cos(theta) * vector[1]

        p3 = (p1[0] + f1[0], p1[1] + f1[1])
        p4 = (p1[0] + f2[0], p1[1] + f2[1])
        self.drawThickLine(display, color, p3, p2)
        self.drawThickLine(display, color, p4, p2)


    @staticmethod
    def pointOnLine(p1, p2, t):
        return (p2[0] - p1[0]) * t + p1[0], (p2[1] - p1[1]) * t + p1[1]


class Curve:
    def __init__(self, points, display, precision):
        assert len(points) >= 4
        self.points = points
        self.precision = precision
        self.point_group = pygame.sprite.LayeredUpdates()
        self.point_classes = []
        self.curves = []
        for i in range(len(points)):
            self.point_classes.append(Point(points[i], self.point_group))
            if i % 3 == 0 and i != 0:
                self.curves.append(CubicBezierCurve(
                    [self.point_classes[i - 3], self.point_classes[i - 2], self.point_classes[i - 1],
                     self.point_classes[i]], display))
        self.display = display

    def shiftPoints(self, vector):
        for point in self.point_classes:
            coords = point.getCoords()
            point.setCoords((coords[0] + vector[0], coords[1] + vector[1]))

        new_bezier_points = []
        for point in self.curves[-1].bezier_points:
            new_bezier_points.append((point[0] + vector[0], point[1] + vector[1]))
        self.curves[-1].bezier_points = new_bezier_points
        self.setPoints()

    def start(self, menu, w, h, vals):
        drawToScreen = True
        running = True
        draw_lerps, show_segments, show_mid_line, draw_points, draw_curve, draw_circle, draw_vectors, draw_bounding_boxes, new_draw_type, allign_segments, miror_segments, hide_points = vals
        i = 0

        direction = ri(1, 4)
        center = (w // 2, h // 2)
        self.curves[-1].bezier_points = []

        speed = 0

        clock = pygame.time.Clock()
        while running:
            clock.tick(200)

            eve = pygame.event.get()
            for e in eve:
                if e.type == pygame.QUIT:
                    pygame.quit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = e.pos

                    buttonsClicked = menu.button_group.get_sprites_at((mousex, mousey))
                    if len(buttonsClicked) > 0:
                        buttonsClicked[0].pressed()
                        values = menu.getValues()
                        draw_lerps, show_segments, show_mid_line, draw_points, draw_curve, draw_circle, draw_vectors, draw_bounding_boxes, new_draw_type, allign_segments, miror_segments, hide_points = values

                        if miror_segments and buttonsClicked[0] == menu.buttons[10]:
                            menu.buttons[9].set(False)
                        elif allign_segments:
                            menu.buttons[10].set(False)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        # Pause
                        events(True)
                    elif e.key == pygame.K_i:
                        return
                    elif e.key == pygame.K_UP:
                        speed += 0.001
                    elif e.key == pygame.K_DOWN and speed > 0.001:
                        speed -= 0.001

            # Draw previous curves
            for j in range(len(self.curves) - 1):
                self.curves[j].calculateBezierCurve(self.precision, draw_points, draw_curve, False, 0, False, False,
                                                    hide_points)
                if draw_bounding_boxes:
                    self.curves[j].boundingBox()

            curve = self.curves[-1]
            p = curve.BezierPoint(i / self.precision, curve.points, draw_lerps, 4, True)
            curve.bezier_points.append(p)

            curve.reDraw(i, draw_curve, draw_points)

            if show_segments:
                self.drawOutline(show_mid_line)

            if draw_circle:
                r = curve.curvatureRadius(i / self.precision)
                d1 = curve.firstDerivative(i / self.precision)
                if r is not None:
                    d1 = (-d1[1] + p[0], d1[0] + p[1])
                    d = r / math.dist(p, d1)
                    p1 = ((1 - d) * p[0] + d * d1[0], (1 - d) * p[1] + d * d1[1])
                    pygame.draw.circle(self.display, LINE_COLOR, p1, abs(r), width=1)

            if draw_vectors:
                d1 = curve.firstDerivative(i / self.precision)
                d2 = curve.secondDerivative(i / self.precision)
                p2 = (d1[0] * 0.2 + p[0], d1[1] * 0.2 + p[1])
                p3 = (d2[0] * 0.05 + p2[0], d2[1] * 0.05 + p2[1])
                curve.drawThickLine(self.display, (134,30,63), p, p2)
                curve.drawThickLine(self.display, (98, 44, 156), p2, p3)

            if draw_points:
                pygame.draw.circle(self.display, (0, 255, 0), p, LINE_THICKNESS)

            if draw_curve:
                if i != 0:
                    curve.drawThickLine(self.display, LINE_COLOR, curve.bezier_points[i - 1],
                                        curve.bezier_points[i])
            if drawToScreen:
                pygame.display.update()

            time.sleep(speed)

            vector = (center[0] - p[0], center[1] - p[1])
            self.shiftPoints(vector)

            # if i % (self.precision//30) == 0:
            #     pygame.image.save(self.display, f"image{i}.png")
            #     ctypes.windll.user32.SystemParametersInfoW(20, 0,
            #                                                fr"F:\Coding\GitHub\Algorithms\Bézier-Curves\CubicCurves\image{i}.png",
            #                                                0)
            self.display.fill((14, 25, 36))
            menu.draw()

            if not hide_points:
                self.point_group.update(self.display)

            i += 1
            #
            # If we finished drawing a curve, we make the next one
            if i == self.precision:
                multiDirection = False
                if multiDirection:
                    other = [[4, 2], [1, 3], [2, 4], [3, 1]][direction - 1]
                    direction = random.choice(other + [direction] * 3)

                    final_point = [(ri(100, w - 200), ri(100, h // 2 - 100)),
                                   (ri(w // 2 + 100, w - 200), ri(100, h - 100)),
                                   (ri(100, w - 200), ri(h // 2 + 100, h - 100)),
                                   (ri(100, w // 2 - 100), ri(100, h - 100))][direction - 1]
                else:
                    # Always in one direction (Right)
                    final_point = (ri(w // 2 + 100, w - 200), ri(100, h - 100))

                self.addCurve([(ri(100, w - 200), ri(100, h - 100)), (ri(100, w - 200), ri(100, h - 100)), final_point])

                # Allign new point so that the velocity is constant (smooth animation)
                if miror_segments:
                    self.allignSegments(self.point_classes[-5], None, True)
                elif allign_segments:
                    self.allignSegments(self.point_classes[-5], None)
                i = 0

            # Check for curves that are outside the bounds of the screen and remove them
            while len(self.curves) != 1:
                bounds = self.curves[0].boundingBox(False)
                if bounds[0] < -w or bounds[1] > w*2 or bounds[2] < -h or bounds[3] > h*2:
                    self.curves = list(reversed(self.curves))
                    self.points = list(reversed(self.points))
                    self.point_classes = list(reversed(self.point_classes))

                    self.removeCurve()

                    self.curves = list(reversed(self.curves))
                    self.points = list(reversed(self.points))
                    self.point_classes = list(reversed(self.point_classes))
                else:
                    break

    def draw(self, drawPoints, drawCurve, drawLerps, pause, drawCircle, drawOutline, drawMidLine, drawVectors,
             drawBoundingBoxes, hidePoints):
        redraw_curves = []
        for curve in self.curves:
            curve.calculateBezierCurve(self.precision, drawPoints, drawCurve, drawLerps, pause, drawCircle, drawVectors,
                                       hidePoints, redrawCurves=redraw_curves, pointG=self.point_group)

            redraw_curves.append(curve)

        if drawOutline:
            self.drawOutline(drawMidLine)

        if drawBoundingBoxes:
            for curve in self.curves:
                curve.boundingBox()

    def drawOutline(self, drawMidLine):
        for i in range(len(self.points) - 1):
            if i % 3 != 1 or drawMidLine:
                CubicBezierCurve.drawThickLine(self.display, colors[i % 3], self.points[i], self.points[i + 1])

    def draw2(self, drawPoints, drawCurve, drawLerps, pause, drawCircle, drawVectors, hidePoints):
        for curve in self.curves:
            curve.bezier_points = []

        for i in range(self.precision + 1):

            for curve in self.curves:
                p = curve.BezierPoint(i / self.precision, curve.points, drawLerps, 4, pause != 0)
                curve.bezier_points.append(p)

                if pause != 0:
                    curve.reDraw(i, drawCurve, drawPoints)

                if drawCircle:
                    r = curve.curvatureRadius(i / self.precision)
                    d1 = curve.firstDerivative(i / self.precision)
                    if r is not None:
                        # Circle on inside
                        d1 = (-d1[1] + p[0], d1[0] + p[1])
                        # Circle on outside
                        # d1 = (d1[1] + p[0], -d1[0] + p[1])
                        d = r / math.dist(p, d1)
                        p1 = ((1 - d) * p[0] + d * d1[0], (1 - d) * p[1] + d * d1[1])
                        pygame.draw.circle(self.display, LINE_COLOR, p1, abs(r), width=1)

                if drawVectors:
                    d1 = curve.firstDerivative(i / self.precision)
                    d2 = curve.secondDerivative(i / self.precision)
                    p2 = (d1[0] * 0.2 + p[0], d1[1] * 0.2 + p[1])
                    p3 = (d2[0] * 0.05 + p2[0], d2[1] * 0.05 + p2[1])
                    curve.drawThickLine(self.display, (134,30,63), p, p2)
                    curve.drawThickLine(self.display, (98, 44, 156), p2, p3)

                if drawPoints:
                    pygame.draw.circle(self.display, (0, 255, 0), p, LINE_THICKNESS)

                if drawCurve:
                    if i != 0:
                        curve.drawThickLine(self.display, LINE_COLOR, curve.bezier_points[i - 1],
                                            curve.bezier_points[i])
            events()

            if pause != 0:
                pygame.display.update()
                time.sleep(pause)
                if i != self.precision:
                    self.display.fill((14, 25, 36))
                if not hidePoints:
                    self.point_group.update(self.display)

    def allignSegments(self, p, move, miror=False):
        i = self.point_classes.index(p)
        if i % 3 == 1 and i != 1:
            otherP = self.point_classes[i - 2]
            centerP = self.point_classes[i - 1]
        elif i % 3 == 2 and i != len(self.point_classes) - 2:
            otherP = self.point_classes[i + 2]
            centerP = self.point_classes[i + 1]
        elif i % 3 == 0 and i != 0 and i != len(self.point_classes) - 1:
            c = self.point_classes[i - 1].getCoords()
            self.point_classes[i - 1].setCoords((c[0] + move[0], c[1] + move[1]))
            c = self.point_classes[i + 1].getCoords()
            self.point_classes[i + 1].setCoords((c[0] + move[0], c[1] + move[1]))
            return
        else:
            return

        if not miror:
            d = -math.dist(otherP.getCoords(), centerP.getCoords()) / math.dist(p.getCoords(), centerP.getCoords())
        else:
            d = -1

        p2 = p.getCoords()
        p1 = centerP.getCoords()
        otherP.setCoords(((1 - d) * p1[0] + d * p2[0], (1 - d) * p1[1] + d * p2[1]))

    def updatePoints(self):
        self.point_group.update(self.display)

    def getPointsClicked(self, mx, my):
        return self.point_group.get_sprites_at((mx, my))

    def addCurve(self, points):
        assert len(points) == 3
        for p in points:
            self.point_classes.append(Point(p, self.point_group))
        self.points += points
        self.curves.append(CubicBezierCurve(
            [self.point_classes[-4], self.point_classes[-3], self.point_classes[-2], self.point_classes[-1]],
            self.display))

    def removeCurve(self):
        if len(self.curves) > 1:
            self.curves.pop()
            self.point_group.remove(self.point_classes[-1])
            self.point_group.remove(self.point_classes[-2])
            self.point_group.remove(self.point_classes[-3])
            self.point_classes = self.point_classes[:-3]
            self.points = self.points[:-3]

    def setPoints(self):
        self.points = [point.getCoords() for point in self.point_classes]

        change = False
        for curve in self.curves:
            if curve.setNewPoints():
                change = True
        return change


class Menu:
    def __init__(self, display, w, h, vals):
        self.buttons = []
        self.display = display
        self.button_group = pygame.sprite.LayeredUpdates()
        self.size = 200
        self.w = w
        self.h = h

        spread = 50
        self.buttons.append(Button(self.button_group, self.display, "Draw Lerps",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[0]))
        self.buttons.append(Button(self.button_group, self.display, "Draw Segments",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[1]))
        self.buttons.append(Button(self.button_group, self.display, "Draw Mid-Line",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[2]))
        self.buttons.append(Button(self.button_group, self.display, "Draw Points",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[3]))
        self.buttons.append(Button(self.button_group, self.display, "Draw Curve",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[4]))
        self.buttons.append(Button(self.button_group, self.display, "Draw Circle",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[5]))
        self.buttons.append(Button(self.button_group, self.display, "Draw Vectors",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[6]))
        self.buttons.append(Button(self.button_group, self.display, "Bounding Boxes",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[7]))
        self.buttons.append(Button(self.button_group, self.display, "Animation v2",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[8]))
        self.buttons.append(Button(self.button_group, self.display, "Allign Segments",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[9]))
        self.buttons.append(Button(self.button_group, self.display, "Mirror Segments",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[10]))
        self.buttons.append(Button(self.button_group, self.display, "Hide Points",
                                   (self.w - self.size + 10, len(self.buttons) * spread + 20), vals[11]))

    def draw(self):
        pygame.draw.rect(self.display, (34, 45, 56), pygame.Rect(self.w - self.size, 0, self.size, self.h))
        self.button_group.update()

    def getValues(self):
        return [b.enabled for b in self.buttons]


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

# TODO Add arrows to vectors
