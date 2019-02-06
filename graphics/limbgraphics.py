import pygame
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.mathlib.math2d import *
from AML.physics.limb import *

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

class LimbG(Limb):
    def __init__(self,n0,n1,numcols,**kwargs):
        super().__init__(n0,n1,numcols,**kwargs)
    def draw(self,screen):
        n0 = self.nodes[0]
        n1 = self.nodes[1]
        n0x = int(n0.get_x())
        n0y = int(n0.get_y())
        n1x = int(n1.get_x())
        n1y = int(n1.get_y())
        pygame.draw.line(screen,BLACK,(n0x,n0y),
                     (n1x,n1y),3)
        pygame.draw.circle(screen,RED,(n0x,n0y),4)
        pygame.draw.circle(screen,BLUE,(n1x,n1y),4)
        for col in self.colliders:
            px = int(col.pos.get_x())
            py = int(col.pos.get_y())
            r = int(col.radius)
            pygame.draw.circle(screen,ORANGE,(px,py),r,3)
