import threading, time

class M:
    def __init__(self):
        self.count = 0



def a(master):
    for i in range(50000):
        master.count += 1
    for i in range(50000):
        master.count += 1

mainClass = M()

c = 100

times = []
for i in range(c):
    start = time.time()
    a(mainClass)
    print(time.time() - start)
    mainClass.count = 0
    times.append(time.time() - start)
print("Average: " + str(sum(times) / c))