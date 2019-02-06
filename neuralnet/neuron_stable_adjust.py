import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.neuralnet.synapse import *

class Firing_Model:
    """
    The model that describes how the neuron will fire given that it is activated.

    Attributes
    ----------
    model_type : str
        A string describing the type of firing model for this Firing_Model instance
    fire : float
        The duration of time it takes for the neuronal current to reach its peak
    refract : float
        The duration of time it takes after reaching the peak current to go back to
        baseline current
    t_max: float
        The total duration of time it takes of the neuron to fire and return to baseline
    precision: float
        The margin of error within which we want the neuron's baseline to be reached.
        Note, this is only used in certain models.
    activation_time : float
        The point of time within the current firing cycle of the neuron.
        If it is -1, then the neuron is inactive.
    potential : float
        The maximum value the neuronal current is to reach.

    Methods
    -------
    curr_val(activation_time)
        Returns the current value of the neuronal current based on the given activation time
    """
    
    def __init__(self, model_type='alpha', **kwargs):
        """
        Parameters
        ----------
        model_type : str
            Describes the type of firing model for this Firing_Model instance
        **fire : float
            Specifies the duration of time it takes for the neuronal current to reach its peak
        **refract : float
            Specifies the duration of time it takes after reaching the peak current to go back to
            baseline current
        **precision: float
            Specifies the margin of error within which we want the neuron's baseline to be reached.
            Note, this is only used in certain models.
        **activation_time : float
            Describes the point of time within the firing cycle of the neuron which we are in
            currently.
            If it is -1, then the neuron is inactive.
        **potential : float
            Specifies the maximum value the neuronal current is to reach.
        """
        
        self.model_type = model_type
        self.fire = kwargs.get('fire', 2)
        self.refract = kwargs.get('refract', 4)
        self.t_max = self.fire + self.refract
        self.precision = kwargs.get('precision', 0.97)
        self.activation_time = kwargs.get('activation_time', -1)
        self.potential = kwargs.get('potential', 1)
        
    def curr_val(self, activation_time = -1):
        """
        Returns the current value of the neuronal current.

        Parameters
        ----------
        activation_time : float
            The point of time within the current firing cycle of the neuron.
            If it is -1, then the neuron is inactive.

        Returns
        -------
        float
            The neuronal current as a function of the model's type, parameters, and activation time.
        """
        
        self.activation_time = activation_time
        if(self.activation_time < 0):
            return 0
        if self.model_type == 'neg_exp':
            # This model is p_0*e^(-beta*t)
            beta = math.log(1-self.precision)/self.t_max
            return self.potential*math.exp(beta*self.activation_time)
        elif self.model_type == 'alpha':
            # This model is p_0*a*t*e^(1-at) which better models the action potential
            # a is chosen such that the peak of the function occurs at self.fire/2
            # since the peak is at t = 1/a, then a = 2/self.fire
            alpha = 2/self.fire
            return self.potential*alpha*self.activation_time*math.exp(1-alpha*self.activation_time)


class Threshold_Model:
    """
    The model that describes how the neuron will fire given that it is activated.

    Attributes
    ----------
    model_type : str
        A string describing the type of firing model for this Firing_Model instance
    threshold : float
        The value of input at which point the neuron goes from being inactive to active
    curr_threshold : float
        The current value of the threshold, which may vary as a function of the activation
        time
    fire : float
        The duration of time it takes for the neuronal current to reach its peak
    refract : float
        The duration of time it takes after reaching the peak current to go back to
        baseline current
    t_max: float
        The total duration of time it takes of the neuron to fire and return to baseline

    Methods
    -------
    update_threshold(activation_time)
        Modifies the model's current threshold based on the model type and parameters.
    """
    
    def __init__(self, model_type, threshold, fire=2, refract=4):
        """
        Parameters
        ----------
        model_type : str
            A string describing the type of firing model for this Firing_Model instance
        threshold : float
            Defines the value of input at which point the neuron goes from being inactive to active
        curr_threshold : float
            Holds the current value of the threshold, which may vary as a function of the activation
            time
        fire : float
            Defines the duration of time it takes for the neuronal current to reach its peak
        refract : float
            Defines the duration of time it takes after reaching the peak current to go back to
            baseline current
        t_max: float
            Represents the total duration of time it takes of the neuron to fire and return to
            baseline
        """
        
        self.model_type = model_type
        self.threshold = threshold
        self.curr_threshold = threshold
        self.fire = fire
        self.refract = refract
        self.t_max = self.fire + self.refract
        
    def update_threshold(self, activation_time):
        """
        Modifies the model's current threshold based on the model type and parameters and on the
        current activation time of the neuron's firing cycle.
        
        Parameters
        ----------
        activation_time : float
            The point of time within the current firing cycle of the neuron.
            If it is -1, then the neuron is inactive.
        """
        
        if self.model_type == 'linear':
            if(activation_time > 0):
                self.curr_threshold = (self.threshold +
                                 (1-self.threshold)*(1-activation_time/
                                                (self.t_max)))
            else:
                self.curr_threshold = self.threshold
        elif self.model_type == 'quadratic':
            if(activation_time > 0):
                self.curr_threshold = (self.threshold +
                                 (1-self.threshold)*(1-(activation_time/
                                                (self.t_max))**2))
            else:
                self.currthreshold = self.threshold
            
        
class Neuron:
    """
    A spiking neuron with a modular firing and threshold model.

    Attributes
    ----------
    sout : list
        A list of Synapse objects that serve as the outputs from this neuron.
    sin : list
        A list of Synapse objects that serve as the inputs to this neuron.
    potential : float
        The maximum value the neuronal current is to reach.
    curr: float
        The current neuronal current.
    threshold_model: Threshold_Model
        The model describing the behavior of the threshold of the neuron.
    activation_time : float
        The point of time within the current firing cycle of the neuron.
        If it is -1, then the neuron is inactive.
    firing_model : Firing_Model
        The model describing the behavior of how the neuron fires when it is activated.
    curr_time : float
        The time in ms from the point of reference of the neuron.

    Methods
    -------
    curr_val()
        Returns the current value of the neuronal current based on the neuron's firing model
        and activation time
    update_inputs(currtime)
        Updates the current value of the neuron based on the input from the neuron's synaptic inputs,
        activation time, and threshold model.
    update_outputs()
        Updates the output of the neuron to its synaptic outputs based on the value of its neuronal
        current and updates the weights of each synapse accordingly
    add_sin(synapse)
        Add a synapse to the neuron's synaptic inputs
    add_sout(synapse)
        Add a synapse to the neuron's synaptic outputs
    remove_sin(synapse)
        Remove the specified synapse from the neuron's synaptic inputs
    remove_sout(synapse)
        Remove the specified synapse from the neuron's synaptic outputs
    """
    
    def __init__(self, threshold, init_time = 0,**kwargs):
        #self.parentcol = kwargs.get('parentcol',None)
        self.sout = kwargs.get('sout',[])
        self.sin = kwargs.get('sin',[])
        self.potential = kwargs.get('potential',1)
        self.curr = 0
        # Note: set fire to 1 ms to make it biologically reasonable,
        # set refract to 3-4 ms to make it biologically reasonable
        fire = kwargs.get('fire', 2)
        refract = kwargs.get('refract', 4)
        # Threshold should be a number between 0 and 1
        threshold_model_type = kwargs.get('threshold_model', 'quadratic')
        self.threshold_model = Threshold_Model(threshold_model_type, threshold, fire, refract)
        precision = kwargs.get('precision', 0.97)
        # Note: add self.capacity for more biologically significant results
        self.activation_time = -1
        firing_model_type = kwargs.get('firing_model', 'alpha')
        self.firing_model = Firing_Model(firing_model_type, potential=self.potential,
                                         precision=precision, fire=fire, refract=refract,
                                         activation_time=self.activation_time)
        self.currtime = init_time
        
    def currval(self):
        return self.firing_model.curr_val(self.activation_time)
        
    def update_inputs(self, currtime):
        # Get change in time
        print(currtime, self.currtime)
        deltatime = currtime - self.currtime
        self.currtime = currtime
        
        # If the neuron is activated, add deltatime to its activation time
        if(self.activation_time >= 0):
            self.activation_time += deltatime
            
        # Aggregate synaptic inputs to current value
        s = 0
        p = 0
        for synapse in self.sin:
            s += synapse.value
            p += synapse.potential
            
        # Normalize aggregated synaptic inputs
        if(p == 0):
            ins = 0
        else:
            ins = s/p
            
        # If the neuron is at resting potential, its firing should only depend on inputs.
        # Otherwise, it should depend on its current value and the inputs
        if(self.activation_time < 0):
            curr = ins
            if(curr < 0):
                curr = 0
        else:
            curr = (self.curr + s)/(self.potential + p)
        
        # Modify the threshold depending on recency of action potential
        self.threshold_model.update_threshold(self.activation_time)
        currthreshold = self.threshold_model.curr_threshold

        # If the neuronal current is greater than the new threshold, the neuron is activated again
        if(curr >= currthreshold):
            self.activation_time = 0
            
        # Check to see if neuron is no longer activated
        if(self.activation_time > self.firing_model.t_max):
            self.activation_time = -1
            
        self.curr = self.currval()

    def update_outputs(self):
        wadd = 0.01
        '''
        if(self.activation_time < self.fire and self.activation_time >= 0):
        '''
        if self.curr >= 0.5:
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
        return ("Neuron(" + "Curr:" + str(self.curr) +
                ", " + "AT:" + str(self.activation_time) +
                ")")

    def __str__(self):
        return self.__repr__()
        
