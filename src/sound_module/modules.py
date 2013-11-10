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
    
    def __init__(self, value = None):
        """Creates a new instance with a given value or None."""
        self.__value = value
    
    def get_value(self):
        """Returns the current value of the Module"""
        return self.__value
    
    def process(self, input_):
        """Creates a instance of the class holding a new value calculated from the given input.
        
        Subclasses of Module must implement this method.
        
        """
        raise NotImplementedError

class Sum(Module):
    def __init__(self, value = None):
        super(Sum, self).__init__(value)
        
    def process(self, input_):
        """Returns a Sum instance with the concatenated input strings."""
        return Sum("".join(input_))

class Delay(Module):
    INITIAL_VALUE = "Hello"
    
    def __init__(self, value = None, previous = None):
        """Creates a new  Delay instance with current and previous value.
        
        The default value for value is None and for previous is Delay.INITIAL_VALUE.
        """
        super(Delay, self).__init__(value)
        self.__previous = previous if previous != None else Delay.INITIAL_VALUE



    def process(self, input_):
        """Returns a Delay instance that holds the summed previous input values.
        
        The previous input values are the values with which the process method was
        called that created the current instance, or the value specified at construction.
        
        """
        previous = self.__previous
        added_input = _sum(input_)
        
        return Delay(previous, added_input)
    
class Echo(Module):
    def __init__(self, value = None):
        super(Echo, self).__init__(value)

    def process(self, input_):
        """Returns an Echo instance with the summed input string concatenated with itself."""
        added_input_ = _sum(input_)
        new_value = added_input_ + added_input_
        
        return Echo(new_value)
            
class Reverse(Module):
    def __init__(self, value = None):
        super(Reverse, self).__init__(value)

    def process(self, input_):
        """Returns a Reverse instance with the summed input string reversed."""
        new_value = _sum(input_)[::-1]
        
        return Reverse(new_value)

def process(module, input_):
    """Returns the processed module and the new value resulting from the given input."""
    processed = module.process(input_)
    
    return processed, processed.get_value()

def process_sequence(module, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The generator contains the output values of the module if it is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    while True:
        input_value = next(inputs)
        module, new_value = process(module, input_value)
        yield new_value
    
__SUM = Sum()
     
def _sum(input_):
    return __SUM.process(input_).get_value()