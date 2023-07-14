import random
import numpy as np
import matplotlib.pyplot as plt

def simulate(initial_prob, markov):
    total_slot = 10000+100
    current_slot = random.choices([0, 1, 2], initial_prob)[0]
    result = [None]*total_slot
    trash_count = 0
    for i in range(total_slot):
        if current_slot == 0:
            trash_count += 1
        else:
            trash_count = 0

        if (trash_count >= 20) or (i == 5 and trash_count == 5):
            current_slot = random.choices([0, 1], initial_prob[:2])[0]
            trash_count = 0

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
    initial_prob = [0.8, 0.1, 0.1]
    markov = [[0.0001, 0.1044, 0.8955], [0.0001, 0.3402, 0.6597], [0.2712, 0.2296, 0.4992]]
    #
    refine_time = 100000
    dx = random.random()*0.01
    #
    for refine in range(refine_time):
        tur_idx = random.randint(0, 9)
        current_score = getScore(simulate(initial_prob, markov))
        if tur_idx < 9:
            turb = 'markov'
            pos_dx_score = getScore(simulate(initial_prob, getTurbMkv(markov, tur_idx, dx)))
            neg_dx_score = getScore(simulate(initial_prob, getTurbMkv(markov, tur_idx, -dx)))
        else:
            turb = 'init'
            tur_idx -= 9
            pos_dx_score = getScore(simulate(getTurbInitProb(initial_prob, tur_idx, dx), markov))
            neg_dx_score = getScore(simulate(getTurbInitProb(initial_prob, tur_idx, -dx), markov))

        if pos_dx_score < neg_dx_score and pos_dx_score < current_score:
            if turb == 'markov':
                markov = getTurbMkv(markov, tur_idx, dx)
            elif turb == 'init':
                initial_prob = getTurbInitProb(initial_prob, tur_idx, dx)
            print(pos_dx_score)
        elif neg_dx_score < pos_dx_score and neg_dx_score < current_score:
            if turb == 'markov':
                markov = getTurbMkv(markov, tur_idx, -dx)
            elif turb == 'init':
                initial_prob = getTurbInitProb(initial_prob, tur_idx, -dx)
            print(neg_dx_score)
        else:
            print(current_score)
            pass

        # Plot
        if not refine % 50:
            # pyautogui.click(1500, 100)
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

