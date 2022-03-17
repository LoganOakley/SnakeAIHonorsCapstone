from Ray import Ray

class Eyes(object):
    
    def __init__(self, head):
        self.rays =[]
        self.rays.append(Ray(head.centerx, head.centery,1,0))
        self.rays.append(Ray(head.centerx, head.centery, 2**.5/2 ,2**.5/2 ))
        self.rays.append(Ray(head.centerx, head.centery,0,1))
        self.rays.append(Ray(head.centerx, head.centery,-2**.5/2 ,2**.5/2 ))
        self.rays.append(Ray(head.centerx, head.centery,-1,0))
        self.rays.append(Ray(head.centerx, head.centery,-2**.5/2 ,-2**.5/2 ))
        self.rays.append(Ray(head.centerx, head.centery,0,-1))
        self.rays.append(Ray(head.centerx, head.centery,2**.5/2 ,-2**.5/2 ))

   

