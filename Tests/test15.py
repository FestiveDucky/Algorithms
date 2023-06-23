import random
import multiprocessing
import sys
import time
sys.setrecursionlimit(1000000)

def QsortDeter(array, low, high):
    global total, a
    if (low < high):
        pivot = low
        i = low
        j = high

        while (i < j):  # Main While Loop
            while array[i] <= array[pivot] and i < high:  # While Loop "i"
                i += 1
                total += 1
            while array[j] > array[pivot]:  # While Loop "j"
                j -= 1
                total += 1

            if (i < j):
                array[i], array[j] = array[j], array[i]

        array[pivot], array[j] = array[j], array[pivot]
        QsortDeter(array, low, j - 1)
        QsortDeter(array, j + 1, high)
        return array

    else:
        return array


def QsortRand(array, low, high):
    global total, a
    if (low < high):
        pivot = random.randint(low, high)
        i = low
        j = high

        while (i < j):  # Main While Loop
            while array[i] <= array[pivot] and i < high:  # While Loop "i"
                i += 1
                total += 1
            while array[j] > array[pivot]:  # While Loop "j"
                j -= 1
                total += 1

            if (i < j):
                array[i], array[j] = array[j], array[i]

        array[pivot], array[j] = array[j], array[pivot]
        QsortRand(array, low, j - 1)
        QsortRand(array, j + 1, high)
        return array

    else:
        return array

dave = 0
rave = 0
i = 0
total = 0
while True:
    a = [random.randint(1, 100) for x in range(100000)]
    i += 1
    total = 0
    QsortDeter(a[:], 0, len(a) - 1)
    dave += total
    total = 0
    QsortRand(a[:], 0, len(a) - 1)
    rave += total
    if i % 1 == 0:
        print("---------------")
        print(f"Deterministic Ave: {round(dave/i, 4)}\nRandom Ave: {round(rave/i,4)}")

# 33.2192809