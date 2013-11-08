from sound_module.streams import Reverse, Delay, Operation, Input
    
class Network(Operation):
    def __init__(self, array_input):
        self.__modules = {"#INPUT": Input(array_input)}
        self.__module_order = ("#INPUT", )
        self.__connections = {}
        self.__output = array_input
        self.__first = True
        
    def add_module(self, module_id, module):
        self.__modules[module_id] = module
        self.__module_order = self.__module_order + (module_id, )
        self.__output = module_id
        if self.__first:
            self.__first = False
            self.add_connection("#INPUT", module_id)
        
    def add_connection(self, module_out_id, module_in_id):
        if self.__module_order.index(module_out_id) > self.__module_order.index(module_in_id):
            raise ValueError("""Modules can be only connected in the order of their definition: 
                Tried to connect %s to %s""", module_out_id, module_in_id)
        if module_in_id in self.__connections:
            self.__connections[module_in_id] = self.__connections[module_in_id] + (module_out_id, )
        else:
            self.__connections[module_in_id] = (module_out_id, )
        
    def process(self):
        out = None
        count = 0
        while out != "" and count < 16:
            out = self.__fetch(self.__output)
            yield out
        
    def __fetch(self, module):
        inputs = self.__connections[module] if module in self.__connections else tuple() 

        return self.__modules[module].process(map(self.__fetch, inputs))
        
if __name__ == "__main__":
    inputs = ("Hello", "World")
    net = Network(inputs)
    net.add_module("A", Reverse())
    net.add_module("B", Delay())
    net.add_connection("A", "B")
    
    print(list(net.process()))
