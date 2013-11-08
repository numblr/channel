class Module(object):
    @classmethod
    def from_id(cls, module_id):
        return cls(module_id)
    
    def __init__(self, module_id):
        self.__id = module_id
    
    def get_id(self):
        return self.__id
    
    def process(self, inputs):
        raise NotImplementedError

class Adder(Module):
    def __init__(self, module_id = None):
        super(Adder, self).__init__(module_id)
        
    def process(self, inputs):
        return "".join(inputs)

class Delay(Module):
    def __init__(self, module_id):
        super(Delay, self).__init__(module_id)
        self.__previous = "Hello"

    def process(self, inputs):
        previous = self.__previous
        self.__previous = Adder().process(inputs)
        
        return previous
    
class Echo(Module):
    def __init__(self, module_id):
        super(Echo, self).__init__(module_id)

    def process(self, inputs):
        added_inputs = Adder().process(inputs)
        
        return added_inputs + added_inputs
            
class Reverse(Module):
    def __init__(self, module_id):
        super(Reverse, self).__init__(module_id)

    def process(self, inputs):
        return Adder().process(inputs)[::-1]