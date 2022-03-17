import pygame




class Snake:

    num_moves = 0
    
    def __init__(self,rows, cols):
        self.headpos = [cols/2, rows/2]
        self.length = 0
        self.tail_list = []
        self.velocity = [0,0]

    def move(self):
        if self.velocity==[0,0]:
            self.velocity =[-1,0]
        self.tail_list.insert(0,self.headpos)
        self.tail_list = self.tail_list[0:self.length]
        self.headpos = [self.headpos[0] + self.velocity[0], self.headpos[1] + self.velocity[1]]
        self.num_moves+=1

    def set_vel(self,vel):
        self.velocity = vel
    
    def grow(self):
        self.length += 1
        
        