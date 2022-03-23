import pygame
import SnakeGame
import GenenticFunctions
import NeuralNet


#small test
test1 = NeuralNet.NeuralNet(5,4,5,4)
test2 = NeuralNet.NeuralNet(5,4,5,4)
print("Test1: \n")
print(test1.getWeights())

print("\nTest2: \n")
print(test2.getWeights())
population = [test1,test2]

for i in range(4):   
    print(f"\nGen {i}\n")
    population = GenenticFunctions.crossover(population,2,0)
    for agent in population:
        print(f"\nAgent: \n")
        print(agent.getWeights())

#the layer that contains the split point for crossover is getting set to seemingly random values rather than splitting properly



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