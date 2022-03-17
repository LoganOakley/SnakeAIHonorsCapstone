import pygame

class Ray:
    def __init__(self, x, y, dirx, diry):
        self.pos=[x,y]
        self.dir=[dirx,diry]

#draws rays to display
    def show(self,dis, color):
        pygame.draw.line(dis, color,[self.pos[0], self.pos[1]],
                                    [self.pos[0] + self.dir[0]*10, self.pos[1] + self.dir[1]*10])
   #calculates where the ray collides with an object
    def cast(self, wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]

        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        den = (x1 - x2) * (y3 - y4)-(y1 - y2) * (x3 - x4)
        if den == 0:
            return
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4))/den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3))/den

        if (t > 0 and t < 1 and u > 0):
            ptx = x1 + t(x2 - x1) 
            pty = y1 + t(y2 - y1)
            return [ptx, pty]

        else:
            return False