import pygame
import SnakeGame
import GenenticFunctions
import NeuralNet

test1 = NeuralNet.NeuralNet(5,4,5,4)
test2 = NeuralNet.NeuralNet(5,4,5,4)

population = [test1,test2]

population = GenenticFunctions.crossover(population,2,0)

print("Test1: \n")
print(test1.getWeights())

print("\nTest2: \n")
print(test2.getWeights())

for agent in population:
    print("\nAgents: \n")
    print(agent.getWeights())


#allows human to play game for testing and demonstrations
'''
fps = 8
game = SnakeGame.SnakeGame(fps, False)
pygame.font.init()
over = False
while not game.game_close:
    #Lock the game at a set fps
    game.gameClock.tick(game.gameSpeed)
    game.checkCollision()
    
    over = game.checkOver()
    if over:
        game.event_handler()
    else:
        game.DrawFrame()
        '''