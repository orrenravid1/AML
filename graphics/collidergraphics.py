import pygame
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.physics.colliders import*

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
BLUE = (0, 0, 255)
RED      = ( 255,   0,   0)
YELLOW = (255,255,0)
PURPLE =  (204, 0, 255)
SAND = (244, 164, 96)
ORANGE = (255,165,0)
GRAY = (139,139,139)
BROWN = (165,99,13)

class CircleColliderG(CircleCollider):
    def __init__(self,pos,radius):
        super().__init__(pos,radius)
    def draw(self,screen):
        pygame.draw.circle(screen,ORANGE,(int(self.pos.get_x()),
                                          int(self.pos.get_y())),
                           self.radius,3)

class SurfaceColliderG(SurfaceCollider):
    def __init__(self,p1,p2):
        super().__init__(p1,p2)
    def draw(self,screen):
        pygame.draw.line(screen,GREEN,(int(self.p1.get_x()),
                                       int(self.p1.get_y())),
                         (int(self.p2.get_x()),int(self.p2.get_y())),3)
