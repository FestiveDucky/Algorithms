import time


def decimal_to_fraction(d):
    f1 = [0, 1]
    f2 = [1, 1]
    while True:
        f3 = [f1[0] + f2[0], f1[1] + f2[1]]
        if d > (f3[0] / f3[1]):
            f1 = f3[:]
        elif d < (f3[0] / f3[1]):
            f2 = f3[:]
        else:
            return f"{f3[0]}/{f3[1]} = {d}"

        print(f"{f1[0]}/{f1[1]} - {f2[0]}/{f2[1]}")


print(decimal_to_fraction(float(input())))
