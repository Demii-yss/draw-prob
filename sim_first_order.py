import random


def draw(total_draw):
    pre_draw = 100
    total_draw += pre_draw
    current_slot = random.choices([0, 1, 2], initial_prob)[0]
    result = [None]*total_draw
    lose_count = 0
    for i in range(total_draw):
        if current_slot == 2:
            lose_count += 1
        else:
            lose_count = 0

        if i == pre_draw-1:
            lose_count = 0

        if (lose_count >= 20) or (i == pre_draw+4 and lose_count == 5):
            current_slot = random.choices([0, 1], initial_prob[:2])[0]
            lose_count = 0

        result[i] = current_slot
        current_slot = random.choices([0, 1, 2], markov[current_slot])[0]

    return result[pre_draw:]

def getProb(results):
    count = {0: 0, 1: 1, 2: 2}
    for result in results:
        for r in result:
            count[r] += 1
    return [count[i]/sum([count[j] for j in range(3)]) for i in range(3)]

if __name__ == '__main__':
    initial_prob = [1/3, 1/3, 1/3]
    markov =   [[0.02815,0.01273,0.95912],
                [0.05809,0.20745,0.73447],
                [0.04934,0.07581,0.87485],
                    ]

    total_pop = 10000
    result = []
    prob = []
    for _ in range(total_pop):
        total_draw = random.randint(1, 200)
        r = draw(total_draw)
        result.append(r)
    prob.append(getProb(result))