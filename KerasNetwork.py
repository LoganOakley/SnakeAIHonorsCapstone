from platform import architecture
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np
def create_model():
        
    model = Sequential()
    model.add(Dense(6, input_shape=(6,)))
    model.add(Activation('relu'))
    model.add(Dense(8, input_shape=(6,)))
    model.add(Activation('relu'))
    model.add(Dense(8,input_shape=(8,)))
    model.add(Activation('relu'))
    model.add(Dense(3, input_shape=(8,)))
    model.add(Activation('sigmoid'))
    model.compile(loss='mse', optimizer='adam') 
    return model 

def predict_action(inputs, population, model_num):
    neural_input = np.asarray(inputs)
    neural_input = np.atleast_2d(neural_input)

    outputs = population[model_num].predict(neural_input,1)[0]

    return np.argmax(outputs)


