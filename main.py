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
MutationRate = .08

#initialize population
def createPop(previousGen=[], members=10, mutationRate=1):
    population = []
    #if not previous generation provided, create random population
    if len(previousGen) == 0:
        for i in range(members):
            population.append(NeuralNet.NeuralNet(5, 4, 5, 4))

    #if previous generations survivors are given, perform crossover to get new population
    else:
        
        population = crossover(previousGen, members, mutationRate)
       
    return population


#return the spaces imediately around the snake's head.
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
            #food is puts space in group 3
            outputs[i] = 3
        elif directions[i] in game.snake.tail_list or directions[i][0] >= game.numCols or directions[i][1] >= game.numRows or directions[i][0] < 0 or directions[i][1] < 0:
            #spaces that would kill the snake go in group 1
            outputs[i] = 1
        else:
            #empty spaces in group 2
            outputs[i] = 2
    return outputs


def Simulate(population):
    for nn in population:
        while not game.game_close:
            # Lock the game at a set fps

            game.gameClock.tick(game.gameSpeed)
            #manhatten distence to food for input
            dis_to_food = game.getDistance()
            #get value of spaces the snake could move to
            environment = getEnvironment()
            #create input list
            input = [dis_to_food, environment[0],
                     environment[1], environment[2], environment[3]]
            #get output for current Neural net
            nn_out = nn.forward(input)

            # print(nn_out)
            #get maxium output value to pick which direction snake will take
            outputIndex = np.argmax(nn_out)

            if outputIndex == 0:
                game.snake.set_vel([0, 1])
            elif outputIndex == 1:
                game.snake.set_vel([1, 0])
            elif outputIndex == 2:
                game.snake.set_vel([0, -1])
            if outputIndex == 3:
                game.snake.set_vel([-1, 0])

            #check if snake hit self, wall or food
            game.checkCollision()

            #over contains the values that go into the fitness function when the game ends
            over = game.checkOver()
            if over:
                #if game is over we run the event handler to clean up for next Neural Net
                game.event_handler()
            else:
                #otherwise we draw the next frame
                game.DrawFrame()
        #fitness function is currently 10*snake_length + total_moves_made
        fitness = over[0] * 10 + over[1]
        nn.setFitness(fitness)
        game.reset()


def getSurvivors(pop, num_survivors):
    #sort population by fitness values
    pop.sort(reverse=True)
    #return the best nets from the population up to the num_survivors
    return pop[0:num_survivors]


def Train(population, num_generations, num_survivors):
    #number of snakes in the population
    members = len(population)

    #for each generation
    for i in range(num_generations):
        print(f"*******************Generation {i}********************")
        #run the game for each snake 
        Simulate(population)
        #get the best snakes
        survivors = getSurvivors(population, num_survivors)
        #create a new population of snakes using the survivors of the previous generation
        population = createPop(survivors,members, MutationRate)
        #print each survivor's fitness to monitor the progression through generations
        for survivor in survivors:
            
            print(f"Fitness: {survivor.getFitness()}")
            

    #write last generations weights and biases to reinitiate for furthur training later and for demonstrations
    with open("Weight_Storage.txt", "a") as f:
        f.truncate(0)
        for nn in population:
            f.write(str(nn.getWeights()))
    with open("Bias_Storage.txt", "a") as f:
        f.truncate(0)
        for nn in population:
            f.write(str(nn.getBiases()))

#get inital population
population = createPop(members=500, mutationRate=MutationRate)

#Train the population
Train(population, 2000, 10)
