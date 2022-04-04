from os import environ
import pygame
import SnakeGame
import GenenticFunctions
import NeuralNet



#allows human to play game for testing and demonstrations

fps = 1
game = SnakeGame.SnakeGame(fps, False)
pygame.font.init()
over = False

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
    
#return the spaces imediately around the snake's head.
def getEnvironment():
    start_pos = game.snake.headpos
    vel_left = [game.snake.velocity[1], -game.snake.velocity[0]]
    vel_right = [-game.snake.velocity[1], game.snake.velocity[0]]
    vel_straight = game.snake.velocity
    straight = [start_pos[i] + vel_straight[i] for i in range(len(start_pos))]
    left     = [start_pos[i] + vel_left[i] for i in range(len(start_pos))]
    right    = [start_pos[i] + vel_right[i] for i in range(len(start_pos))]
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

while not game.game_close:
    #Lock the game at a set fps

    environment = getEnvironment()
    print(environment)
    game.gameClock.tick(game.gameSpeed)
    
    
    game.checkCollision()
    
    over = game.checkOver()
    if over:
        game.event_handler()
    else:
        game.DrawFrame()
    
