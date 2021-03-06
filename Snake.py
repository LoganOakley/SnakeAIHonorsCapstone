import pygame




class Snake:

    movesTowardsFood = 0
    #moves since last food to test for game ending due to infinite loop
    moves_since_eat = 0
    def __init__(self,rows, cols):
        #start head at center
        self.headpos = [cols/2, rows/2]
        self.length = 0
        self.tail_list = []
        self.velocity = [0,-1]
        self.squares_visited = []

    #change position based onvelocity
    def move(self):
        #if snake just started give base movement
        #insert into the first location in taillist the current head
        if (self.headpos not in self.squares_visited):
            self.squares_visited.append(self.headpos)
        self.tail_list.insert(0,self.headpos)
        #remove all of the blocks past the length of the snake
        self.tail_list = self.tail_list[0:self.length]
        #update head pos
        self.headpos = [self.headpos[0] + self.velocity[0], self.headpos[1] + self.velocity[1]]
        #increment move counters

        self.moves_since_eat +=1

    def set_vel(self,vel):
        #set velocity
        self.velocity = vel
    
    def grow(self):
        #increase lenght and reset move since eat counter
        self.length += 1
        self.moves_since_eat=0

    def turn_left(self):
        if(self.velocity)==[0,0]:
            self.velocity = [0,-1]
        temp_x = self.velocity[0]
        temp_y = self.velocity[1]
        self.velocity[0] = temp_y
        self.velocity[1] = -temp_x
    
    
    def turn_right(self):
        if(self.velocity)==[0,0]:
            self.velocity = [0,-1]
        temp_x = self.velocity[0]
        temp_y = self.velocity[1]
        self.velocity[0] =  -temp_y
        self.velocity[1] =  temp_x
        
        