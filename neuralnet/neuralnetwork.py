from synapse import Synapse
from timemodule import Clock
from neuron import *
import random

clock = Clock()
neurons = []
for i in range(20):
    neurons.append(Neuron(clock.get_time(),7/10))

for i in range(30):
    connect(neurons[random.randrange(20)],neurons[random.randrange(20)]
            ,random.randrange(2),1)

for neuron in neurons:
        print(neuron)
        
while(True):
    command = input().lower()
    if(command == 't'):
        clock.tick(1)
        for neuron in neurons:
            neuron.update_inputs(clock.get_time())
            neuron.update_outputs()
    for neuron in neurons:
        print(neuron)

    
