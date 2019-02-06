import pygame
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.neuralnet.neuron import *
from AML.mathlib.math2d import Vector2

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


class NeuronG(Neuron):
    def __init__(self, threshold, pos, init_time = 0, scale = 1, **kwargs):
        super().__init__(threshold, init_time, **kwargs)
        self.pos = Vector2(pos)
        self.scale = scale
        val = int(self.curr/self.potential*255)
        self.color = (val,0,255-val)
    def update(self):
        val = int(self.curr/self.potential*255)
        self.color = (val,0,255-val)
    def draw_synapses(self,screen):
        for sout in self.sout:
            val = int(sout.value/sout.potential*255)
            if(val < 0):
                val = abs(val)
                color = (0,val,0)
            else:
                color = (val,0,255-val)
            # Get the origin and destination coordinates in order to draw an
            # arrow indicating the direction of the synapse (only if the synapse
            # is not self-connected i.e. magnitude of dirpos > 0
            dirpos = self.pos - sout.dest.pos
            if dirpos.mag() > 0:
                larrow = Vector2(dirpos.rotate(-45).normalized()) * 12 * self.scale + sout.dest.pos
                rarrow = Vector2(dirpos.rotate(45).normalized()) * 12 * self.scale + sout.dest.pos
                pygame.draw.aaline(screen,color,(int(larrow.get_x()),int(larrow.get_y())),
                                   (int(sout.dest.pos.get_x()),int(sout.dest.pos.get_y())))
                pygame.draw.aaline(screen,color,(int(rarrow.get_x()),int(rarrow.get_y())),
                                   (int(sout.dest.pos.get_x()),int(sout.dest.pos.get_y())))
            pygame.draw.aaline(screen,color,(int(self.pos.get_x()),int(self.pos.get_y())),
                               (int(sout.dest.pos.get_x()),int(sout.dest.pos.get_y())))
            
    def draw_neuron(self, screen):   
        pygame.draw.circle(screen, self.color,
                           (int(self.pos.get_x()),int(self.pos.get_y())), int(20 * self.scale))

