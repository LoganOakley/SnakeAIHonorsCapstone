from tkinter import E
import numpy as np
import random
import NeuralNet

#return weights or biases to correct shape after crossover and mutation
def inflate(flat, shapes):
    output = []
    index = 0

    for shape in shapes:
        #number of elements in the current row
        size = np.product(shape)
     
        #take the next "size" elements to make the correct shaped array
        output.append(flat[index: index + size].reshape(shape))
        index += size
    return output

def crossover(survivors, pop_size, mutationRate):
    children = []
    #each iteration creates 2 children show by looping half the number of population size we get the correct number of snakes
    for i in range((pop_size)//2):
        #get 2 random snakes
        parent1 = random.choice(survivors)
        parent2 = random.choice(survivors)
        #initialize 2 random nets
        child1 = NeuralNet.NeuralNet(5, 4, 5, 4)
        child2 = NeuralNet.NeuralNet(5, 4, 5, 4)

        #get the weight shape
        Wshapes = [a.shape for a in parent1.getWeights() ]

        #flatten the parents weights for crossover
        p1_Wgenes = np.concatenate([a.flatten() for a in parent1.getWeights()])
        p2_Wgenes = np.concatenate([a.flatten() for a in parent2.getWeights()])

        #get a random point to cross over
        split_point = random.randint(0,len(p1_Wgenes)-1)

        #first child is the first section of parent 1 and second of parent 2 vice versa for child 2
        c1_Wgenes = np.asarray(p1_Wgenes[0:split_point].tolist() + p2_Wgenes[split_point:].tolist())
        c2_Wgenes = np.asarray(p2_Wgenes[0:split_point].tolist() + p1_Wgenes[split_point:].tolist())

        #set the weights with the inflated gense
        child1.setWeights(inflate(c1_Wgenes,Wshapes))
        child2.setWeights(inflate(c2_Wgenes,Wshapes))

        #repeat above for bias
        p1_Bgenes = np.concatenate([a.flatten() for a in parent1.getBiases()])
        p2_Bgenes = np.concatenate([a.flatten() for a in parent2.getBiases()])

        split_point = random.randint(0,len(p1_Bgenes)-1)

        c1_Bgenes = np.asarray(p1_Bgenes[0:split_point].tolist() + p2_Bgenes[split_point:].tolist())
        c2_Bgenes = np.asarray(p1_Bgenes[0:split_point].tolist() + p2_Bgenes[split_point:].tolist())

        Bshapes = [a.shape for a in parent1.getBiases()]
        child1.setBiases(inflate(c1_Bgenes,Bshapes))
        child2.setBiases(inflate(c2_Bgenes,Bshapes))

        #check for mutaions
        W1mutator = random.uniform(0,1)
        B1mutator = random.uniform(0,1)
        W2mutator = random.uniform(0,1)
        B2mutator = random.uniform(0,1)

        if W1mutator <= mutationRate:
            child1 = mutate(child1)
        if B1mutator <= mutationRate:
            child1 = mutate(child1,True)
        if W2mutator <= mutationRate:
            child2 = mutate(child2)
        if B2mutator <= mutationRate:
            child2 = mutate(child2,True)

        #put the children in the output
        children.append(child1)
        children.append(child2)
        
    return children

def mutate(agent, mutateBias = False):

    #mutate weights
    if not mutateBias:
        #reflatten for mutation
        shape = [a.shape for a in agent.getWeights()]
        genes =  np.concatenate([a.flatten() for a in agent.getWeights()])
        #get random gene
        mutatedGene = random.randint(0, len(genes)-1)
        #set gene to random value
        genes[mutatedGene] = .1* np.random.randn()
        #change the agent's weights
        agent.setWeights(inflate(genes, shape))
    #mutate bias
    else:
        #reflatten for mutation
        shape = [a.shape for a in agent.getBiases()]
        genes =  np.concatenate([a.flatten() for a in agent.getBiases()])
        #get random gene
        mutatedGene = random.randint(0, len(genes)-1)
        #set gene to random value
        genes[mutatedGene] = .1* np.random.randn()
        #change the agent's biases
        agent.setBiases(inflate(genes, shape))
    return agent
    
    