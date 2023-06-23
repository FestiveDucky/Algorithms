import time


def sqr(x):
    return x*x

a = range(1000000)

start = time.time()
b = []
for i in a:
    b.append(sqr(i))
print(f"Loop Time: {time.time() - start}")

start = time.time()
list(map(sqr, a))
print(f"Map Time: {time.time() - start}")