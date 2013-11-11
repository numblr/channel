class Module(object):
    """Module is the base class for processing units.
    
    A Module instance holds the module's output value. Subclasses of Module
    must implement the process method that creates a new instance which holds the
    processed output value for the given input.
    
    Modules may have additional state other than the output value.
    
    Module is not intended to be instantiated. Instances of subclasses of Module
    should be immutable.
    
    """
    @classmethod
    def create(cls):
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
        
        For strings the summed input is the concatenation of the stirngs in
        the input.
        
        """
        #TODO implement other types :(
        return Sum("".join(input_))

def process(module, input_):
    """Returns the processed module and the output value calculated from the given input."""
    processed = module.process(input_)
    
    return processed, processed.get_output()

_SUM = Sum()
     
def sum_(input_):
    return _SUM.process(input_).get_output()