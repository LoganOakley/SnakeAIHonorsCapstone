
import pygame
import time
import random
from Snake import Snake

pygame.init()
 
#constants
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

class SnakeGame():
    def __init__(self, gameSpeed,cap_moves= True, max_moves=50):
        #game setup
        self.dis_width = 500
        self.dis_height = 600
        self.grid_buffer = 100
        self.gameClock = pygame.time.Clock()
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        self.game_over = False
        self.game_close = False
        self.numRows, self.numCols = 10, 10
        self.snake = Snake(self.numRows, self.numCols)
        self.gameSpeed = gameSpeed
        self.score = 0
        self.generate_food()
        self.cap_moves = cap_moves
        self.max_moves = max_moves
        self.disToFood = self.getDistance()
        

    def DrawFrame(self):
        self.dis.fill(black)
        self.grid()
        self.draw_Sprites()
        pygame.display.update()

    
    def generate_food(self):
        row = random.randrange(0, self.numRows)
        col = random.randrange(0, self.numCols)
        while [col,row] in self.snake.tail_list or [row,col]==self.snake.headpos:
            row = random.randrange(0, self.numRows)
            col = random.randrange(0, self.numCols)
        self.food = [col,row]

    def getDistance(self):
        return abs(self.food[0] - self.snake.headpos[0]) + abs(self.food[1] - self.snake.headpos[1])

    def grid(self):
        grid_spacing = self.dis_width // self.numCols
        
        for i in range(self.numRows):
            pygame.draw.line(self.dis, white, [0,grid_spacing*i + self.grid_buffer],[self.dis_width, grid_spacing*i + self.grid_buffer])
        
        for i in range(self.numCols):
            pygame.draw.line(self.dis, white, [grid_spacing*i, self.grid_buffer], [grid_spacing*i, self.dis_height])

        pygame.draw.line(self.dis, white, (grid_spacing*self.numRows-2, self.grid_buffer), (grid_spacing*self.numRows-2, self.dis_height))
        pygame.draw.line(self.dis, white, (0, self.dis_height -2),  (self.dis_width, self.dis_height -2))

    def draw_Sprites(self):
        grid_spaceing = self.dis_width//self.numCols
        pygame.draw.rect(self.dis, red, [self.food[0]*grid_spaceing+1, self.grid_buffer + self.food[1]*grid_spaceing+1, grid_spaceing-1, grid_spaceing-1])
        self.Snake_Movement()
        if self.cap_moves and  self.snake.moves_since_eat >= self.max_moves :
            self.game_over = True
        pygame.draw.rect(self.dis, green,[self.snake.headpos[0]*grid_spaceing+1,self.grid_buffer+self.snake.headpos[1]*grid_spaceing+1, grid_spaceing-1, grid_spaceing-1])
        for block in self.snake.tail_list:
            pygame.draw.rect(self.dis, green,[block[0]*grid_spaceing+1,self.grid_buffer+block[1]*grid_spaceing+1, grid_spaceing-1, grid_spaceing-1])

        
        
    def checkCollision(self):
        self.foodCollision()
        self.wallCollision()
        self.snakeCollision()
    
    def foodCollision(self):
        if self.snake.headpos == self.food:
            
            self.snake.grow()
            self.generate_food()
    
    def wallCollision(self):
        if self.snake.headpos[0] >= self.numCols or self.snake.headpos[0] < 0 or self.snake.headpos[1] >= self.numRows or self.snake.headpos[1] < 0:
            self.game_over = True
            
    
    def snakeCollision(self):
        if self.snake.headpos in self.snake.tail_list:
            self.game_over = True
            

    def checkOver(self):
        if self.game_over:
            return (self.snake.length, self.snake.num_moves)
        else:
            return False

    def Snake_Movement(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.set_vel([-1,0])
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_vel([1,0])
                elif event.key == pygame.K_UP:
                    self.snake.set_vel([0,-1])
                elif event.key == pygame.K_DOWN:
                    self.snake.set_vel([0,1])
                elif event.key == pygame.K_q:
                    self.event_handler()

        self.snake.move()
        self.disToFood = self.getDistance()
        #print(f"Distance: {self.disToFood}")

    def event_handler(self):
        self.game_close = True
        #pygame.quit()

    def reset(self):
        self.__init__(self.gameSpeed)
        

            
'''
fps = 8
game = SnakeGame(fps)
pygame.font.init()
over = False
while not game.game_close:
    #Lock the game at a set fps
    game.gameClock.tick(game.gameSpeed)
    game.checkCollision()
    game.DrawFrame()
    over = game.checkOver()
    if over:
        game.event_handler()
fitness = over[0] * 100 + over[1]

print(f"Fitness: {fitness}")
'''

