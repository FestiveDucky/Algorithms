import random, decimal

while True:
    n = 10
    print("-------------------")
    l1 = []
    l2 = []
    for i in range(n):
        l1.append(random.randint(0, 100))
        l2.append(random.randint(0, 100))

    l1.sort()
    l2.sort()

    l3 = l1[:] + l2[:]
    l3.sort()

    print("MEDIAN", l3[n - 1], l3[n], (l3[n - 1] + l3[n]) / 2)


    m = [l3[n - 1], l3[n]]
    lv = [-1, 100000]
    for i in range(n):
        print(i, l1[i], l2[n - i - 1], (l1[i]+ l2[n - i - 1])/2, abs(l1[i] - l2[n - i - 1]))
        if abs(l1[i] - l2[n - i - 1]) < lv[1]:
            lv = [i, abs(l1[i] - l2[n - i - 1])]

    v = [l1[lv[0]], l2[n - lv[0] - 1]]
    best = v[:] + [abs(l1[lv[0]] - l2[n - lv[0] - 1])]

    for i in [l1[lv[0]-1], l2[n - lv[0] - 2], l1[lv[0]+1], l2[n - lv[0]]]:
        if abs(v[0] - i) < best[2]:
            best = [v[0], i, abs(v[0] - i)]
        elif abs(v[1] - i) < best[2]:
            best = [v[1], i, abs(v[1] - i)]
    print("CALCULATED MEDIAN", best)



