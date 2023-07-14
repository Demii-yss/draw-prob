import random
import numpy as np
import csv

def simulate(initial_prob, markov):
    total_slot = 10000+2
    result = [None]*total_slot
    result[0] = random.choices([2, 1, 0], initial_prob)[0]
    result[1] = random.choices([2, 1, 0], initial_prob)[0]
    trash_count = 0
    for i in range(2, total_slot):
        current_slot = random.choices([0, 1, 2], markov[result[i-2]][result[i-1]])[0]
        if current_slot == 2:
            trash_count += 1
        else:
            trash_count = 0

        if (trash_count >= 20) or (i == 5 and trash_count == 5):
            current_slot = random.choices([0, 1], initial_prob[:2])[0]
            trash_count = 0

        result[i] = current_slot

    return result[3:]


def generateProbTrip():
    p1 = random.random()
    p2 = (1 - p1) * random.random()
    return p1, p2, 1 - p1 - p2


def isValidProb(p):
    for x in p:
        if not 0 <= x <= 1:
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
    i = idx//9
    j = idx%9
    p = j//3
    q = j%3
    while isFirstLoop or not isValidProb(add[i][p]):
        add = [[[0 for _ in range(3)] for __ in range(3)] for ___ in range(3)]
        add[i][p] = [-dx/2]*3
        add[i][p][q] += 3 * dx / 2
        add = np.add(markov, add)

        dx /= 2
        isFirstLoop = False
    return add

def getScore(result):
    count = {0: 0, 1: 0, 2: 0}
    for r in result:
        count[r] += 1
    return (count[0]/len(result)-0.05)**2 + (count[1]/len(result)-0.1)**2


if __name__ == '__main__':
    initial_prob = [1/3, 1/3, 1/3]
    markov = [[generateProbTrip() for _ in range(3)] for __ in range(3)]
    #
    refine_time = 10000
    dx = random.random()*0.05
    best_score = 1
    statisfies_count = 0
    #
    while statisfies_count < 1000:
        tur_idx = random.randint(0, 26)
        current_score = getScore(simulate(initial_prob, markov))
        pos_dx_score = getScore(simulate(initial_prob, getTurbMkv(markov, tur_idx, dx)))
        neg_dx_score = getScore(simulate(initial_prob, getTurbMkv(markov, tur_idx, -dx)))

        if pos_dx_score < neg_dx_score and pos_dx_score < current_score:
            markov = getTurbMkv(markov, tur_idx, dx)
            best_score = pos_dx_score
        elif neg_dx_score < pos_dx_score and neg_dx_score < current_score:
            markov = getTurbMkv(markov, tur_idx, -dx)
            best_score = neg_dx_score
        else:
            best_score = current_score

        print(best_score)
        if best_score < 0.0001:
            statisfies_count += 1
        else:
            statisfies_count = max(0, statisfies_count-500)

    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for s in markov:
            writer.writerows(s)

