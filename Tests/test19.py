def pointOnLine(p1, p2, t):
    return (p2[0] - p1[0]) * t + p1[0], (p2[1] - p1[1]) * t + p1[1]

print(pointOnLine((0, 0), (1, 1), 0.5))