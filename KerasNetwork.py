import tensorflow as tf
from tensorflow import keras
from keras import layers

class SnakeNetwork():
    def __init__(self):
        
        self.model = keras.Sequential(name = "Snake Agent")
        self.model.add(layers.Dense(5,activation='relu', name = "Input_Layer", input_shape=(6,)))
        self.model.add(layers.Dense(5, activation='relu', name = "Hidden_1"))
        self.model.add(layers.Dense(5, activation='relu', name = "Hidden_2"))
        self.model.add(layers.Dense(3, activation='softmax', name = "Output_Layer"))
    
    def forward(self, inputs):
        return self.model(inputs)
    

