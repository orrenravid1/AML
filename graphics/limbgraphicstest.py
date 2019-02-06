import pygame
import sys,os
import random

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.graphics.limbgraphics import LimbG
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

l1 = LimbG(Vector2(50,50),Vector2(100,100),3)
l2 = LimbG(l1.get_node(1),Vector2(200,30),3)
l3 = LimbG(l2.get_node(1),Vector2(400,10),3)
l1.add_child(l2,True)
l2.add_child(l3,True)

limbs = [l1,l2,l3]

l1.translate(Vector2(300,300))

a = 4
b = 3
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        a = -4
    if keys[pygame.K_d]:
        a = 4
    if keys[pygame.K_w]:
        b = -4
    if keys[pygame.K_s]:
        b = 4

    screen.fill(WHITE)
    for l in limbs:
        l.draw(screen)

    l3.rotate_about(-a, l3.get_shared_joint(l2))
    l2.rotate_about(-b, l2.get_shared_joint(l1))
    l1.rotate_about(-1, l1.get_node(0))
    pygame.display.flip()
    clock.tick(20)

pygame.quit()
