import random as r


def getSign(x):
    if x < 0:
        return "-"
    return "+"


while True:
    try:
        print("1 - Easy, 2 - Medium, 3 - Hard, 4 - Impossible")
        d = int(input("Difficulty: "))
        if d not in [1, 2, 3, 4]:
            raise InterruptedError
        break
    except:
        print("Not a valid input!")

while True:
    print("\n")
    answers = r.choice([[r.randint(1, 5), r.randint(-5, -1)], [r.randint(1, 5), r.randint(1, 5)],
                        [r.randint(-5, -1), r.randint(-5, -1)]])
    if d == 3:
        answers = r.choice([[r.randint(1, 15), r.randint(-15, -1)], [r.randint(1, 15), r.randint(1, 15)],
                            [r.randint(-15, -1), r.randint(-15, -1)]])
    elif d == 4:
        answers = r.choice([[r.randint(1, 50), r.randint(-50, -1)], [r.randint(1, 50), r.randint(1, 50)],
                            [r.randint(-50, -1), r.randint(-50, -1)]])

    m1, m2 = "", ""
    if d == 2:
        m1 = r.randint(2, 3)
    elif d == 3:
        m1 = r.randint(2, 3)
    elif d == 4:
        m1, m2 = r.randint(2, 8), r.randint(2, 8)

    s1, s2 = 1, 1
    if d > 1:
        s1 = m1
    if d == 4:
        s2 = m2

    answers[0] /= s1
    answers[1] /= s2

    print("Solve using factoring.")
    a = s1 * s2
    b = (s2 * (-answers[0] * s1)) + (s1 * (-answers[1] * s2))
    c = (-answers[0] * s1) * (-answers[1] * s2)
    aDisplay, bDisplay, cDisplay = a, abs(round(b)), abs(round(c))
    if a == 1:
        aDisplay = ""
    if b == 1:
        bDisplay = ""
    print(f"{aDisplay}x² {getSign(b)} {bDisplay}x {getSign(c)} {cDisplay} = 0")

    while True:
        try:
            a1 = float(input("Enter First Answer: "))
            a2 = float(input("Enter Second Answer: "))
            break
        except:
            print("Not a valid input!")

    print()

    if [a1, a2] == answers or [a2, a1] == answers:
        print("Correct!")
    elif a1 in answers or a2 in answers:
        print("1/2 Correct!")
    else:
        print("Incorrect")

    print()
    print(
        f"Factored: ({m1}x {getSign(-answers[0])} {round(abs(answers[0]) * s1)})({m2}x {getSign(-answers[1])} {round(abs(answers[1]) * s2)}) = 0")
    print(f"x = {answers[0]}, {answers[1]}")
