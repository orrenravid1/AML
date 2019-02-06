import math
import sys,os

p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not (p in sys.path):
    sys.path.insert(0,p)

from AML.neuralnet.synapse import Synapse

class Firing_Model:
    """
    The model that describes how the neuron will fire given that it is activated

    Attributes
    ----------
    model_type : str
        A string describing the type of firing model for this Firing_Model instance
    fire : float
        The duration of time it takes for the neuronal current to reach its peak and return
        approximately to baseline
    refract : float
        The duration of time it takes after firing until the threshold for activation returns to
        baseline
    t_max: float
        The total duration of time it takes of the neuron to fire and return to baseline
    precision: float
        The margin of error within which we want the neuron's baseline to be reached
        Note, this is only used in certain models.
    activation_time : float
        The point of time within the current firing cycle of the neuron
        If it is -1, then the neuron is inactive
    potential : float
        The maximum value the neuronal current is to reach

    Methods
    -------
    curr_val(activation_time)
        Returns the current value of the neuronal current based on the given activation time
    """
    
    def __init__(self, model_type='alpha', **kwargs):
        """
        Parameters
        ----------
        model_type : str, optional
            Describes the type of firing model for this Firing_Model instance
        **fire : float, optional
            Specifies the duration of time it takes for the neuronal current to reach its peak and return
            approximately to baseline
        **refract : float, optional
            Specifies the duration of time it takes after firing until the threshold for activation returns to
            baseline
        **precision: float, optional
            Specifies the margin of error within which we want the neuron's baseline to be reached
            Note, this is only used in certain models
        **activation_time : float, optional
            Describes the point of time within the firing cycle of the neuron which we are in
            currently
            If it is -1, then the neuron is inactive
        **potential : float, optional
            Specifies the maximum value the neuronal current is to reach
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
        Returns the current value of the neuronal current

        Parameters
        ----------
        activation_time : float, optional
            The point of time within the current firing cycle of the neuron
            If it is -1, then the neuron is inactive

        Returns
        -------
        float
            The neuronal current as a function of the model's type, parameters, and activation time
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
    The model that describes how the neuron will fire given that it is activated

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
        The duration of time it takes for the neuronal current to reach its peak and return
        approximately to baseline
    refract : float
        The duration of time it takes after firing until the threshold for activation returns to
        baseline
    t_max: float
        The total duration of time it takes of the neuron to fire and return to baseline

    Methods
    -------
    update_threshold(activation_time)
        Modifies the model's current threshold based on the model type and parameters
    """
    
    def __init__(self, model_type, threshold, fire=2, refract=4):
        """
        Parameters
        ----------
        model_type : str
            A string describing the type of firing model for this Firing_Model instance
        threshold : float
            Defines the value of input at which point the neuron goes from being inactive to active
        fire : float, optional
            Defines the duration of time it takes for the neuronal current to reach its peak and return
            approximately to baseline
        refract : float, optional
            The duration of time it takes after firing until the threshold for activation returns to
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
        current activation time of the neuron's firing cycle
        
        Parameters
        ----------
        activation_time : float
            The point of time within the current firing cycle of the neuron
            If it is -1, then the neuron is inactive
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
                self.curr_threshold = self.threshold

class Synapse_Model:
    """
    The model that describes how the neuron interacts with synapses

    Attributes
    ----------
    threshold : float
        The value of input at which point the neuron goes from being inactive to active
    lr : float
        A value defining the amount by which synaptic weights are modified per time step
    sin : list
        A list of synaptic inputs to the neuron
    sout : list
        A list of synaptic outputs from the neuron

    Methods
    -------
    update_threshold(activation_time)
        Modifies the model's current threshold based on the model type and parameters
    """
    
    def __init__(self, threshold, lr, sin, sout):
        """
        Parameters
        ----------
        threshold : float
            Specifies the value of input at which point the neuron goes from being inactive to active
        lr : float
            Specifies the amount by which synaptic weights are modified per time step
        sin : list
            Specifies the list of synaptic inputs to the neuron
        sout : list
            Specifies the list of synaptic outputs from the neuron
        """
        
        self.threshold = threshold
        self.lr = lr
        self.sin = sin
        self.sout = sout
        
    def get_synapses_in(self):
        """
        Aggregates the input current and potential based on the input from the neuron's synaptic inputs.

        Returns
        -------
        tuple
            A tuple of the aggregated synapse values and the aggregated synapse potentials
        """
        
        s = 0
        p = 0
        for synapse in self.sin:
            s += synapse.value
            p += synapse.potential
        return (s,p)
    
    def update_synapses_out(self, curr):
        """
        Updates the output of the neuron to its synaptic outputs based on the value of its neuronal
        current and updates the weights of each synapse accordingly

        Parameters
        ----------
        curr : float
            The neuronal current
        """
        
        if curr >= self.threshold:
            for synapse in self.sout:
                # Currently outputs an output of unit size
                # i.e. value/potential = potential/potential
                # Inhibitory vs excitory represented by synapse.sign
                synapse.value = synapse.sign*synapse.potential*synapse.weight
                # Strengthen synaptic weight each time the connected neurons fire together
                # by the Hebbian learning rule
                # i.e. neurons that fire together wire together
                firing_correlation = (synapse.origin.curr/synapse.origin.potential *
                                      synapse.dest.curr/synapse.dest.potential)
                synapse.weight += self.lr*firing_correlation
                if synapse.weight > 1:
                    synapse.weight = 1
        else:
            for synapse in self.sout:
                # Weaken synaptic weight each time synapse doesn't fire
                synapse.value = 0
                synapse.weight = synapse.weight - self.lr
                if synapse.weight < 0:
                    synapse.weight = 0
        
class Neuron:
    """
    A spiking neuron with a modular firing and threshold models

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
    update_inputs(curr_time)
        Aggregates the input current based on the input from the neuron's synaptic inputs,
        activation time, and threshold model.
    update_outputs()
        Updates the output of the neuron to its synaptic outputs based on the value of its neuronal
        current and updates the weights of each synapse accordingly
    add_sin(synapse)
        Adds a synapse to the neuron's synaptic inputs
    add_sout(synapse)
        Adds a synapse to the neuron's synaptic outputs
    remove_sin(synapse)
        Removes the specified synapse from the neuron's synaptic inputs
    remove_sout(synapse)
        Removes the specified synapse from the neuron's synaptic outputs
    """
    
    def __init__(self, threshold, init_time = 0,**kwargs):
        """
        Parameters
        ----------
        threshold : float
            Defines the value of input at which point the neuron goes from being inactive to active
        init_time : float, optional
            Defines the starting time in ms from the reference point of the neuron
        **sout : list, optional
            Defines the list of Synapse objects that serve as the outputs from this neuron
        **sin : list, optional
            Defines the list of Synapse objects that serve as the inputs to this neuron
        **potential : float, optional
            Specifies the maximum value the neuronal current is to reach
        **fire : float, optional
            Specifies the duration of time it takes for the neuronal current to reach its peak and return
            approximately to baseline
        **refract : float, optional
            Specifies the duration of time it takes after firing until the threshold for activation returns to
            baseline
        **threshold_model_type: str, optional
            Specifies the type of threshold model for this neuron
        **precision : float, optional
            Specifies the margin of error within which we want the neuron's baseline to be reached
        **firing_model_type : str, optional
            Specifies the type of firing model for this neuron
        **synapse_threshold : float, optional
            Defines the threshold required for an outgoing synapse to be activated
        **synapse_lr : float, optional
            Defines the amount by which synaptic weights are modified for each timestep
            If the value is 0, the synaptic weights do not change
        """
        
        self.sout = kwargs.get('sout',[])
        self.sin = kwargs.get('sin',[])
        self.potential = kwargs.get('potential',1)
        self.curr = 0
        # Note: set fire to 1 ms to make it biologically reasonable,
        # set refract to 3-4 ms to make it biologically reasonable
        fire = kwargs.get('fire', 2)
        refract = kwargs.get('refract', 4)
        # Threshold must be a number between 0 and 1
        threshold_model_type = kwargs.get('threshold_model', 'quadratic')
        self.threshold_model = Threshold_Model(threshold_model_type, threshold, fire, refract)
        precision = kwargs.get('precision', 0.97)
        self.activation_time = -1
        firing_model_type = kwargs.get('firing_model', 'alpha')
        self.firing_model = Firing_Model(firing_model_type, potential=self.potential,
                                         precision=precision, fire=fire, refract=refract,
                                         activation_time=self.activation_time)
        synapse_threshold = kwargs.get('synapse_threshold', 0.5)
        synapse_lr = kwargs.get('learning_rate', 0)
        self.synapse_model = Synapse_Model(synapse_threshold, synapse_lr, self.sin, self.sout)
        self.curr_time = init_time
        
    def curr_val(self):
        """
        Returns the current value of the neuronal current based on the neuron's firing model
        and activation time

        Returns
        -------
        float
            The neuronal current as a function of the firing model's type, parameters, and activation time
        """
        
        return self.firing_model.curr_val(self.activation_time)
        
    def update_inputs(self, curr_time):
        """
        Aggregates the input current based on the input from the neuron's synaptic inputs,
        activation time, and threshold model

        Parameters
        ----------
        curr_time : float
            The new current time.
        """
                
        # Get change in time
        deltatime = curr_time - self.curr_time
        self.curr_time = curr_time
        
        # If the neuron is activated, add deltatime to its activation time
        if(self.activation_time >= 0):
            self.activation_time += deltatime

        # Get the aggregated synaptic inputs and their corresponding aggregated potentials
        s, p = self.synapse_model.get_synapses_in()
            
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
        curr_threshold = self.threshold_model.curr_threshold

        # If the neuronal current is greater than the new threshold, the neuron is activated again
        if(curr >= curr_threshold):
            self.activation_time = 0
            
        # Check to see if neuron is no longer activated
        if(self.activation_time > self.firing_model.t_max):
            self.activation_time = -1
            
        self.curr = self.curr_val()

    def update_outputs(self):
        """
        Updates the output of the neuron to its synaptic outputs based on the value of its neuronal
        current and updates the weights of each synapse accordingly
        """
        
        self.synapse_model.update_synapses_out(self.curr)

    def add_sin(self,synapse):
        """
        Adds a synapse to the neuron's synaptic inputs

        Parameters
        ----------
        synapse : Synapse
            The synapse to be added
        """
        
        self.sin.append(synapse)

    def add_sout(self,synapse):
        """
        Adds a synapse to the neuron's synaptic outputs

        Parameters
        ----------
        synapse : Synapse
            The synapse to be added
        """
        
        self.sout.append(synapse)

    def remove_sin(self,synapse):
        """
        Removes the specified synapse from the neuron's synaptic inputs

        Parameters
        ----------
        synapse : Synapse
            The synapse to be removed
        """
        
        if(synapse in self.sin):
            del(self.sin[index(synapse)])

    def remove_sout(self,synapse):
        """
        Removes the specified synapse from the neuron's synaptic outputs

        Parameters
        ----------
        synapse : Synapse
            The synapse to be removed
        """
        
        if(synapse in self.sout):
            del(self.sout[index(synapse)])

    def __repr__(self):
        return ("Neuron(" + "Curr:" + str(self.curr) +
                ", " + "AT:" + str(self.activation_time) +
                ")")

    def __str__(self):
        return self.__repr__()

# TODO: Change parameters of connect to match Synapse constructor
def connect(nout,nin,val,pot,**kwargs):
    """
    Connects two neurons by a synapse.

    Parameters
    ----------
    nout : Neuron
        The neuron to be connected to the input of the synapse.
    nin : Neuron
        The neuron for which the output of the synapse will be the input
        of the neuron
    """
    synapse = Synapse(val,pot,nout,nin,**kwargs)
    if not(nout is None):
        nout.add_sout(synapse)
    if not(nin is None):
        nin.add_sin(synapse)
    return synapse
