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
    
    def process(self, inputs):
        """Creates a new instance of the class holding a new value calculated from the given inputs.
        
        Subclasses of Module must implement this method.
        
        """
        raise NotImplementedError

class Sum(Module):
    def __init__(self, value = None):
        super(Sum, self).__init__(value)
        
    def process(self, inputs):
        """Returns a new Sum instance with the concatenated input strings."""
        return Sum("".join(inputs))

class Delay(Module):
    __INITIAL_VALUE = "Hello"
    
    def __init__(self, value = None, previous = None):
        """Creates a new Delay instance with current and previous value.
        
        The default value for value is None and for previous is Delay.__INITIAL_VALUE.
        """
        super(Delay, self).__init__(value)
        self.__previous = previous if previous != None else Delay.__INITIAL_VALUE



    def process(self, inputs):
        """Returns a new Delay instance that holds the summed previous input values.
        
        The previous input values are the values with which the process method was
        called that created the current instance, or the value specified at construction.
        
        """
        previous = self.__previous
        added_input = _sum(inputs)
        
        return Delay(previous, added_input)
    
class Echo(Module):
    def __init__(self, value = None):
        super(Echo, self).__init__(value)

    def process(self, inputs):
        """Returns a new Echo instance with the summed input string concatenated with itself."""
        added_inputs = _sum(inputs)
        new_value = added_inputs + added_inputs
        
        return Echo(new_value)
            
class Reverse(Module):
    def __init__(self, value = None):
        super(Reverse, self).__init__(value)

    def process(self, inputs):
        """Returns a new Reverse instance with the summed input string reversed."""
        new_value = _sum(inputs)[::-1]
        
        return Reverse(new_value)
    
__SUM = Sum()
     
def _sum(self, inputs):
    return __SUM.process(inputs).get_value()