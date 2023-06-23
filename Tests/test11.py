import math


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

print(calculateNewCoords((5, 0), 10, 90))
print(reverseAngle((5, 0), calculateNewCoords((5, 0), 10, 90)))