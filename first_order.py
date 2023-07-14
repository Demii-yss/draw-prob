import random
import numpy as np
import matplotlib.pyplot as plt

def simulate(initial_prob, markov):
    total_draw = 10000
    pre_draw = 100
    #
    total_draw += pre_draw
    current_slot = random.choices([0, 1, 2], initial_prob)[0]
    result = [None]*total_draw
    lose_count = 0
    for i in range(total_draw):
        if current_slot == 0:
            lose_count += 1
        else:
            lose_count = 0

        if (lose_count >= 20) or (i == pre_draw+4 and lose_count >= 5):
            current_slot = random.choices([0, 1], initial_prob[:2])[0]
            lose_count = 0

        result[i] = current_slot
        current_slot = random.choices([0, 1, 2], markov[current_slot])[0]

    return result[100:]


def generateProbTrip():
    p1 = random.random()
    p2 = (1 - p1) * random.random()
    return p1, p2, 1 - p1 - p2


def isValidProb(p):
    for x in p:
        if not 0.0001 <= x <= 1:
            return False
    return True

def getTurbInitProb(initial_prob, idx, dx):
    isFirstLoop = True
    while isFirstLoop or not isValidProb(add):
        add = [-dx / 2]*3
        add[idx] += 3 * dx / 2
        add = np.add(initial_prob, add)
        dx /= 2
        isFirstLoop = False
    return add

def getTurbMkv(markov, idx, dx):
    isFirstLoop = True
    while isFirstLoop or not isValidProb(add[idx//3]):
        add = [[-dx / 2 if i == idx // 3 else 0]*3 for i in range(3)]
        add[idx // 3][idx % 3] += 3 * dx / 2
        add = np.add(markov, add)

        dx /= 2
        isFirstLoop = False
    return add

def getScore(result):
    count = {0: 0, 1: 0, 2: 0}
    for r in result:
        count[r] += 1
    return (count[0]/len(result)-0.04)**2 + (count[1]/len(result)-0.09)**2


if __name__ == '__main__':
    plt.ion()
    plt.show()
    #
    initial_prob = generateProbTrip()
    markov = [generateProbTrip() for _ in range(3)]
    #
    refine_time = 100000
    #
    for refine in range(refine_time):
        dx = random.random()*0.01
        tur_idx = random.randint(0, 8)
        current_score = getScore(simulate(initial_prob, markov))
        pos_dx_score = getScore(simulate(initial_prob, getTurbMkv(markov, tur_idx, dx)))
        neg_dx_score = getScore(simulate(initial_prob, getTurbMkv(markov, tur_idx, -dx)))

        if pos_dx_score < neg_dx_score and pos_dx_score < current_score:
            markov = getTurbMkv(markov, tur_idx, dx)
        elif neg_dx_score < pos_dx_score and neg_dx_score < current_score:
            markov = getTurbMkv(markov, tur_idx, -dx)

        # Plot
        if not refine % 50:
            fig, ax = plt.subplots(1, 1)
            ax.axis('tight')
            ax.axis('off')

            display = [[round(m, 4) for m in row] for row in markov]
            colors = [[((1-m)/2+0.5, (1-m)/2+0.5, (1-m)/2+0.5) for m in row] for row in display]
            table = ax.table(cellText=display, loc="center", cellColours=colors)
            table.auto_set_font_size(False)
            table.set_fontsize(24)
            table.scale(1, 8)
            plt.draw()
            plt.pause(0.001)

