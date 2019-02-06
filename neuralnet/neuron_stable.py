import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.neuralnet.synapse import *

class Firing_Model:
    def __init__(self, model_type, **kwargs):
        self.model_type = model_type
        self.fire = kwargs.get('fire', 2)
        self.precision = kwargs.get('precision', 0.97)
        self.activation_time = kwargs.get('activation_time', -1)
        if self.model_type == 'neg_exp':
            self.refract = kwargs.get('refract', 4)
            self.t_max = self.fire + self.refract     
    def curr_val(self, **kwargs):
        self.activation_time = kwargs.get('activation_time', self.activation_time)
        self.fire = kwargs.get('fire', self.fire)
        self.precision = kwargs.get('precision', self.precision)
        if(self.activation_time < 0):
            return 0
        if self.model_type == 'neg_exp':
            #this model is p_0*e^(-beta*t)
            self.refract = kwargs.get('refract', self.refract)
            self.t_max = self.fire + self.refract
            beta = math.log(1-self.precision)/self.t_max
            return self.potential*math.exp(beta*self.activation_time)
        elif self.model_type == 'alpha':
            #this model is p_0*a*t*e^(1-at) which better models the action potential
            #a is chosen such that the peak of the function occurs at self.fire/2
            #since the peak is at t = 1/a, then a = 2/self.fire
            alpha = 2/self.fire
            return self.potential*alpha*self.activation_time*math.exp(1-alpha*self.activation_time)


class Threshold_Model:
    def __init__(self, model_type, is_dynamic, threshold):
        self.model_type = model_type
        self.is_dynamic = is_dynamic
        self.threshold = threshold
        self.curr_threshold = threshold
    def update_threshold(self, activation_time, fire, refract):
        if model_type == 'linear':
            if(activation_time > 0):
                self.curr_threshold = (self.threshold +
                                 (1-self.threshold)*(1-activation_time/
                                                (fire+refract)))
            else:
                self.curr_threshold = self.threshold
        elif model_type == 'quadratic':
            if(activation_time > 0):
                self.curr_threshold = (self.threshold +
                                 (1-self.threshold)*(1-(activation_time/
                                                (fire+refract))**2))
            else:
                self.currthreshold = self.threshold
            
        
class Neuron:
    def __init__(self,init_time,threshold,**kwargs):
        #self.parentcol = kwargs.get('parentcol',None)
        self.sout = kwargs.get('sout',[])
        self.sin = kwargs.get('sin',[])
        self.potential = kwargs.get('potential',1)
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

    def update_outputs(self):
        wadd = 0.01
        if(self.activation_time < self.fire and self.activation_time >= 0):
            for synapse in self.sout:
                synapse.potential = self.potential*synapse.weight
                #currently outputs an output of unit size
                #i.e. value/potential = potential/potential
                #inhibitory vs excitory represented by synapse.sign
                synapse.value = synapse.sign*synapse.potential
                #strengthen synaptic weight each time synapse fires
                #i.e. neurons that fire together wire together
                synapse.weight += wadd
        else:
            for synapse in self.sout:
                synapse.potential = self.potential*synapse.weight
                synapse.value = 0
                #weaken synaptic weight each time synapse doesn't fire
                if synapse.weight - wadd > 0:
                    synapse.weight -= wadd

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
        
