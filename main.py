
from inspect import CORO_SUSPENDED
import pygame
from GenenticFunctions import crossover, mutate
import SnakeGame
import NeuralNet
from KerasNetwork import create_model, predict_action
import numpy as np
import random
fps = 60
game = SnakeGame.SnakeGame(fps, max_moves=20)
pygame.init()
over = False

load_progress = True

#initialize population
def createPop( members=10):
    population = []
    
    #if not previous generation provided, create random population
    
    for i in range(members):
        population.append(create_model())
    if load_progress:
        for i in range(members):
            population[i].load_weights("SavedModels/model_new"+str(i)+".keras")
    


    #if previous generations survivors are given, perform crossover to get new population
       
    return population


#return the spaces imediately around the snake's head.
def getEnvironment():
    start_pos = game.snake.headpos
    vel_left = [game.snake.velocity[1], -game.snake.velocity[0]]
    vel_right = [-game.snake.velocity[1], game.snake.velocity[0]]
    vel_straight = game.snake.velocity
    straight = start_pos + vel_straight
    left     = start_pos + vel_left
    right    = start_pos + vel_right
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

    #Need to add looking for food to the left right or striaght
    food_ahead = check_for_food(start_pos, vel_straight, food_pos)
    food_left = check_for_food(start_pos, vel_left, food_pos)
    food_right = check_for_food(start_pos,vel_right , food_pos)
    
    outputs.append(food_ahead)
    outputs.append(food_left)
    outputs.append(food_right)

    return outputs

def check_for_food(curr_space, direction,food):
    if direction[0] == 0:
        if curr_space[0] == food[0]:
            if direction[1] > 0:
                if curr_space[1] < food[1]:
                    return 1 
                else:
                    return 0
            else:
                if curr_space[1] > food[1]:
                    return 1
                else:
                    return 0
        else:
            return 0
    else:
        if curr_space[1] == food[1]:
            if direction[0] > 0:
                if curr_space[0] < food[0]:
                    return 1 
                else:
                    return 0
            else:
                if curr_space[0] > food[0]:
                    return 1
                else:
                    return 0
        else:
            return 0


def Simulate(population):
    fitnesses=[0 for i in range(len(population))]
    for i in range(len(population)):
        while not game.game_close:
            # Lock the game at a set fps

            game.gameClock.tick(game.gameSpeed)

            #get value of spaces the snake could move to
            environment = getEnvironment()
            
            #get output for current Neural net
            nn_out = predict_action(environment,population,i)

            # print(nn_out)
            #get maxium output value to pick which direction snake will take
            outputIndex = nn_out
            if outputIndex == 0:
                if(game.snake.velocity == [0,0]):
                    game.snake.velocity = [0,-1]
                else:
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
        fitness = over[0] * 100 + over[1] +over[2]*2
        if over[3]:
            fitness -= 30
        fitnesses[i]=fitness
        game.reset()
    return fitnesses


def save_pool(population):
    for xi in range(len(population)):
        population[xi].save_weights("SavedModels/model_new" + str(xi) + ".keras")
    print("Saved current pool!")


def Train(population, num_generations, num_survivors):
    #number of snakes in the population
    members = len(population)

    #for each generation
    for i in range(num_generations):
        print(f"*******************Generation {i}********************")
        #run the game for each snake 
        new_weights = []
        fitnesses = Simulate(population)
        survivors, survivor_fitnesses = getSurvivors(population, fitnesses)
        print("Selected fitnesses:\n")
        for fitness in survivor_fitnesses:
            print(f'Fitness: {fitness}\n')
        parents = random.choices(survivors,weights = survivor_fitnesses, k=pop_size)
        for i in range(pop_size // 2):
            
            crossed_weights = crossover( parents[i], parents[i+1])
            mutated1 = mutate(crossed_weights[0])
            mutated2 = mutate(crossed_weights[1])

            new_weights.append(mutated1)
            new_weights.append(mutated2)


        
        for i in range(len(new_weights)):
            population[i].set_weights(new_weights[i])
        population[0].set_weights(survivors[0].get_weights())
        save_pool(population)


def getSurvivors(pop, fit):
    
    #zip together
    mappedFitness = list(zip(pop,fit))
    #sort by fitness to get the best models
    mappedFitness.sort(key= lambda x:x[1], reverse=True )
    #return the best models as a list to be put through crossover
    numSurvivors = round(len(pop)*.15) 
    mappedSurvivors = mappedFitness[0:numSurvivors]
    survivors = [mappedSurvivors[i][0] for i in range(len(mappedSurvivors))]
    survivor_fits = [mappedSurvivors[i][1] for i in range(len(mappedSurvivors))]
    return survivors, survivor_fits


#get inital population
pop_size = 50

population = createPop(members=pop_size)

#Train the population
Train(population, 2000, 5)
