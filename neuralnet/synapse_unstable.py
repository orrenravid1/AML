import os.path
import sys

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from BioML.mathlib.math2d import Vector, sigmoid


class Synapse:
    '''
    nts - Stores a vector of the neurotransmitters emitted from the presynaptic vesicles
    weights - A vector that models the strength of neurotransmitter receptors at the postsynaptic
              membrane
    external - Stores a vector of the amount of neurotransmitters in local space surrounding the
              synapse
    potential - Stores the resultant potential acquired from nts acting at their respective
                postsynaptic receptor sites both at the previous (0) and current (1) time
    dest - A list of neurons that are connected postsynaptically to the synapse
    origin - A list of neurons that are connected presynaptically to the synapse
    '''
    def __init__(self, origin=[], dest=[], nts=Vector(8), weights = Vector(8),
                 potential=[0,0], external=Vector(8)):
        self.nts = nts
        self.weights = weights
        self.external = external
        self.potential = potential
        self.dpotential = potential[1]-potential[0]
        self.dest = dest
        self.origin = origin
        
    def update_nts(self):
        # Update the neurotransmitter vector by summing the neurotransmitters in each respective
        # neuron.
        for neuron in self.origin:
            nts += self.origin.nts
     
    def update_potential(self):
        # Update the potential by calculating the action of the nts and ambient nts at the postsynaptic
        # receptors (and normalize through sigmoid). Then, set the change in potential.
        self.potential[0] = self.potential[1]
        self.potential[1] = sigmoid(self.weights * (self.nts + self.external))
        self.dpotential = potential[1]-potential[0]
        
    def update_weights(self):
        # Neurons that fire together wire together
        self.weights = self.weights + self.weights*self.dpotential
        # Models nt receptor regulation by downregulating and upregulating at certain thresholds
        threshold = 0.2
        delta = 0.05
        for i in range(self.weights.dim):
            if self.weights[i] < threshold:
                self.weights[i] += delta
            elif self.weights[i] > 1-threshold:
                self.weights[i] -= delta
           
    def update(self):
        self.update_potential()
        self.update_weights()
        
    def __str__(self):
        ret = "Synapse: "
        ret = ret + "(Origin = " + str(self.origin) + ",\n"
        ret = ret + "Dest = " + str(self.dest) + ",\n"
        ret = ret + "NTs = " + str(self.nts) + ",\n"
        ret = ret + "External = " + str(self.external) + ",\n"
        ret = ret + "Weights = " + str(self.weights)
        ret = ret + "Potential = " + str(self.potential) +")"
        return ret

'''
def connect(nout,nin,**kwargs):
    synapse = Synapse(nout,nin)
    if not(nout is None):
        nout.add_sout(synapse)
    if not(nin is None):
        nin.add_sin(synapse)
    return synapse
'''
