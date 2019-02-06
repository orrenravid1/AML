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

n = 5

init_time = 0

slr = .3

##excitory_left = NeuronG(0.1, (100, 300), init_time)
excitory_lefts = [NeuronG(0.1, (100 + i*100, 300), init_time, synapse_lr=slr) for i in range(n)]
##inhibitory_left = NeuronG(0.1, (200, 300), init_time)
inhibitory_lefts = [NeuronG(0.1, (200 + i*100, 300), init_time, synapse_lr=slr) for i in range(n)]
##motor_left = NeuronG(0.1, (150, 200), init_time)
motor_lefts = [NeuronG(0.1, (150 + i*100, 200), init_time, synapse_lr=slr) for i in range(n)]
##excitory_right = NeuronG(0.1, (100, 400), init_time)
excitory_rights = [NeuronG(0.1, (100 + i*100, 400), init_time, synapse_lr=slr) for i in range(n)]
##inhibitory_right = NeuronG(0.1, (200, 400), init_time)
inhibitory_rights = [NeuronG(0.1, (200 + i*100, 400), init_time, synapse_lr=slr) for i in range(n)]
##motor_right = NeuronG(0.1, (150, 500), init_time)
motor_rights = [NeuronG(0.1, (150 + i*100, 500), init_time, synapse_lr=slr) for i in range(n)]

#Excitation
for i in range(n):
    connect(excitory_lefts[i], inhibitory_lefts[i], 0, 1)
    connect(excitory_lefts[i], motor_lefts[i], 0, 1)
    connect(excitory_lefts[i], inhibitory_rights[i], 0, 1)
    connect(excitory_rights[i], inhibitory_rights[i], 0, 1)
    connect(excitory_rights[i], motor_rights[i], 0, 1)
    connect(excitory_rights[i], inhibitory_lefts[i], 0, 1)
    if i < 4:
        connect(motor_rights[i], excitory_lefts[i+1], 0, 1)
        connect(motor_lefts[i], excitory_rights[i+1], 0, 1)
        ##connect(inhibitory_rights[i], excitory_rights[i], 0, 1, sign = -1)
'''
connect(excitory_left, inhibitory_left, 0, 1)
connect(excitory_left, motor_left, 0, 1)
connect(excitory_left, inhibitory_right, 0, 1)
connect(excitory_right, inhibitory_right, 0, 1)
connect(excitory_right, motor_right, 0, 1)
connect(excitory_right, inhibitory_left, 0, 1)
'''

#Inhibition
for i in range(n):
    connect(inhibitory_lefts[i], motor_lefts[i], 0, 1, sign = -1)
    connect(inhibitory_rights[i], motor_rights[i], 0, 1, sign = -1)
    connect(motor_lefts[i], inhibitory_lefts[i], 0, 1)
    connect(motor_rights[i], inhibitory_rights[i], 0, 1)
    connect(motor_lefts[i], excitory_lefts[i], 0, 1, sign = -1)
    connect(motor_rights[i], excitory_rights[i], 0, 1, sign = -1)
    connect(inhibitory_lefts[i], excitory_lefts[i], 0, 1, sign = -1)
    connect(inhibitory_rights[i], excitory_rights[i], 0, 1, sign = -1)
'''
connect(inhibitory_left, motor_left, 0, 1, sign = -1)
connect(inhibitory_right, motor_right, 0, 1, sign = -1)
##connect(inhibitory_right, excitory_right, 0, 1, sign = -1)
'''

#Initial conditions
control_1 = connect(None, excitory_lefts[0], 0, 1)
control_2 = connect(None, excitory_rights[0], 0, 1)

neurons = (excitory_lefts + inhibitory_lefts + motor_lefts +
           excitory_rights + inhibitory_rights + motor_rights)

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_d]:
        control_1.value = 1
    else:
        control_1.value = 0
    if keys[pygame.K_s] or keys[pygame.K_d]:
        control_2.value = 1
    else:
        control_2.value = 0
        
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
