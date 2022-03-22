import numpy as np
import random
import NeuralNet

def inflate(flat, shapes):
    output = []
    index = 0
    for shape in shapes:
        size = np.product(shape)
     
        output.append(flat[index: index + size].reshape(shape))
        index += size
    return output

def crossover(survivors, pop_size):
    children = []
    for i in range((pop_size)//2):
        parent1 = random.choice(survivors)
        parent2 = random.choice(survivors)
        child1 = NeuralNet.NeuralNet(5, 4, 5, 4)
        child2 = NeuralNet.NeuralNet(5, 4, 5, 4)

        Wshapes = [a.shape for a in parent1.getWeights() ]

        p1_Wgenes = np.concatenate([a.flatten() for a in parent1.getWeights()])
        p2_Wgenes = np.concatenate([a.flatten() for a in parent2.getWeights()])

        split_point = random.randint(0,len(p1_Wgenes)-1)

        c1_Wgenes = np.asarray(p1_Wgenes[0:split_point].tolist() + p2_Wgenes[split_point:].tolist())
        c2_Wgenes = np.asarray(p1_Wgenes[0:split_point].tolist() + p2_Wgenes[split_point:].tolist())

        child1.setWeights(inflate(c1_Wgenes,Wshapes))
        child2.setWeights(inflate(c2_Wgenes,Wshapes))

        p1_Bgenes = np.concatenate([a.flatten() for a in parent1.getBiases()])
        p2_Bgenes = np.concatenate([a.flatten() for a in parent2.getBiases()])

        split_point = random.randint(0,len(p1_Bgenes)-1)

        c1_Bgenes = np.asarray(p1_Bgenes[0:split_point].tolist() + p2_Bgenes[split_point:].tolist())
        c2_Bgenes = np.asarray(p1_Bgenes[0:split_point].tolist() + p2_Bgenes[split_point:].tolist())

        Bshapes = [a.shape for a in parent1.getBiases()]
        child1.setBiases(inflate(c1_Bgenes,Bshapes))
        child2.setBiases(inflate(c2_Bgenes,Bshapes))

        children.append(child1)
        children.append(child2)
    for survivor in survivors:
        children.append(survivor)
    return children