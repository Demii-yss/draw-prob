import random

def draw(total_draw):
    result = [None]*total_draw
    lose_count = 0
    for i in range(total_draw):
        current_slot = random.choices([0, 1, 2], [0.05, 0.10, 0.85], k=1)[0]
        if current_slot == 2:
            lose_count += 1
        else:
            lose_count = 0

        if (lose_count >= 20) or (i == 5 and lose_count == 5):
            current_slot = random.choices([0, 1], [0.05, 0.10], k=1)[0]
            lose_count = 0

        result[i] = current_slot
    return result

def getProb(results):
    count = {0: 0, 1: 1, 2: 2}
    for result in results:
        for r in result:
            count[r] += 1
    return [count[i]/sum([count[j] for j in range(3)]) for i in range(3)]

if __name__ == '__main__':
    total_pop = 10000
    result = []
    prob = []
    for _ in range(total_pop):
        total_draw = random.randint(1, 200)
        r = draw(total_draw)
        result.append(r)
    prob.append(getProb(result))