from itertools import chain
from modular.modules.base import Module, sum_input, process

class Delay(Module):
    """Gives the previous summed input, and initally Delay.INITIAL_VALUE"""
    INITIAL_VALUE = "Hello"
    
    def __init__(self, output = None, previous = None):
        """Creates a new  Delay instance with current and previous output.
        
        The default for output is None and for previous is Delay.INITIAL_VALUE.
        """
        super(Delay, self).__init__(output)
        self.__previous = previous if previous != None else Delay.INITIAL_VALUE

    def process(self, input_):
        """Returns a Delay instance that holds the previous summed input.
        
        The input_ must be a single string or a sequence of strings.
        
        The previous summed input is the summed input with which the process
        method was called that created the current instance, or the value
        specified at construction.
        
        """
        new_output = self.__previous
        current_input = sum_input(input_)
        
        return Delay(new_output, current_input)
    
class Echo(Module):
    """Concatenates the summed input with itself."""
    def __init__(self, output = None):
        """Initializes a new instance with the given output or None."""
        super(Echo, self).__init__(output)

    def process(self, input_):
        """Returns an Echo instance that holds the summed input concatenated with itself.

        The input_ must be a single string or a sequence of strings.
        
        """
        added_input_ = sum_input(input_)
        new_output = added_input_ + added_input_
        
        return Echo(new_output)
            
class Reverse(Module):
    """Reverses the summed input."""
    def __init__(self, output = None):
        """Initializes a new instance with the given output or None."""
        super(Reverse, self).__init__(output)

    def process(self, input_):
        """Returns a Reverse instance that holds the summed input reversed.

        The input_ must be a single string or a sequence of strings.
        
        """
        new_output = sum_input(input_)[::-1]
        
        return Reverse(new_output)
    
def process_sequence(module, input_sequence):
    """Returns an infinite generator of output strings for the given sequence of inputs.
    
    The input_sequence must be a single string, a sequence of strings or a
    sequence of sequences of strings.
    
    The generator contains the output values of the module that is consecutively feed
    with the elements from the input sequence followed by an infinte sequence of empty
    strings. None values in the output are converted to empty strings.
    
    """
    inputs = chain(input_sequence, iter(str, "infinite generator of empty strings"))
    while True:
        input_value = next(inputs)
        module, new_output = process(module, input_value)

        yield new_output if new_output else ""