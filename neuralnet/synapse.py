class Synapse:
    """
    A synapse which follows the Hebbian learning rule.

    Attributes
    ----------
    value : float
        The current value of the synapse
    potential : float
        The highest possible synaptic value (in magnitude)
    origin : Neuron
        The neuron connected to the synaptic input.
    dest : Neuron
        The neuron connected to the synaptic output.
    sign : int
        Whether the synapse is inhibitory (-1) or excitory (+1)
    weight : float
        The value that weights the synaptic output.
    """
    
    def __init__(self,value,potential,origin,dest = None,**kwargs):
        """
        Parameters
        ----------
        value : float
            Stores the current value of the synapse
        potential : float
            Describes highest possible synaptic value (in magnitude)
        origin : Neuron
            Stores the neuron connected to the synaptic input.
        dest : Neuron
            Stores the neuron connected to the synaptic output.
        sign : int
            Whether the synapse is inhibitory (-1) or excitory (+1)
        weight : float
            The value that weights the synaptic output.
        """
        
        self.value = value
        self.potential = potential
        self.origin = origin
        self.dest = dest
        # Sign must be -1 or 1
        self.sign = kwargs.get('sign',1)
        self.weight = kwargs.get('weight',1)

    def __str__(self):
        ret = ""
        ret = ret + "(Origin = " + str(self.origin) + '\n'
        ret = ret + ", Dest = " + str(self.dest) + '\n'
        ret = ret + ", Potential = " + str(self.potential) + '\n'
        ret = ret + ", Sign = " + str(self.sign) + '\n'
        ret = ret + ", Weight = " + str(self.weight) + ")"
        return ret
