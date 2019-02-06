import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.neuralnet.neuron import *

#shows the vector along which the collision occurred
#and the vector that describes how far along the vector the collision is
#to resolve the collision, simply set the pos to pos - coldepth
class CollisionInstance:
    def __init__(self,colvec,coldepth):
        self.colvec = colvec
        self.coldepth = coldepth
    def __repr__(self):
        return (str((self.colvec.x,self.colvec.y))
                + ", " + str((self.coldepth.x,self.coldepth.y)))

#return a tuple (boolean hasCollided, CollisionInstance collision)
#if hasCollided is False then collision will be None
class CircleCollider:
    def __init__(self,pos,radius,**kwargs):
        self.pos = pos
        self.radius = radius
        self.sout = kwargs.get('sout',[])
        self.is_colliding = kwargs.get('is_colliding',False)
        
    def get_collision(self,other):
        if isinstance(other, CircleCollider):
            if (self.pos - other.pos).mag() < (self.radius + other.radius):
                colvecs = other.pos - self.pos
                colveco = -colvecs
                colvecsu = colvecs/colvecs.mag()
                colvecou = colveco/colveco.mag()
                colvecsr = colvecsu*self.radius + self.pos
                colvecor = colvecou*other.radius + other.pos
                coldepth = colvecsr - colvecor
                self.colliding = True
                return (True,CollisionInstance(colvecs,coldepth))
            else:
                return (False,None)
        elif isinstance(other, SurfaceCollider):
            if(((other.p1.x == other.p2.x) and ((self.pos.y >= other.p1.y and
                                               self.pos.y >= other.p2.y) or
                                               self.pos.y <= other.p1.y and
                                               self.pos.y <= other.p2.y))
               or
               ((other.p1.y == other.p2.y) and ((self.pos.x >= other.p1.x and
                                               self.pos.x >= other.p2.x) or
                                               (self.pos.x <= other.p1.x and
                                               self.pos.x <= other.p2.x)))):
                vsc = other.get_closest(self.pos)
                colvec = vsc - self.pos
                if(colvec.mag() < self.radius):
                    coldepth = -(colvec - (colvec/colvec.mag())*self.radius)
                    self.is_colliding = True
                    return (True,CollisionInstance(colvec,coldepth))
                else:
                    return (False,None)
            elif(((self.pos.x < other.p1.x and self.pos.x < other.p2.x) or
                  (self.pos.x > other.p1.x and self.pos.x > other.p2.x))
                 and
                 ((self.pos.y > other.p1.y and self.pos.y > other.p2.y) or
                   (self.pos.y < other.p1.y and self.pos.y < other.p2.y))):
                vsc = other.get_closest(self.pos)
                colvec = vsc - self.pos
                if(colvec.mag() < self.radius):
                    coldepth = -(colvec - (colvec/colvec.mag())*self.radius)
                    self.is_colliding = True
                    return (True,CollisionInstance(colvec,coldepth))
                else:
                    return (False,None)
            else:
                a = self.pos - other.p2
                b = other.p2 - other.p1
                ap = a - b*((a*b)/(b*b))
                if ap.mag() < self.radius:
                    colvec = -ap
                    coldepth = -(colvec - (colvec/colvec.mag())*self.radius)
                    self.is_colliding = True
                    return (True,CollisionInstance(colvec,coldepth))
                else:
                    return (False,None)
        else:
            return (False,None)
    
    def update_synapse(self):
        if(self.is_colliding):
            for s in self.sout:
                s.value = s.potential*s.sign
        else:
            for s in self.sout:
                s.value = 0
        self.is_colliding = False
        
    def add_sout(self,synapse):
        self.sout.append(synapse)
        
    def remove_sout(self,synapse):
        if(synapse in self.sout):
            del(self.sout[index(synapse)])

#a surface is defined as the line segment vetween 2 points        
class SurfaceCollider:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
    def get_closest(self,pos):
        if((self.p1-pos).mag() <= (self.p2-pos).mag()):
            return self.p1
        else:
            return self.p2
    
