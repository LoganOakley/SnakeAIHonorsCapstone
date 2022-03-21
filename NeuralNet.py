from audioop import bias
import sys
import matplotlib
import numpy as np
import nnfs
from nnfs.datasets import spiral_data
from pkg_resources import yield_lines


# nnfs.init()

class Layer_Dense:
    def __init__(self, n_inputs, n_neurons, activation):
        self.weights = 0.10*np.random.randn(n_inputs, n_neurons)
        # print(self.weights)
        self.biases = 0.10*np.random.randn(1, n_neurons)
        self.activation = activation

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases
        self.activation.forward(self.output)

    def setWeights(self, weights, biases):
        self.weights = weights
        self.biases = biases


class Activation_ReLU:
    def __init__(self):
        pass

    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class Activation_Softmax:
    def forward(self, inputs):
        # print(inputs)
        exp_values = np.exp(inputs - np.max(inputs,  axis=1, keepdims=True))
        # print(exp_values)
        probabilities = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        # print(probabilities)
        self.output = probabilities


class Loss:
    def calculate(self, output, y):
        sample_losses = self.forward(output, y)
        data_loss = np.mean(sample_losses)
        return data_loss


class Loss_CategoricalCrossentropy(Loss):
    def forward(self, y_pred, y_true):
        samples = len(y_pred)
        y_pred_clipped = np.clip(y_pred, 1e-7, 1-1e-7)
        if len(y_true.shape) == 1:
            correct_confidences = y_pred_clipped[range(samples), y_true]
        elif len(y_true.shape) == 2:
            correct_confidences = np.sum(y_pred_clipped * y_true, axis=1)
        negative_log_likelyhoods = -np.log(correct_confidences)
        return negative_log_likelyhoods


class NeuralNet:
    def __init__(self, num_inputs, num_outputs, num_layers, nodesPerLayer):
        self.inputLayer = Layer_Dense(
            num_inputs, nodesPerLayer, Activation_ReLU())
        self.outputLayer = Layer_Dense(
            nodesPerLayer, num_outputs, Activation_Softmax())
        self.Layers = []
        self.Layers.append(self.inputLayer)
        for layer in range(num_layers-2):
            self.Layers.append(Layer_Dense(
                nodesPerLayer, nodesPerLayer, Activation_ReLU()))
        self.Layers.append(self.outputLayer)

    def forward(self, inputs):
        self.inputLayer.forward(inputs)
        for i in range(1, len(self.Layers)):
            self.Layers[i].forward(self.Layers[i-1].activation.output)
        self.output = self.outputLayer.activation.output
        return self.output

    def getWeights(self):
        weights = []
        for layer in self.Layers:
            weights.append(layer.weights)
        return weights

    def writeWeights(self):
        weights = self.getWeights()
        np.savetxt("test.txt", weights, delimiter=' ', fmt='%s',
                   newline='\n', header='', footer='', comments='# ', encoding=None)

    def getBiases(self):
        biases = []
        for layer in self.Layers:
            biases.append(layer.biases)
        return biases

    def writeBiases(self):
        biases = self.getBiases()
        np.savetxt("test1.txt", biases, delimiter=' ', fmt='%s', newline='\n', header='', footer='', comments='# ', encoding=None)


    def setBiases(self, biases):
        self.inputLayer.biases = biases[0]
        self.outputLayer.biases = biases[-1]
        for i in range(1, len(self.Layers)-2):
            self.Layers[i].biases = biases[i]

    def setWeights(self, weights):
        self.inputLayer.weights = weights[0]
        self.outputLayer.weights = weights[-1]
        for i in range(1, len(self.Layers)-2):
            self.Layers[i].weights = weights[i]

    def setFitness(self, fitness):
        self.fitness = fitness
    
    def getFitness(self):
        return self.fitness

    def __lt__(self,other):
        if (self.fitness < other.fitness):
            return True
        else:
            return False




