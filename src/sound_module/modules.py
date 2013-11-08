class Module(object):
    @classmethod
    def from_id(cls, module_id):
        return cls(module_id = module_id)
    
    def __init__(self, value, module_id):
        self.__value = value
        self.__id = module_id
    
    def get_value(self):
        return self.__value
    
    def get_id(self):
        return self.__id
    
    def process(self, inputs):
        raise NotImplementedError

class Adder(Module):
    def __init__(self, value = None, module_id = None):
        super(Adder, self).__init__(value, module_id)
        
    def process(self, inputs):
        new_value = "".join(inputs)
        
        return Adder(new_value, self.get_id())

class Delay(Module):
    __INITIAL_VALUE = "Hello"
    
    def __init__(self, value = None, previous = None, module_id = None):
        super(Delay, self).__init__(value, module_id)
        self.__previous = previous if previous != None else Delay.__INITIAL_VALUE

    def process(self, inputs):
        previous = self.__previous
        added_input = Adder().process(inputs).get_value()
        
        return Delay(previous, added_input, self.get_id())
    
class Echo(Module):
    def __init__(self, value = None, module_id = None):
        super(Echo, self).__init__(value, module_id)

    def process(self, inputs):
        added_inputs = Adder().process(inputs).get_value()
        new_value = added_inputs + added_inputs
        
        return Echo(new_value, self.get_id())
            
class Reverse(Module):
    def __init__(self, value = None, module_id = None):
        super(Reverse, self).__init__(value, module_id)

    def process(self, inputs):
        new_value = Adder().process(inputs).get_value()[::-1]
        
        return Reverse(new_value, self.get_id())