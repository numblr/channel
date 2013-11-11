from itertools import chain

class Module(object):
    """Module is the base class for processing units for strings.
    
    A Module instance holds the module's current value. Subclasses of Module
    must implement the process method that creates a new instance which holds the
    processed value depending on the given input.
     
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
        """Returns the current value of the Module"""
        return self.__output
    
    def process(self, input_):
        """Creates a instance of the class holding a new value calculated from the given input.
        
        Subclasses of Module must implement this method.
        
        """
        raise NotImplementedError

class Sum(Module):
    def __init__(self, output = None):
        """Initializes a new instance with the given output or None."""
        super(Sum, self).__init__(output)
        
    def process(self, input_):
        """Returns a Sum instance that holds the summed input.
        
        For strings the summed input is the concatenation of the input strings.
        
        """
        #TODO implement other types :)
        return Sum("".join(input_))

def process(module, input_):
    """Returns the processed module and the new value resulting from the given input."""
    processed = module.process(input_)
    
    return processed, processed.get_output()

def process_sequence(module, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The generator contains the output values of the module if it is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    while True:
        input_value = next(inputs)
        module, new_output = process(module, input_value)
        yield new_output
    
_SUM = Sum()
     
def sum_(input_):
    return _SUM.process(input_).get_output()