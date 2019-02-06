import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.neuralnet.synapse import *

class Neuron:
    def __init__(self,init_time,threshold,**kwargs):
        #self.parentcol = kwargs.get('parentcol',None)
        self.sout = kwargs.get('sout',[])
        self.sin = kwargs.get('sin',[])
        self.potential = kwargs.get('potential',1)
        self.debug = kwargs.get('debug',False)
        #threshold should be a number between 0 and 1
        self.threshold = threshold
        self.precision = 0.97
        self.curr = 0
        #Note: add self.capacity for more biologically significant results
        self.activation_time = -1
        #Note: set fire to 1 ms to make it biologically reasonable
        #set refract to 3-4 ms to make it biologically reasonable
        self.fire = 2
        self.refract = 4
        self.currtime = init_time
        
    def currval(self):
        if(self.activation_time < 0):
            return 0
        '''
        #this model is p_0*e^(-beta*t)
        t_max = self.fire+self.refract
        beta = math.log(((1-self.precision)))/t_max
        return self.potential*math.exp(beta*self.activation_time)
        '''
        #this model is p_0*a*t*e^(1-at) which better models the action potential
        #a is chosen such that the peak of the function occurs at self.fire/2
        #since the peak is at t = 1/a, then a = 2/self.fire
        a = 2/self.fire
        t = self.activation_time
        return self.potential*a*t*math.exp(1-a*t)
        
    def update_inputs(self,currtime):
        #get change in time
        deltatime = currtime-self.currtime
        self.currtime = currtime
        
        #if the neuron is activated, add deltatime to its activation time
        if(self.activation_time >= 0):
            self.activation_time += deltatime
            
        #aggregate synaptic inputs to current value
        s = 0
        p = 0
        for synapse in self.sin:
            if(synapse.value != 0):
                s += synapse.value
                p += synapse.potential
            
        #normalize aggregated synaptic inputs
        if(p == 0):
            ins = 0
        else:
            ins = s/p
            
        #Use this section if threshold is dynamically defined
        #if the neuron is at resting potential, its firing should only depend on inputs
        #otherwise, it should depend on its current value and the inputs
        if(self.activation_time < 0):
            curr = ins
            if(curr < 0):
                curr = 0
        else:
            curr = (self.curr + s)/(self.potential + p)
        
        #Increase the threshold depending on recency of action potential

        #quadratic model for modulating action potential
        if(self.activation_time > 0):
            currthreshold = (self.threshold +
                             (1-self.threshold)*(1-(self.activation_time/
                                            (self.fire+self.refract))**2))
        else:
            currthreshold = self.threshold
        
        '''
        #linear model for modulating action potential
        if(self.activation_time > 0):
            currthreshold = (self.threshold +
                             (1-self.threshold)*(1-self.activation_time/
                                            (self.fire+self.refract)))
        else:
            currthreshold = self.threshold
        '''
        '''
        #Alternate model uses current neuronal value to modulate threshold
        if(self.activation_time > 0):
            currthreshold = (self.threshold +
                             (1-self.threshold)*(1-self.curr/self.potential))
        else:
            currthreshold = self.threshold
        '''
        #check for activation
        '''
        #Use this version if threshold is not dynamically defined
        if((self.activation_time > self.fire or self.activation_time < 0)
           and curr >= currthreshold):
            self.activation_time = 0
        '''
        #Use this version if threshold is dynamically defined
        if(curr >= currthreshold):
            self.activation_time = 0
            
        #check to see if neuron is no longer activated
        if(self.activation_time > self.fire+self.refract):
            self.activation_time = -1  
        self.curr = self.currval()

        if(self.debug):
            return [self.curr, currthreshold]

    def update_outputs(self):
        if(self.activation_time < self.fire and self.activation_time >= 0):
            for synapse in self.sout:
                synapse.potential = self.potential*synapse.weight
                #currently outputs an output of unit size
                #i.e. value/potential = potential/potential
                #inhibitory vs excitory represented by synapse.sign
                synapse.value = synapse.sign*synapse.potential
        else:
            for synapse in self.sout:
                synapse.value = 0

    def add_sin(self,synapse):
        self.sin.append(synapse)

    def add_sout(self,synapse):
        self.sout.append(synapse)

    def remove_sin(self,synapse):
        if(synapse in self.sin):
            del(self.sin[index(synapse)])

    def remove_sout(self,synapse):
        if(synapse in self.sout):
            del(self.sout[index(synapse)])

    def __repr__(self):
        return ("neuron(" + "Curr:" + str(self.curr) +
                ", " + "AT:" + str(self.activation_time) +
                ")")

    def __str__(self):
        return self.__repr__()
        
