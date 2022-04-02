
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
        self.snake = Snake( self.numCols,self.numRows)
        self.gameSpeed = gameSpeed
        self.score = 0
        self.generate_food()
        self.cap_moves = cap_moves
        self.max_moves = max_moves
        self.disToFood = self.getDistance()
        self.starved = False
        

    def DrawFrame(self):
        #clear screen
        self.dis.fill(black)
        #draw grid
        self.grid()
        #draw food and snake
        self.draw_Sprites()
        #update display
        pygame.display.update()

    
    def generate_food(self):
        #put food in random location
        row = random.randrange(0, self.numRows)
        col = random.randrange(0, self.numCols)
        #check that food not inside of snake
        while [col,row] in self.snake.tail_list or [row,col]==self.snake.headpos:
            #if it is move the food
            row = random.randrange(0, self.numRows)
            col = random.randrange(0, self.numCols)
        #set food location
        self.food = [col,row]

    def getDistance(self):
        #return manhatten distance to food
        return abs(self.food[0] - self.snake.headpos[0]) + abs(self.food[1] - self.snake.headpos[1])

    def grid(self):
        #space grid evenly
        grid_spacing = self.dis_width // self.numCols
        #draw rows and coloumns
        for i in range(self.numRows):
            pygame.draw.line(self.dis, white, [0,grid_spacing*i + self.grid_buffer],[self.dis_width, grid_spacing*i + self.grid_buffer])
        
        for i in range(self.numCols):
            pygame.draw.line(self.dis, white, [grid_spacing*i, self.grid_buffer], [grid_spacing*i, self.dis_height])
        #add lines at bottom and right of screen to be visible
        pygame.draw.line(self.dis, white, (grid_spacing*self.numRows-2, self.grid_buffer), (grid_spacing*self.numRows-2, self.dis_height))
        pygame.draw.line(self.dis, white, (0, self.dis_height -2),  (self.dis_width, self.dis_height -2))

    def draw_Sprites(self):
        #set spacing
        grid_spaceing = self.dis_width//self.numCols
        #draw food
        pygame.draw.rect(self.dis, red, [self.food[0]*grid_spaceing+1, self.grid_buffer + self.food[1]*grid_spaceing+1, grid_spaceing-1, grid_spaceing-1])
        #move snake
        self.Snake_Movement()
        #check if we are limiting the moves and if so if the snake has moved too mcuh
        if self.cap_moves and  self.snake.moves_since_eat >= self.max_moves :
            #if so snake dies
            self.starved = True
            self.game_over = True
        #draw snake head
        pygame.draw.rect(self.dis, green,[self.snake.headpos[0]*grid_spaceing+1,self.grid_buffer+self.snake.headpos[1]*grid_spaceing+1, grid_spaceing-1, grid_spaceing-1])
        #draw tail segments
        for block in self.snake.tail_list:
            pygame.draw.rect(self.dis, green,[block[0]*grid_spaceing+1,self.grid_buffer+block[1]*grid_spaceing+1, grid_spaceing-1, grid_spaceing-1])

        
        
    def checkCollision(self):
        self.foodCollision()
        self.wallCollision()
        self.snakeCollision()
    
    def foodCollision(self):
        #if head on food grow the snake and make new food
        if self.snake.headpos == self.food:
            
            self.snake.grow()
            self.generate_food()
    
    def wallCollision(self):
        #if snake is past walls snake dies
        if self.snake.headpos[0] >= self.numCols or self.snake.headpos[0] < 0 or self.snake.headpos[1] >= self.numRows or self.snake.headpos[1] < 0:
            self.game_over = True
            
    
    def snakeCollision(self):
        #If snake's head is in the tail snake dies
        if self.snake.headpos in self.snake.tail_list:
            self.game_over = True
            

    def checkOver(self):
        #check that the game is over if so we return the values needed for fitness function
        if self.game_over:
            return (self.snake.length, self.snake.movesTowardsFood,len(self.snake.squares_visited) ,self.starved)
        else:
            return False

    def Snake_Movement(self):
        #movement for human input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.snake.turn_left()
                elif event.key == pygame.K_RIGHT:
                    self.snake.turn_right()
                elif event.key == pygame.K_UP:
                    self.snake.set_vel([0,-1])
                elif event.key == pygame.K_DOWN:
                    self.snake.set_vel([0,1])
                elif event.key == pygame.K_q:
                    self.event_handler()
        #move the snake and update distance to food
        self.snake.move()
        self.previousDistToFood = self.disToFood
        self.disToFood = self.getDistance()
        if self.previousDistToFood > self.disToFood:
            self.snake.movesTowardsFood += 1
        #print(f"Distance: {self.disToFood}")

    #close the game and perform any other required functions
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

