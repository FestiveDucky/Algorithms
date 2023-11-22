from decimal import Decimal
def inverseFactorial(n):
    product = Decimal(1)
    for i in range(1, n+1):
        product *= Decimal(1) - (Decimal(i)/Decimal(100))
    return product

a = 4
s = Decimal(0)
for i in range(1, a + 1):
    s += inverseFactorial(i-1)
    print(inverseFactorial(i-1))
print(s)

import random

n = 100
total = 0
s = 0
while True:
    win = 0
    prob = 1
    for i in range(1, n + 1):
        if random.randint(1, 101) <= prob:
            win += 1
            prob = 0
        prob += 1

    total += 1
    s += win
    print(f"Average: {round(s/total,5)}, Total: {total}, Expected: {round(n/(s/total), 5)}")

# total = 0
# s = 0
# while True:
#     for i in range(1, 101):
#         if random.randint(1, 100) <= i:
#             s += i
#             break
#     total += 1
#     print(f"Average: {round(s/total,5)}")