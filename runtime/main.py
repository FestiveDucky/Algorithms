import time


def rT(func, *arg):
    start = time.time_ns()
    for i in range(10000):
        func(*arg)
    print(time.time_ns() - start)


def mult(x, y):
    return x * y


print(rT(mult, 5, 10))
