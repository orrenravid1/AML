import pygame
import sys,os
import random

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.graphics.neurongraphics import NeuronG
from AML.neuralnet.neuron import *
from AML.neuralnet import timemodule
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

gclock = pygame.time.Clock()

nclock = timemodule.Clock()

init_time = 0

sensory = NeuronG(0.1, (300,300), init_time)
motor = NeuronG(0.1, (600,300), init_time)
inhibitor = NeuronG(0.1,(600,600), init_time)

control = connect(None, sensory, 0, 1)
connect(sensory, motor, 0, 1)
connect(inhibitor, motor, 0, 0.2, sign = -1)
connect(inhibitor, inhibitor, 1, 1)

neurons = [sensory,inhibitor,motor]

'''
for neuron in neurons:
    for s in neuron.sout:
        print(s)
    print("------------")
'''

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        control.value = 1
    else:
        control.value = 0
        
    for neuron in neurons:
        neuron.update()
        neuron.update_inputs(nclock.get_time())
        neuron.update_outputs()
    
    screen.fill(WHITE)
    
    for neuron in neurons:
        neuron.draw_neuron(screen)
    for neuron in neurons:
        neuron.draw_synapses(screen)

    pygame.display.flip()
    nclock.tick(0.07)
    gclock.tick(20)

pygame.quit()
