from pickletools import read_bytes1
from tkinter import NE, W
from venv import create
from matplotlib.pyplot import axis
import pygame
from GenenticFunctions import crossover
from Snake import Snake
import SnakeGame
import NeuralNet
import numpy as np
import math
import random

fps = 5000
game = SnakeGame.SnakeGame(fps, max_moves=20)
pygame.font.init()
over = False


def createPop(previousGen=[], members=10, mutationRate=1):
    population = []
    if len(previousGen) == 0:
        for i in range(members):
            population.append(NeuralNet.NeuralNet(5, 4, 5, 4))
    else:
        population = crossover(previousGen, members)
    return population



def getEnvironment():
    start_pos = game.snake.headpos
    north = [start_pos[0], start_pos[1]-1]
    south = [start_pos[0], start_pos[1]+1]
    east = [start_pos[0]+1, start_pos[1]]
    west = [start_pos[0]-1, start_pos[1]]
    directions = [north, south, east, west]
    outputs = [0, 0, 0, 0]
    for i in range(len(directions)):
        if directions[i] == game.food:
            outputs[i] = 3
        elif directions[i] in game.snake.tail_list or directions[i][0] >= game.numCols or directions[i][1] >= game.numRows or directions[i][0] < 0 or directions[i][1] < 0:
            outputs[i] = 1
        else:
            outputs[i] = 2
    return outputs


def Simulate(population):
    for nn in population:
        while not game.game_close:
            # Lock the game at a set fps

            game.gameClock.tick(game.gameSpeed)
            dis_to_food = abs(
                game.food[0]-game.snake.headpos[0]) + abs(game.food[1]-game.snake.headpos[1])
            environment = getEnvironment()
            input = [dis_to_food, environment[0],
                     environment[1], environment[2], environment[3]]
            nn_out = nn.forward(input)

            # print(nn_out)
            outputIndex = np.argmax(nn_out)

            if outputIndex == 0:
                game.snake.set_vel([0, 1])
            elif outputIndex == 1:
                game.snake.set_vel([1, 0])
            elif outputIndex == 2:
                game.snake.set_vel([0, -1])
            if outputIndex == 3:
                game.snake.set_vel([-1, 0])
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
    pop.sort(reverse=True)
    return pop[0:num_survivors]


def Train(population, num_generations, num_survivors):
    members = len(population)
    for i in range(num_generations):
        print(f"*******************Generation {i}********************")
        Simulate(population)
        survivors = getSurvivors(population, num_survivors)
        for survivor in survivors:
            print(f"Fitness: {survivor.getFitness()}")
            

    
    with open("Weight_Storage.txt", "a") as f:
        f.truncate(0)
        for nn in population:
            f.write(str(nn.getWeights()))
    with open("Bias_Storage.txt", "a") as f:
        f.truncate(0)
        for nn in population:
            f.write(str(nn.getBiases()))


population = createPop(members=500, mutationRate=.08)

Train(population, 2000, 10)
