import math

points = [(1, 2), (3, 7), (5, 6), (7, 7)]


def firstDerivative(t):
    final_vector = [0, 0]
    n = len(points) - 1
    for i in range(n):
        scalar = bValue(n - 1, i, t) * n * t
        final_vector[0] += scalar * (points[i + 1][0] - points[i][0])
        final_vector[1] += scalar * (points[i + 1][1] - points[i][1])
    return tuple(final_vector)


def secondDerivative(t):
    final_vector = [0, 0]
    n = len(points) - 1
    for i in range(n - 1):
        scalar = bValue(n - 2, i, t) * n * (n - 1)
        print(bValue(n - 2, i, t))
        final_vector[0] += scalar * (points[i + 2][0] - 2 * points[i + 1][0] + points[i][0])
        final_vector[1] += scalar * (points[i + 2][1] - 2 * points[i + 1][1] + points[i][1])
    return tuple(final_vector)


def bValue(n, i, t):
    # n is the degree of the bezier curve meaning n + 1 is the number of control points\
    # Formulas found here https://pages.mtu.edu/~shene/COURSES/cs3621/NOTES/spline/Bezier/bezier-der.html
    return math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))


def curvatureRadius(t):
    f = firstDerivative(t)
    s = secondDerivative(t)
    numerator = abs(f[0] * s[1] - f[1] * s[0])
    denominator = ((f[0] ** 2) + (f[1] ** 2)) ** (1.5)
    if denominator == 0 or numerator == 0:
        print("Undefined Curvature (A line)")
    else:
        k = numerator / denominator
        return 1. / k


print(curvatureRadius())
