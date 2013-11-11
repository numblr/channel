from modular.modules.base import Module, sum_

class Delay(Module):
    INITIAL_VALUE = "Hello"
    
    def __init__(self, output = None, previous = None):
        """Creates a new  Delay instance with current and previous output.
        
        The default output for output is None and for previous is Delay.INITIAL_VALUE.
        """
        super(Delay, self).__init__(output)
        self.__previous = previous if previous != None else Delay.INITIAL_VALUE



    def process(self, input_):
        """Returns a Delay instance that holds the summed new_output input values.
        
        The new_output input values are the values with which the process method was
        called that created the current instance, or the value specified at construction.
        
        """
        new_output = self.__previous
        current_input = sum_(input_)
        
        return Delay(new_output, current_input)
    
class Echo(Module):
    def __init__(self, output = None):
        super(Echo, self).__init__(output)

    def process(self, input_):
        """Returns an Echo instance with the summed input string concatenated with itself."""
        added_input_ = sum_(input_)
        new_output = added_input_ + added_input_
        
        return Echo(new_output)
            
class Reverse(Module):
    def __init__(self, output = None):
        super(Reverse, self).__init__(output)

    def process(self, input_):
        """Returns a Reverse instance with the summed input string reversed."""
        new_output = sum_(input_)[::-1]
        
        return Reverse(new_output)