import random

prevEdges = []
n = 4
e = 6
for i in range(e):
    v1 = random.randint(0, n - 1)
    v2 = random.randint(0, n - 1)
    while v1 == v2:
        v2 = random.randint(0, n - 1)
    # Directed
    # while (v1, v2) in prevEdges:
    while (v1, v2) in prevEdges or (v2, v1) in prevEdges:
        v1 = random.randint(0, n-1)
        v2 = random.randint(0, n-1)
        while v1 == v2:
            v2 = random.randint(0, n-1)
    prevEdges.append((v1, v2))
    w = random.randint(-10, 10)
    # print(f"g.addEdge({v1}, {v2}, {w});")
    # print(f"g.addEdge({v2}, {v1}, {w});")
    print(v1, v2, w)