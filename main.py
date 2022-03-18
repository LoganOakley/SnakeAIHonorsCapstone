from pickletools import read_bytes1
from tkinter import NE, W
from venv import create
from matplotlib.pyplot import axis
import pygame
from Snake import Snake
import SnakeGame
import NeuralNet
import numpy as np
import math
import random

fps = 1000
game = SnakeGame.SnakeGame(fps)
pygame.font.init()
over = False
def createPop(previousGen=[], members = 10):
    population = []
    if len(previousGen)==0:
        for i in range(members):
            population.append(NeuralNet.NeuralNet(4,4,3,4))
    else:
        for nn1 in previousGen:
            for nn2 in previousGen:
                nn = NeuralNet.NeuralNet(4,4,3,4)
                weights = genWeights(nn1, nn2)
                biases = genBiases(nn1,nn2)
                nn.setWeights(weights)
                nn.setBiases(biases)
                population.append(nn)
                
    return population

def genWeights(nn1,nn2):
    weights = []
    nn1_weights = nn1.getWeights()
    nn2_weights = nn2.getWeights()
    weights.append(np.average([nn1_weights[0], nn2_weights[0]], axis=0) + .01* np.random.randn(*nn1_weights[0].shape)) 
    weights.append(np.average([nn1_weights[1], nn2_weights[1]], axis=0) + .01* np.random.randn(*nn1_weights[1].shape))
    weights.append(np.average([nn1_weights[2], nn2_weights[2]], axis=0) + .01* np.random.randn(*nn1_weights[2].shape))
    return weights

def genBiases(nn1,nn2):
    biases = []
    nn1_biases = nn1.getBiases()
    nn2_biases = nn2.getBiases()
    biases.append(np.average([nn1_biases[0], nn2_biases[0]], axis=0) + .01* np.random.randn(*nn1_biases[0].shape))
    biases.append(np.average([nn1_biases[1], nn2_biases[1]], axis=0) + .01* np.random.randn(*nn1_biases[1].shape))
    biases.append(np.average([nn1_biases[2], nn2_biases[2]], axis=0) + .01* np.random.randn(*nn1_biases[2].shape))
    return biases

def Simulate(population):
    for nn in population:
        while not game.game_close:
            #Lock the game at a set fps

            game.gameClock.tick(game.gameSpeed)
            input = [abs(game.food[0]-game.snake.headpos[0])+ abs(game.food[1]-game.snake.headpos[1]), game.snake.length, game.snake.headpos[0], game.snake.headpos[1]]
            nn_out = nn.forward(input)
            
            #print(nn_out)
            outputIndex = np.argmax(nn_out)
            
            if outputIndex == 0:
                game.snake.set_vel([0,1])
            elif outputIndex == 1:
                game.snake.set_vel([1,0])
            elif outputIndex == 2:
                game.snake.set_vel([0,-1])
            if outputIndex == 3:
                game.snake.set_vel([-1,0])
            game.checkCollision()
            
            over = game.checkOver()
            if over:
                game.event_handler()
            else:
                game.DrawFrame()
        fitness = over[0] * 10 + over[1]
        nn.setFitness(fitness)
        game.reset()

def getSurvivors(pop, num_survivors):
    pop.sort(reverse = True)
    return pop[0:num_survivors]

def Train(population, num_generations, num_survivors):
    members = len(population)
    for i in range(num_generations):
        print(f"*******************Generation {i}********************")
        Simulate(population)
        survivors = getSurvivors(population,num_survivors)
        for survivor in survivors:
            print(f"Fitness: {survivor.getFitness()}")
        population = createPop(survivors, members)
    f = open("Weight_Storage.txt", "a")
    f.truncate(0)
    for nn in population:
        f.write(str(nn.getWeights()))
    f.close
    f = open("Bias_Storage.txt",'a' )
    f.truncate(0)
    for nn in population:
        f.write(str(nn.getBiases()))
    f.close

    

population = createPop(members = 9)

Train(population, 5, 3) 


 