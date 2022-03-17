import sys
import matplotlib
import numpy as np
import nnfs
from nnfs.datasets import spiral_data
from pkg_resources import yield_lines


#nnfs.init()

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons, activation):
        self.weights = 0.10*np.random.randn(n_inputs, n_neurons)
        #print(self.weights)
        self.biases = 0.10*np.random.randn(1, n_neurons)
        self.activation = activation

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
    
    def setWeights(self, weights, biases):
        self.weights = weights
        self.biases = biases

class Activation_ReLU:
    def __init__(self):
        pass
    
    def forward(self,inputs):
        self.output = np.maximum(0,inputs)

class Activation_Softmax:
    def forward(self,inputs):
        #print(inputs)
        exp_values = np.exp(inputs- np.max(inputs,  axis=1, keepdims=True))
        #print(exp_values)
        probabilities = exp_values / np.sum(exp_values,axis=1, keepdims=True)
        #print(probabilities)
        self.output = probabilities
    
class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output,y)
        data_loss = np.mean(sample_losses)
        return data_loss
    
class Loss_CategoricalCrossentropy(Loss):
    def forward(self,y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)
        if len(y_true.shape)==1:
            correct_confidences = y_pred_clipped[range(samples), y_true]
        elif len(y_true.shape) ==2:
            correct_confidences = np.sum(y_pred_clipped * y_true, axis = 1)
        negative_log_likelyhoods = -np.log(correct_confidences)
        return negative_log_likelyhoods


class NeuralNet:
    def __init__(self, num_inputs, num_outputs, num_layers, nodesPerLayer):
        self.inputLayer = Layer_Dense(num_inputs, nodesPerLayer, Activation_ReLU())
        self.outputLayer = Layer_Dense(nodesPerLayer, num_outputs, Activation_Softmax())
        self.hiddenLayers = []
        for layer in range(num_layers-2):
            self.hiddenLayers.append(Layer_Dense(nodesPerLayer,nodesPerLayer, Activation_ReLU()))
        
    def forward(self, inputs):
        self.inputLayer.forward(inputs)
        #print(self.inputLayer.output)
        self.inputLayer.activation.forward(self.inputLayer.output)
        #print(self.inputLayer.activation.output)
        for layer in range(len(self.hiddenLayers)):
            if layer == 0:
                self.hiddenLayers[0].forward(self.inputLayer.activation.output)
                #print(self.hiddenLayers[0].output)
                self.hiddenLayers[0].activation.forward(self.hiddenLayers[0].output)
                #print (self.hiddenLayers[0].activation.output)
            else:
                self.hiddenLayers[layer].forward(self.hiddenLayers[layer-1].activation.output)
                #print(self.hiddenLayers[layer-1].activation.output)
                self.hiddenLayers[layer].activation.forward(self.hiddenLayers[layer].output)
        self.outputLayer.forward(self.hiddenLayers[-1].activation.output)
        #print(self.outputLayer.output)
        self.outputLayer.activation.forward(self.outputLayer.output)
        #print(self.output)
        self.output = self.outputLayer.activation.output
        return self.output

    def getWeights(self):
        inputWeights = self.inputLayer.weights
        hiddenWeights = []
        for layer in self.hiddenLayers:
            hiddenWeights.append(layer.weights)
        
        outputWeights = self.outputLayer.weights
        weights = [inputWeights, np.array(hiddenWeights), outputWeights]
        return weights

    def getBiases(self):
        inputBiases = self.inputLayer.biases
        hiddenBiases = []
        for layer in self.hiddenLayers:
            hiddenBiases.append(layer.biases)
        
        outputBiases = self.outputLayer.biases
        biases = [inputBiases, np.array(hiddenBiases), outputBiases]
        return biases

    def setBiases(self, biases):
        self.inputLayer.biases = biases[0]
        self.outputLayer.biases = biases[2]
        for i in range(len(self.hiddenLayers)):
            self.hiddenLayers[i].biases = biases[1][i]

    def setWeights(self, weights):
        self.inputLayer.weights = weights[0]
        self.outputLayer.weights = weights[2]
        for i in range(len(self.hiddenLayers)):
            self.hiddenLayers[i].weights = weights[1][i]

    def setFitness(self, fitness):
        self.fitness = fitness
    
    def getFitness(self):
        return self.fitness

    def __lt__(self,other):
        if (self.fitness < other.fitness):
            return True
        else:
            return False


'''
X, y = spiral_data(samples = 100, classes = 3)
dense1 = Layer_Dense(2,3)
activation1 = Activation_ReLU()

dense2= Layer_Dense(3, 3)
activation2 = Activation_Softmax()

dense1.forward(X)
activation1.forward(dense1.output)

dense2.forward(activation1.output)
activation2.forward(dense2.output)

print(activation2.output[:5])

loss_function = Loss_CategoricalCrossentropy()
loss = loss_function.calculate(activation2.output, y)
print(loss)
'''

