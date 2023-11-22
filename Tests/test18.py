import math

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

def adjust2():
    # Values are [food y, food x, home y, home x]
    pheromoneSums = [0, 0, 0, 0]
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            # Check that it is within bounds of screen
            if not (0 <= dy + coords[0] < yheight and 0 <= dx + coords[1] < xheight):
                continue

            if (dy, dx) != (0, 0) and abs(minAngleBetweenAngles(angle, precalculatedAngles[(dy, dx)])) <= 50:
                pheromoneSums[0] += boardFood[dy + coords[0]][dx + coords[1]] * dy
                pheromoneSums[1] += boardFood[dy + coords[0]][dx + coords[1]] * dx
                print(boardFood[dy + 0][dx + 1], (dy, dx))
                # pheromoneSums[2] += screen.boardHome[dy + self.coords[0]][dx + self.coords[1]] * dy
                # pheromoneSums[3] += screen.boardHome[dy + self.coords[0]][dx + self.coords[1]] * dx

    foodAngle = calculateAngle((0, 0), (pheromoneSums[0], pheromoneSums[1]))
    # 50% is max value of magnitudes
    maxPerc = 0.5
    foodMagnitude = maxPerc * (abs(pheromoneSums[0]) + abs(pheromoneSums[1])) * 0.25
    newFoodAngle = minAngleBetweenAngles(angle, foodAngle) * foodMagnitude + angle
    if newFoodAngle < 0:
        newFoodAngle += 360
    elif newFoodAngle >= 360:
        newFoodAngle -= 360

    print(newFoodAngle, foodMagnitude, foodAngle, pheromoneSums, minAngleBetweenAngles(angle, foodAngle))


precalculatedAngles = {}
for y in [-1, 0, 1]:
    for x in [-1, 0, 1]:
        if (y, x) != (0, 0):
            angle = calculateAngle((0, 0), (y, x))
            if angle < 0:
                angle += 360
            precalculatedAngles[(y, x)] = angle

coords = (2, 2)
yheight = 3
xheight = 3
angle = 180
boardFood = [[0.01, 0.4, 0.2],
             [0.5, 0.0, 0.1],
             [0.3, 0.7, 0.9]]

adjust2()

