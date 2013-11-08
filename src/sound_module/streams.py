class Operation(object):
    def process(self, inputs):
        raise NotImplementedError

class Input(Operation):
    def __init__(self, values):
        self.__values = values
        self.__count = 0
    
    def process(self, inputs):
        if self.__count < len(self.__values):
            value = self.__values[self.__count]
            self.__count += 1
            
            return value
        
        return ""
    
class Adder(Operation):
    def process(self, inputs):
        return "".join(inputs)

class Delay(Operation):
    def __init__(self):
        self.__previous = "Hello"

    def process(self, inputs):
        previous = self.__previous
        self.__previous = Adder().process(inputs)
        
        return previous
    
class Echo(Operation):
    def process(self, inputs):
        added_inputs = Adder().process(inputs)
        
        return added_inputs + added_inputs
            
class Reverse(Operation):
    def process(self, inputs):
        return Adder().process(inputs)[::-1]
        
class Noop(Operation):
    def process(self, inputs):
        return Adder().process(inputs)