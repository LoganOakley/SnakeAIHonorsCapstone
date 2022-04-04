import pygame
import SnakeGame
import GenenticFunctions
import NeuralNet
from KerasNetwork import create_model, predict_action


#allows human to play game for testing and demonstrations
best = create_model()
best.load_weights("SavedModels/HighScore_3439.keras")
fps = 8
game = SnakeGame.SnakeGame(fps, False)
pygame.font.init()
over = False


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

while not game.game_close:
            # Lock the game at a set fps
            environment = getEnvironment()
            game.gameClock.tick(game.gameSpeed)

            #get value of spaces the snake could move to
           
            
            #get output for current Neural net
            nn_out = predict_action(environment,[best],0)

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
                game.snake.turn_right()


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
