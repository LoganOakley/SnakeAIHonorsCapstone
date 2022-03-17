import pygame
import SnakeGame



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