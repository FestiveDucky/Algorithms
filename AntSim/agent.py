import datetime
import time
import timeit

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
        self.carryingFood = False
        self.birthTime = time.time()
        averageLivingTime = 180
        self.lifeSpan = random.randint(averageLivingTime - 15, averageLivingTime + 15) + random.random()

    def adjust2(self, screen):
        # Values are [food y, food x, home y, home x]
        possibleMoves = []
        pheromoneSums = [0, 0, 0, 0]
        # 40%
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                # Check that it is within bounds of screen
                if not (0 <= dy + self.coords[0] < screen.tile_height and 0 <= dx + self.coords[1] < screen.tile_length):
                    continue

                # Adds up the amount of pheromone around the agent
                if (dy, dx) != (0, 0) and abs(minAngleBetweenAngles(self.angle, precalculatedAngles[(dy, dx)])) <= 80:
                    possibleMoves.append((dy, dx))
                    pheromoneSums[0] += screen.boardFood[dy + self.coords[0]][dx + self.coords[1]] * dy
                    pheromoneSums[1] += screen.boardFood[dy + self.coords[0]][dx + self.coords[1]] * dx
                    pheromoneSums[2] += screen.boardHome[dy + self.coords[0]][dx + self.coords[1]] * dy
                    pheromoneSums[3] += screen.boardHome[dy + self.coords[0]][dx + self.coords[1]] * dx

        # Change which pheromone we prioritize based on whether we have food
        # [0.5, 0.1]
        maxPercent = [1, 0.1]
        maxPercent = [1, 100]
        if not self.carryingFood:
            maxPercent = [0, 100]

        # 10%
        scaling = 1
        # Calculates how much the angle should change based on paths nearby going towards food
        foodAngle = calculateAngle((0, 0), (pheromoneSums[0], pheromoneSums[1]))
        foodMagnitude = maxPercent[0] * (abs(pheromoneSums[0]) + abs(pheromoneSums[1])) * 0.25 * scaling
        if foodMagnitude > 1:
            foodMagnitude = 1
        foodAngleChange = minAngleBetweenAngles(self.angle, foodAngle) * foodMagnitude

        # Calculates how much the angle should change based on paths nearby going towards the nest
        homeAngle = calculateAngle((0, 0), (pheromoneSums[2], pheromoneSums[3]))
        homeMagnitude = maxPercent[1] * (abs(pheromoneSums[2]) + abs(pheromoneSums[3])) * 0.25 * scaling
        if homeMagnitude > 1:
            homeMagnitude = 1
        homeAngleChange = minAngleBetweenAngles(self.angle, homeAngle) * homeMagnitude

        foodAngleChange = 0
        homeAngleChange = 0

        # print("-----------------------")
        # print(self.lifeSpan)
        # print(foodAngleChange, foodMagnitude, foodAngle, pheromoneSums, minAngleBetweenAngles(self.angle, foodAngle))
        # print(homeAngleChange, homeMagnitude, homeAngle, pheromoneSums, minAngleBetweenAngles(self.angle, homeAngle))
        # print(self.angle)

        # 4%
        # Pulls angle towards nest depending on whether the agent is carrying food
        guidingAngle = 0
        if len(screen.nests) > 0:
            weight = 0.1
            angleToNest = calculateAngle(self.coords, screen.nests[0].coords)
            if self.carryingFood:
                # Attraction to nest when we have food
                guidingAngle = weight * minAngleBetweenAngles(self.angle, angleToNest)
            else:
                # Repulsion from nest when we don't have food
                angleToNest -= 180
                if angleToNest < 0:
                    angleToNest += 360
                # Multp by 0.5 worled very well, but was a bit too high as all of the agents not on the paths collected up into the corners
                estimatedFarthestDistance = screen.length + screen.height
                distanceRatio = ((estimatedFarthestDistance - math.dist(screen.nests[0].coords, self.coords))/estimatedFarthestDistance)
                distanceRatio = 1
                guidingAngle = weight * minAngleBetweenAngles(self.angle, angleToNest) * 0.1 * distanceRatio

        # Adds randomness to the paths so that they don't just travel like arrows
        randomAngle = random.randint(-20, 20)
        self.angle += foodAngleChange + homeAngleChange + guidingAngle + randomAngle
        if self.angle < 0:
            self.angle += 360
        elif self.angle >= 360:
            self.angle -= 360

        self.move(screen)
        # self.move2(screen, possibleMoves)

    def move(self, screen, package=None):
        # 10%
        if package is None:
            next_trig_coords = calculateNewCoords(self.trigCoords, self.speed, self.angle)
        else:
            # Get midpoint (WORKS ONLY FOR SPEED OF 1)
            next_trig_coords = ((package[0] + self.trigCoords[0]) / 2, (package[1] + self.trigCoords[1]) / 2)
        next_coords = (round(next_trig_coords[0]), round(next_trig_coords[1]))

        angle_of_change = 40

        # If we are going to go past a wall, reverse our angle (with a bit of randomness) and then run the move again
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

        # Complete the move and update the board
        self.trigCoords = next_trig_coords
        self.coords = next_coords
        if self.carryingFood:
            screen.boardHome[next_coords[0]][next_coords[1]] = 1
        else:
            screen.boardFood[next_coords[0]][next_coords[1]] = 1

    # def move2(self, screen, moves):
    #     # basically just choose a point in front of you with the highest value
    #     best = (-1, (0, 0))
    #     for move in moves:
    #         if self.carryingFood:
    #             score = screen.boardFood[move[0] + self.coords[0]][move[1] + self.coords[1]]
    #         else:
    #             score = screen.boardHome[move[0] + self.coords[0]][move[1] + self.coords[1]]
    #         if score > best[0]:
    #             best = (score, move)
    #
    #     self.coords = (best[1][0] + self.coords[0], best[1][1] + self.coords[1])
    #     if self.carryingFood:
    #         screen.boardHome[self.coords[0]][self.coords[1]] = 1
    #     else:
    #         screen.boardFood[self.coords[0]][self.coords[1]] = 1

    def update(self, screen):
        # Gives the agents a lifespan
        if time.time() > self.birthTime + self.lifeSpan:
            screen.agents.remove(self)
            self.kill()

        # Moves the agent
        self.adjust2(screen)

        # Checks if the agent has reached food
        if not self.carryingFood:
            for food in screen.food:
                if self.coords == food.coords:
                    self.carryingFood = True
                    self.angle -= 180
                    if self.angle < 0:
                        self.angle += 360
                    self.lifeSpan += 10
                    food.quantity -= 1

        # Checks if the agent has reached its nest
        else:
            for nest in screen.nests:
                if nest.coords == self.coords:
                    self.carryingFood = False
                    self.angle -= 180
                    if self.angle < 0:
                        self.angle += 360
                    nest.storedFood += 1


def calculateAngle(p1, p2):
    # p1 is your point, p2 is other point
    angle = math.degrees(math.atan2(p2[0] - p1[0], p2[1] - p1[1]))
    if angle < 0:
        angle += 360
    return angle


def minAngleBetweenAngles(a1, a2):
    # Angles must be between 0 - 359, a1 is your angle
    # Returned sign indicates whether the shortest angle is clockwise (+) or ccw (-)

    largerAngle = max(a1, a2)
    smallerAngle = min(a1, a2)
    dist = largerAngle - smallerAngle
    sign = 1
    if dist > 180:
        sign *= -1
        dist = 360 - dist
    if largerAngle == a1:
        sign *= -1

    return dist * sign


precalculatedAngles = {}
for y in [-1, 0, 1]:
    for x in [-1, 0, 1]:
        if (y, x) != (0, 0):
            angle = calculateAngle((0, 0), (y, x))
            if angle < 0:
                angle += 360
            precalculatedAngles[(y, x)] = angle
print(precalculatedAngles)
