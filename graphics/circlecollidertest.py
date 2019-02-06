import pygame
import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

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
    
circle1 = CircleColliderG(Vector2(150,30),15)
circle1v = Vector2(0,0)
circle2 = CircleColliderG(Vector2(200,200),30)
circle2v = Vector2(0,0)

shouldprint = True

speed = 3
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    keys = pygame.key.get_pressed()

    circle1v = Vector2(0,0)
    circle2v = Vector2(0,0)
    
    if keys[pygame.K_a]:
        circle1v.set_x(-speed)
    elif keys[pygame.K_d]:
        circle1v.set_x(speed)
    if keys[pygame.K_w]:
        circle1v.set_y(-speed)
    elif keys[pygame.K_s]:
        circle1v.set_y(speed)

    '''
    if keys[pygame.K_LEFT]:
        circle2v.x = -speed
    elif keys[pygame.K_RIGHT]:
        circle2v.x = speed
    if keys[pygame.K_UP]:
        circle2v.y = -speed
    elif keys[pygame.K_DOWN]:
        circle2v.y = speed
    '''
    
     
    screen.fill(WHITE)

    circle1.pos += circle1v
    circle2.pos += circle2v

    col1 = circle1.get_collision(circle2)
    
    if(col1[0]):
        print(col1)
        colvec= col1[1].colvec
        coldepth= col1[1].coldepth
        circle1.pos -= coldepth/2
        circle2.pos += coldepth/2
    
    circle1.draw(screen)
    circle2.draw(screen)
    
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
