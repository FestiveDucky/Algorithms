import threading, time

class M:
    def __init__(self):
        self.count = 0



class A(threading.Thread):
    def __init__(self, master):
        super().__init__()
        self.master = master

    def run(self):
        for i in range(50000):
            self.master.count += 1

mainClass = M()

c = 100

times = []
for i in range(c):
    start = time.time()
    one = A(mainClass)
    two = A(mainClass)
    one.start()
    two.start()
    while mainClass.count != 100000:
        # print(mainClass.count)
        pass
    print(time.time() - start)
    mainClass.count = 0
    times.append(time.time() - start)
print("Average: " + str(sum(times) / c))