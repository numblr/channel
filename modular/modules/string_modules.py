from modular.modules.base import Module, sum_

class Delay(Module):
    """Output is the previous input value, and initally Delay.INITIAL_VALUE"""
    INITIAL_VALUE = "Hello"
    
    def __init__(self, output = None, previous = None):
        """Creates a new  Delay instance with current and previous output.
        
        The default for output is None and for previous is Delay.INITIAL_VALUE.
        """
        super(Delay, self).__init__(output)
        self.__previous = previous if previous != None else Delay.INITIAL_VALUE

    def process(self, input_):
        """Returns a Delay instance that holds the previous summed input.
        
        The previous summed input is the summed input with which the process
        method was called that created the current instance, or the value
        specified at construction.
        
        """
        new_output = self.__previous
        current_input = sum_(input_)
        
        return Delay(new_output, current_input)
    
class Echo(Module):
    """Output is the input value concatenated with itself."""
    def __init__(self, output = None):
        """Initializes a new instance with the given output or None."""
        super(Echo, self).__init__(output)

    def process(self, input_):
        """Returns an Echo instance that holds the summed input concatenated with itself."""
        added_input_ = sum_(input_)
        new_output = added_input_ + added_input_
        
        return Echo(new_output)
            
class Reverse(Module):
    """Output is the input value reversed."""
    def __init__(self, output = None):
        """Initializes a new instance with the given output or None."""
        super(Reverse, self).__init__(output)

    def process(self, input_):
        """Returns a Reverse instance that holds the summed input reversed."""
        new_output = sum_(input_)[::-1]
        
        return Reverse(new_output)