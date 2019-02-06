import pygame
import sys,os
import random

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.graphics.neurongraphics import *
from AML.graphics.limbgraphics import *
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
scale = 0.6
for i in range(n):
    x = (size[0]/10+(i%10)*size[0]/12) * scale
    y = (int(i/10)+1)*int(size[1]/(n/10+1))*scale
    pos = (x,y)
    init_time = 0
    threshold = float(random.randrange(2,7))/10
    init_threshold.append([init_time,threshold])
    neurons.append(NeuronG(threshold, pos, init_time, scale))

s = []
for i in range(60):
    n_a = random.randrange(n)
    n_b = list(range(n))
    n_b.remove(n_a)
    n_b = random.choice(n_b)
    syn = random.randrange(2)
    s.append([n_a,n_b,syn])
    syn_sign = [-1 for _ in range(10)] + [1 for _ in range(35)]
    connect(neurons[n_a],neurons[n_b]
            ,syn,1,sign = random.choice(syn_sign))

l1 = LimbG(Vector2(50,50),Vector2(100,100),3)
l2 = LimbG(l1.get_node(1),Vector2(200,30),3)
l3 = LimbG(l2.get_node(1),Vector2(400,10),3)
l1.add_child(l2,True)
l2.add_child(l3,True)

limbs = [l1,l2,l3]

l1.translate(Vector2(600,350))

a = 4
b = 3
c = 1

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    for neuron in neurons:
        neuron.update()
        neuron.update_inputs(nclock.get_time())
        neuron.update_outputs()

    screen.fill(WHITE)

    for neuron in neurons:
        neuron.draw_neuron(screen)
    for neuron in neurons:
        neuron.draw_synapses(screen)

    for l in limbs:
        l.draw(screen)

    a_curr = a * (neurons[10].curr - neurons[1].curr)
    b_curr = b * (neurons[15].curr - neurons[16].curr)
    c_curr = c * (neurons[13].curr - neurons[20].curr)
    l3.rotate_about(-a_curr, l3.get_shared_joint(l2))
    l2.rotate_about(-b_curr, l2.get_shared_joint(l1))
    l1.rotate_about(c_curr, l1.get_node(0))

    pygame.display.flip()
    nclock.tick(0.07)
    gclock.tick(20)

pygame.quit()
    

