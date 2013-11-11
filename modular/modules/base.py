class Module(object):
    """Module is the base class for modules.
    
    A Module instance provides a process method that returns a Module instance
    that holds an output calculated from an input and eventualy some additional
    internal state. If a Module instance is not originating from a call to the
    process method, it's output value must be None.
    
    The Module base class is not intended to be instantiated. Instances of
    subclasses of Module should be immutable.
    
    """
    @classmethod
    def create(cls):
        """Creates a new instance with output None."""
        return cls()
    
    def __init__(self, output = None):
        """Creates a new instance with a given output or None."""
        self.__output = output
    
    def get_output(self):
        """Returns the output value held by the current instance.
        
        The output value is the processing result from the call to the process
        method that created the current instance, or None if the instance was
        not created by the process method.
        
        """
        return self.__output
    
    def process(self, input_):
        """Returns an instance holding the output calculated from the given input.
        
        Subclasses of Module must implement this method.
        
        """
        raise NotImplementedError

class Sum(Module):
    """Sums the input."""
    def __init__(self, output = None):
        """Initializes a new instance with the given output or None."""
        super(Sum, self).__init__(output)
        
    def process(self, input_):
        """Returns a Sum instance that holds the summed input.
        
        For strings the summed input is the concatenation of the strings in
        the input.
        
        """
        #TODO implement other types :(
        return Sum("".join(input_))

def process(module, input_):
    """Returns the processed module and the output value calculated from the given input."""
    processed = module.process(input_)
    
    return processed, processed.get_output()

_SUM = Sum()
     
def sum_input(input_):
    """Processes the input with the Sum module and returns the resulting output."""
    return _SUM.process(input_).get_output()