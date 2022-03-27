#code adapted from Neural Networks From Scratch https://nnfs.io/
import numpy as np
import math

#Layer class
class Layer_Dense:
    def __init__(self, n_inputs, n_neurons, activation):
        #random weights and biases
        self.weights = 0.10*np.random.randn(n_inputs, n_neurons)
        self.biases = 0.10*np.random.randn(1, n_neurons)
        self.activation = activation

    def forward(self, inputs):
        #run the dot product and activation for the layer
        self.output = np.dot(inputs, self.weights) + self.biases
        self.activation.forward(self.output)



#rectified linear activation
class Activation_ReLU:
    def __init__(self):
        pass

    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class Activation_Sigmoid:
    def sigmoid(self, x):
        return 1/(1 + math.e**-x)
    def forward(self, inputs):
        sigmoidVectorized = np.vectorize(self.sigmoid)
        self.output = sigmoidVectorized(inputs)

class Activation_Softmax:
    def forward(self, inputs):
        # print(inputs)
        exp_values = np.exp(inputs - np.max(inputs,  axis=1, keepdims=True))
        # print(exp_values)
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        # print(probabilities)
        self.output = probabilities



class NeuralNet:

    #snake NN
    def __init__(self, num_inputs, num_outputs, num_layers, nodesPerLayer):
        #create input layer with sigmoid activation
        self.inputLayer = Layer_Dense(
            num_inputs, nodesPerLayer, Activation_Sigmoid())
        #create output layer with softmax activation
        self.outputLayer = Layer_Dense(
            nodesPerLayer, num_outputs, Activation_Softmax())
        self.Layers = []
        #put in input layer
        self.Layers.append(self.inputLayer)
        #create and append each hidden layer with a sigmoid activation
        for layer in range(num_layers-2):
            self.Layers.append(Layer_Dense(
                nodesPerLayer, nodesPerLayer, Activation_Sigmoid()))
        #append output layer
        self.Layers.append(self.outputLayer)

    def forward(self, inputs):
        #do forward for each layer 
        self.inputLayer.forward(inputs)
        for i in range(1, len(self.Layers)):
            self.Layers[i].forward(self.Layers[i-1].activation.output)
        self.output = self.outputLayer.activation.output
        return self.output

    def getWeights(self):
        #return weights for each layer
        weights = []
        for layer in self.Layers:
            weights.append(layer.weights)
        return weights


    #testing another way to write weights
    def writeWeights(self):
        weights = self.getWeights()
        np.savetxt("test.txt", weights, delimiter=' ', fmt='%s',
                   newline='\n', header='', footer='', comments='# ', encoding=None)

    
    def getBiases(self):
        #return biases for each layer
        biases = []
        for layer in self.Layers:
            biases.append(layer.biases)
        return biases

    #testing another way to write biases
    def writeBiases(self):
        biases = self.getBiases()
        np.savetxt("test1.txt", biases, delimiter=' ', fmt='%s', newline='\n', header='', footer='', comments='# ', encoding=None)


    def setBiases(self, biases):
        #set input layer with first biases array
        self.inputLayer.biases = biases[0]
        #set output layer with last bias array
        self.outputLayer.biases = biases[-1]
        #for each other layer give it the bias in the corrosponding location
        for i in range(1, len(self.Layers)-2):
            self.Layers[i].biases = biases[i]

    def setWeights(self, weights):
        #for each other layer give it the weight in the corrosponding location
        for i in range(0, len(self.Layers)-1):
            self.Layers[i].weights = weights[i]
        self.inputLayer = self.Layers[0]
        self.outputLayer = self.Layers[-1]

    def setFitness(self, fitness):
        #set fitness for the NN
        self.fitness = fitness
    
    def getFitness(self):
        return self.fitness

    #allows comparision and sorting by fitness
    def __lt__(self,other):
        if (self.fitness < other.fitness):
            return True
        else:
            return False




