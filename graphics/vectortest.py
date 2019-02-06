import pygame
import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.mathlib.math2d import *

import random
import time
from pygame.locals import*

pygame.init()
pygame.font.init()

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

colors = [RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,GRAY,BROWN]

size = (1080,720)

screen = pygame.display.set_mode(size)

done = False

clock = pygame.time.Clock()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
    screen.fill(WHITE)

    v1 = Vector2(50,50)
    v1r = 40
    v2 = Vector2(100,100)
    v2r = 50

    v1v2 = v2 - v1
    v2v1 = -v1v2

    v1v2u = v1v2/v1v2.mag()
    v2v1u = v2v1/v2v1.mag()

    v1rv = v1 + v1v2u*v1r
    v2rv = v2 + v2v1u*v2r

    vmid = v2rv - v1rv
    
    pygame.draw.circle(screen,RED,(v1.get_x(),v1.get_y()),v1r)
    pygame.draw.circle(screen,BLUE,(v2.get_x(),v2.get_y()),v2r)
    
    pygame.draw.line(screen,BLACK,(v1.get_x(),v1.get_y()),
                     (v1rv.get_x(),v1rv.get_y()),3)
    pygame.draw.line(screen,WHITE,(v2.get_x(),v2.get_y()),
                     (v2rv.get_x(),v2rv.get_y()),3)
    pygame.draw.line(screen,GRAY,(v1rv.get_x(),v1rv.get_y()),
                     (v1rv.get_x() + vmid.get_x(), v1rv.get_y() + vmid.get_y()),5)
    
    
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
