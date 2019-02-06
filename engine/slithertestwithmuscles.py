import pyglet
from pyglet.window import key
import pymunk
from pymunk.pyglet_util import DrawOptions
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)
    
from AML.graphics.neurongraphics import NeuronG
from AML.graphics.limbgraphics import LimbG
from AML.neuralnet.neuron import *
from AML.neuralnet import timemodule
from AML.mathlib.math2d import *


class Muscle:
    def __init__(self, body1, body2, anchor1, anchor2, restlen, force, space):
        contract_len_const = 5/7
        self.contract_len = restlen*contract_len_const + restlen/20
        self.mc = pymunk.constraint.DampedSpring(body1, body2, anchor1, anchor2,
                                                 restlen + restlen/20, 0.2, 0.2)
        self.ml = pymunk.constraint.SlideJoint(body1, body2, anchor1, anchor2,
                                               restlen*contract_len_const,
                                               restlen + restlen/20)
        space.add(self.mc)
        space.add(self.ml)
        self.is_contracting = False
        self.is_contracted = False
        self.body1 = body1
        self.body2 = body2
        self.force = force
    def contract(self):
        self.is_contracting = True
    def relax(self):
        self.is_contracting = False
    def _update(self):
        b1posvec = (pymunk.vec2d.Vec2d(self.mc.anchor_a) +
                    pymunk.vec2d.Vec2d(self.body1.position))
        b2posvec = (pymunk.vec2d.Vec2d(self.mc.anchor_b) +
                    pymunk.vec2d.Vec2d(self.body2.position))
        bdist = b1posvec.get_distance(b2posvec)
        if bdist <= self.contract_len:
            self.is_contracted = True
        else:
            self.is_contracted = False
        b1forcevec = (b2posvec - b1posvec).normalized()*self.force
        if not self.is_contracting:
            b1forcevec = -b1forcevec
        b2forcevec = -b1forcevec
        
        self.body1.apply_force_at_local_point(b1forcevec, self.mc.anchor_a)
        self.body2.apply_force_at_local_point(b2forcevec, self.mc.anchor_b)
            
    def debug_draw(self):
        b1posvec = (pymunk.vec2d.Vec2d(self.mc.anchor_a) +
                    pymunk.vec2d.Vec2d(self.body1.position))
        b2posvec = (pymunk.vec2d.Vec2d(self.mc.anchor_b) +
                    pymunk.vec2d.Vec2d(self.body2.position))
        b1forcevec = (b2posvec - b1posvec).normalized()*40
        if not self.is_contracting:
            b1forcevec = -b1forcevec
        b2forcevec = -b1forcevec
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ('v2f', (b1posvec.x, b1posvec.y,
                                     (b1posvec + b1forcevec).x,
                                     (b1posvec + b1forcevec).y)))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                             ('v2f', (b2posvec.x, b2posvec.y,
                                     (b2posvec + b2forcevec).x,
                                     (b2posvec + b2forcevec).y)))


            
window = pyglet.window.Window(1280, 720, "SlitherTest", resizable=False)
keys = key.KeyStateHandler()
window.push_handlers(keys)
options = DrawOptions()

space = pymunk.Space()
space.gravity = 0, 0
# Viscosity of the space
space.damping = 0.2

# Defining the bounds of the screen
size = window.get_size()
framel = pymunk.Body(body_type=pymunk.Body.STATIC)
framelshape = pymunk.Segment(framel, (0,0), (0,size[1]), 1)
frameu = pymunk.Body(body_type=pymunk.Body.STATIC)
frameushape = pymunk.Segment(frameu, (0,size[1]), size, 1)
framer = pymunk.Body(body_type=pymunk.Body.STATIC)
framershape = pymunk.Segment(framer, size, (size[0],0), 1)
frameb = pymunk.Body(body_type=pymunk.Body.STATIC)
framebshape = pymunk.Segment(frameb, (size[0],0), (0,0), 1)
space.add(framel, framelshape, frameu, frameushape, framer, framershape, frameb, framebshape)

numbodies = 9
mass = 6
moment = 200

bodies = [pymunk.Body(mass,moment) for _ in range(numbodies)]
bodyposvecs = []
shapes = []
for i, body in enumerate(bodies):
    body.position = (100 + i*100), 500
    bodyposvecs.append(pymunk.vec2d.Vec2d(body.position))
    shapes.append(pymunk.Circle(body, 20))

force = 1000
muscles = []
for i in range(0, numbodies-2, 2):
    dist = bodyposvecs[i].get_distance(bodyposvecs[i+2])
    muscles.append(Muscle(bodies[i], bodies[i+2], (0, shapes[i].radius),
                    (0, shapes[i+2].radius), dist, force, space))
    muscles.append(Muscle(bodies[i], bodies[i+2], (0, -shapes[i].radius),
                    (0, -shapes[i+2].radius), dist, force, space))
flip = False
for i, muscle in enumerate(muscles):
    if i%2 == 0:
        muscle.is_contracting = True
        flip = not flip
    if flip:
        muscle.is_contracting = not muscle.is_contracting

for body in bodies:
    space.add(body)

for shape in shapes:
    space.add(shape)

for i in range(0, numbodies-1):
    cb = pymunk.PinJoint(bodies[i], bodies[i+1])
    space.add(cb)
for i in range(0, numbodies-2, 2):
    cb1l = pymunk.PinJoint(bodies[i], bodies[i+1], (0, shapes[i].radius))
    cb1r = pymunk.PinJoint(bodies[i], bodies[i+1], (0, -shapes[i].radius))
    cb3l = pymunk.PinJoint(bodies[i+2], bodies[i+1], (0, shapes[i+2].radius))
    cb3r = pymunk.PinJoint(bodies[i+2], bodies[i+1], (0, -shapes[i+2].radius))
    space.add(cb1l, cb1r, cb3l, cb3r)

init_time = 0
scale = 0.6
refract = 0.5
fire = 6
n = len(range(0, numbodies-2, 2))

excitory_lefts = [NeuronG(0.1, ((100 + i*100)*scale, 300*scale), init_time, scale,
                          refract=refract, fire=fire) for i in range(n)]
inhibitory_lefts = [NeuronG(0.1, ((200 + i*100)*scale, 300*scale), init_time, scale,
                            refract=refract, fire=fire) for i in range(n)]
motor_lefts = [NeuronG(0.1, ((150 + i*100)*scale, 200*scale), init_time, scale,
                       refract=refract, fire=fire) for i in range(n)]
excitory_rights = [NeuronG(0.1, ((100 + i*100)*scale, 400*scale), init_time, scale,
                           refract=refract, fire=fire) for i in range(n)]
inhibitory_rights = [NeuronG(0.1, ((200 + i*100)*scale, 400*scale), init_time, scale,
                             refract=refract, fire=fire) for i in range(n)]
motor_rights = [NeuronG(0.1, ((150 + i*100)*scale, 500*scale), init_time, scale,
                        refract=refract, fire=fire) for i in range(n)]

#Excitation
for i in range(n):
    connect(excitory_lefts[i], inhibitory_lefts[i], 0, 1)
    connect(excitory_lefts[i], motor_lefts[i], 0, 1)
    connect(excitory_lefts[i], inhibitory_rights[i], 0, 1)
    connect(excitory_rights[i], inhibitory_rights[i], 0, 1)
    connect(excitory_rights[i], motor_rights[i], 0, 1)
    connect(excitory_rights[i], inhibitory_lefts[i], 0, 1)
    if i < n-1:
        connect(motor_rights[i], excitory_lefts[i+1], 0, 1)
        connect(motor_lefts[i], excitory_rights[i+1], 0, 1)

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

#Creating Controls
control_1 = connect(None, excitory_lefts[0], 0, 1)
control_2 = connect(None, excitory_rights[0], 0, 1)

neurons = (excitory_lefts + inhibitory_lefts + motor_lefts +
           excitory_rights + inhibitory_rights + motor_rights)
@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)
    for muscle in muscles:
        muscle.debug_draw()
                                 
def update(dt):
    global nclock
    global keys
    if keys[key.A] and control_2.value == 0:
        control_1.value = 1
    else:
        control_1.value = 0
    if keys[key.S] and control_1.value == 0:
        control_2.value = 1
    else:
        control_2.value = 0
    for i in range(0, n):
        if motor_lefts[i].curr >= 0.5:
            muscles[2*i].contract()
        else:
            muscles[2*i].relax()
        if motor_rights[i].curr >= 0.5:
            muscles[2*i+1].contract()
        else:
            muscles[2*i+1].relax()
    for muscle in muscles:
        muscle._update()
    for neuron in neurons:
        neuron.update()
        neuron.update_inputs(nclock.get_time())
        neuron.update_outputs()
    nclock.tick(0.075)
    space.step(dt)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1.0/60)
    nclock = timemodule.Clock()
    pyglet.app.run()
