import pygame
import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0, p)

from AML.mathlib.math2d import*
from AML.graphics.collidergraphics import*

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

prevtime = pygame.time.get_ticks()
currtime = pygame.time.get_ticks()

def deltaTime():
    return (currtime-prevtime)/1000
    
circle = CircleColliderG(Vector2(150,30),15)
circlev = Vector2(0,0)
surf1 = SurfaceColliderG(Vector2(100,100),Vector2(300,100))
surf2 = SurfaceColliderG(Vector2(400,300),Vector2(500,100))
surf3 = SurfaceColliderG(Vector2(10,50),Vector2(10,250))

surfs = [surf1,surf2,surf3]

shouldprint = True

speed = 200
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    keys = pygame.key.get_pressed()

    circlev = Vector2(0,0)
    
    if keys[pygame.K_a]:
        circlev.set_x(-speed*deltaTime())
    elif keys[pygame.K_d]:
        circlev.set_x(speed*deltaTime())
    if keys[pygame.K_w]:
        circlev.set_y(-speed*deltaTime())
    elif keys[pygame.K_s]:
        circlev.set_y(speed*deltaTime())
     
    screen.fill(WHITE)

    circle.pos += circlev

    for i,surf in enumerate(surfs):
        col = circle.get_collision(surf)
        shouldprint = col[0]
        if(shouldprint):
            print(str(i) + ": " + str(surf.p1) + "," + str(surf.p2) + str(col))
            coldepth = col[1].coldepth
            circle.pos -= coldepth
        surf.draw(screen)
    
    circle.draw(screen)
    
    pygame.display.flip()
    clock.tick(20)
    prevtime = currtime
    currtime = pygame.time.get_ticks()

pygame.quit()
