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
MutationRate = 0

#initialize population
def createPop(previousGen=[], members=10, mutationRate=0):
    population = []
    #if not previous generation provided, create random population
    if len(previousGen) == 0:
        for i in range(members):
            population.append(NeuralNet.NeuralNet(3, 3, 8, 8))

    #if previous generations survivors are given, perform crossover to get new population
    else:
        
        population = crossover(previousGen, members, mutationRate)
       
    return population


#return the spaces imediately around the snake's head.
def getEnvironment():
    start_pos = game.snake.headpos
    straight = start_pos + game.snake.velocity
    left     = start_pos + [game.snake.velocity[1], -game.snake.velocity[0]]
    right    = start_pos + [-game.snake.velocity[1], game.snake.velocity[0]]
    directions = [straight, left, right]
    outputs = [0, 0, 0]
    for i in range(len(directions)):
        if directions[i] in game.snake.tail_list or directions[i][0] >= game.numCols or directions[i][1] >= game.numRows or directions[i][0] < 0 or directions[i][1] < 0:
            #spaces that would kill the snake go in group 1
            outputs[i] = 1
        else:
            #non-lethal positions get 0
            outputs[i] = 0
    food_pos = game.food

    #use 3 inputs for location of food left or right or straight
    

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
            input = environment
            #get output for current Neural net
            nn_out = nn.forward(input)

            # print(nn_out)
            #get maxium output value to pick which direction snake will take
            outputIndex = nn_out
            if outputIndex == 0:
                pass
            elif outputIndex == 1:
                game.snake.turn_left()
            elif outputIndex == 2:
                game.snake.turn_right


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
        fitness = over[0] * 15 + over[1]
        if over[2]:
            fitness -= 50
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

            #print(survivor.getWeights())
            #print('\n')
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
population = createPop(members=50, mutationRate=MutationRate)

#Train the population
Train(population, 2000, 5)
