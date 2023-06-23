import pygame, time, math
import random
from random import randint as ri
from random import choice as ch


class Sampling:
    def __init__(self, width, height, candidate_samples, inner_circle_radius, outer_circle_radius, gamedisplay, circle_size):
        self.width = width
        self.height = height
        self.gamedisplay = gamedisplay
        self.inner_circle_radius = inner_circle_radius
        self.outer_circle_radius = outer_circle_radius
        self.circle_size = circle_size
        self.points = []
        self.available_points = []
        self.createPoints(candidate_samples)

    def draw(self, specific_point, all=False):
        if all:
            self.gamedisplay.fill((0, 0, 0))
            for point in self.points:
                if point in self.available_points:
                    color = (255, 255, 255)
                else:
                    color = (255, 0, 0)
                pygame.draw.circle(self.gamedisplay, color, (point[1], point[0]), self.circle_size)
        else:
            if specific_point in self.available_points:
                color = (255, 255, 255)

            else:
                color = (255, 0, 0)
            pygame.draw.circle(self.gamedisplay, color, (specific_point[1], specific_point[0]),
                               self.circle_size)
        pygame.display.update()

    def checkEvents(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()

    def getPoints(self):
        return self.points

    def distance(self, other_point, current_point):
        vector = (current_point[0] - other_point[0], current_point[1] - other_point[1])
        dis = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

        # dis = abs(other_point[0] - current_point[0]) + abs(other_point[1] - current_point[1])
        if dis <= self.inner_circle_radius:
            return None
        else:
            return dis

    def createPoints(self, candidate_samples):
        current_point = (ri(0, self.height), ri(0, self.width))
        self.points.append(current_point)
        self.available_points.append(current_point)

        while True:
            finished = False
            for i in range(candidate_samples):
                self.checkEvents()
                if current_point[0] - self.inner_circle_radius > 0 and current_point[0] + self.inner_circle_radius < self.height and \
                        current_point[1] - self.inner_circle_radius > 0 and current_point[
                    1] + self.inner_circle_radius < self.width:

                    num = 3
                    if num == 1:
                        new_candidate = (
                            ri(current_point[0] - self.inner_circle_radius, current_point[0] + self.inner_circle_radius),
                            ri(current_point[1] - self.inner_circle_radius, current_point[1] + self.inner_circle_radius))
                    elif num == 2:
                        x = ri(self.inner_circle_radius+1, self.outer_circle_radius)
                        y = ri(0, self.outer_circle_radius-x)

                        # Random choice to be negative
                        if ch([True, False]): x = -x
                        if ch([True, False]): y = -y
                        new_candidate = (current_point[0] + y, current_point[1] + x)
                    elif num == 3:
                        angle = random.random() * 2 * math.pi
                        core = random.random()
                        if core < (self.inner_circle_radius / self.outer_circle_radius): core += (self.inner_circle_radius / self.outer_circle_radius)
                        dis = math.sqrt(core) * self.outer_circle_radius

                        new_candidate = (int(current_point[0] + dis * math.sin(angle)), int(current_point[1] + dis * math.cos(angle)))
                    elif num == 4:
                        x = ri(0, self.outer_circle_radius - self.inner_circle_radius + 1)
                        y = ri(self.inner_circle_radius - x + 1, self.outer_circle_radius - x)

                        # Random choice to be negative
                        if ch([True, False]): x = -x
                        if ch([True, False]): y = -y
                        new_candidate = (current_point[0] + y, current_point[1] + x)
                    elif num == 5:
                        x = ri(self.inner_circle_radius + 1, self.outer_circle_radius)
                        print(x, self.inner_circle_radius + 1, self.outer_circle_radius)
                        print(self.outer_circle_radius - x)
                        y = ri(0, self.outer_circle_radius - x) + self.inner_circle_radius
                        # Random choice to be negative
                        if ch([True, False]): x = -x
                        if ch([True, False]): y = -y
                        new_candidate = (current_point[0] + y, current_point[1] + x)
                    elif num == 6:
                        x = ri(0, self.outer_circle_radius)
                        print(x, self.inner_circle_radius + 1, self.outer_circle_radius)
                        print(self.outer_circle_radius - x)
                        y = ri(0, self.outer_circle_radius - x)
                        # Random choice to be negative
                        if ch([True, False]): x = -x
                        if ch([True, False]): y = -y
                        new_candidate = (current_point[0] + y, current_point[1] + x)
                    elif num == 7:
                        if ch([True, False]):
                            x = ri(self.inner_circle_radius + 1, self.outer_circle_radius)
                            y = ri(0, self.outer_circle_radius - x)
                        else:
                            y = ri(self.inner_circle_radius + 1, self.outer_circle_radius)
                            x = ri(0, self.outer_circle_radius - y)
                        # Random choice to be negative
                        if ch([True, False]): x = -x
                        if ch([True, False]): y = -y
                        new_candidate = (current_point[0] + y, current_point[1] + x)
                    # print(new_candidate, current_point)
                    print(new_candidate)
                    self.points.append(new_candidate)
                    self.draw(None, True)
                    # distances = list(set(list(map(self.distance, self.points, [new_candidate] * len(self.points)))))
                    # if None not in distances:
                    #     self.points.append(new_candidate)
                    #     self.available_points.append(new_candidate)
                    #     finished = True
                    #     break

            if not finished:
                self.available_points.remove(current_point)



            if len(self.available_points) > 0:
                current_point = ch(self.available_points)
            else:
                break
