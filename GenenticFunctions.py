import random
import numpy as np
def crossover(parent1, parent2):
    weight1 = parent1.get_weights()
    weight2 = parent2.get_weights()

    new_weight1 = weight1
    new_weight2 = weight2

    gene = random.randint(0,len(new_weight1)-1)

    new_weight1[gene]=weight2[gene]
    new_weight2[gene]=weight1[gene]

    return np.asarray([new_weight1, new_weight2])

def mutate(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if( random.uniform(0,1) > .90):
                change = random.uniform(-.5,.5)
                weights[i][j] += change
    return weights
