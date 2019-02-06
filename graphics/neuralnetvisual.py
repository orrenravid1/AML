import pygame
import sys,os
import random

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.graphics.neurongraphics import *
from AML.mathlib.math2d import Vector2
from AML.neuralnet import timemodule

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

pygame.init()

size = (1080,720)

screen = pygame.display.set_mode(size)

done = False

gclock = pygame.time.Clock()

nclock = timemodule.Clock()

neurons = []
init_threshold = []
n = 30
for i in range(n):
    x = int(size[0]/10+(i%10)*size[0]/12)
    y = (int(i/10)+1)*int(size[1]/(n/10+1))
    pos = (x,y)
    init_time = 0
    threshold = float(random.randrange(4,7))/10
    init_threshold.append([init_time,threshold])
    neurons.append(NeuronG(threshold, pos, init_time))

s = []
for i in range(60):
    a = random.randrange(n)
    b = list(range(n))
    b.remove(a)
    b = random.choice(b)
    syn = random.randrange(2)
    s.append([a,b,syn])
    syn_sign = [-1 for _ in range(10)] + [1 for _ in range(35)]
    connect(neurons[a],neurons[b]
            ,syn,1,sign = random.choice(syn_sign))

##print(init_threshold)
##print(s)

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for neuron in neurons:
        neuron.update()
        neuron.update_inputs(nclock.get_time())
        neuron.update_outputs()

    screen.fill(BLACK)
    
    for neuron in neurons:
        neuron.draw_neuron(screen)
    for neuron in neurons:
        neuron.draw_synapses(screen)

    pygame.display.flip()
    nclock.tick(0.07)
    gclock.tick(20)

pygame.quit()
    

