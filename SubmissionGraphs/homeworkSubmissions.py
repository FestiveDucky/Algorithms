import matplotlib.pyplot as plt
import datetime
import time

month = {"Jun": 6, "Jul": 7}


def toUnix(vals):
    hours = int(vals[3].split(":")[0])
    if ("PM" in vals[3] and "12" not in vals[3]) or ("12" in vals[3] and "AM" in vals[3]):
        hours += 12
    if hours == 24:
        hours = 0

    if len(vals[3]) == 6:
        minutes = int(vals[3][2:4])
    else:
        minutes = int(vals[3][3:5])
    return time.mktime(datetime.datetime(2023, month[vals[0]], int(vals[1]), hours, minutes).timetuple())


count = int(input("Number of People: "))
# ,
data = [toUnix(input("Start Time: ").split()), toUnix(input("End Time: ").split())]
for i in range(count):
    v = input().split("\t")[-1].split()
    data.append(toUnix(v))

data = sorted(data)
plt.plot(data, range(count + 2))
plt.ylabel("Number of Submissions")
plt.xlabel("Unix Time")
plt.show()
