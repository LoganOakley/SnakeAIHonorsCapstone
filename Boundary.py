import pygame

class Boundary:

    def __init__(self, x1, y1, x2, y2):
        self.a = [ x1, y1 ]
        self.b = [ x2, y2 ]

    def show(self, dis, color):
        pygame.draw.line(dis, color, [self.a[0], self.a[1]], [self.b[0], self.b[1]],1)





