from sound_module.streams import Reverse, Delay, Module
from collections import OrderedDict
    
class NetworkGraph():
    def __init__(self):
        self.__modules = OrderedDict()
        self.__connections = {}
        
    def add_module(self, module):
        module_id = module.get_id()
        if module_id in self.__modules:
            raise ValueError("Module with name %s is already defined", module.get_id()) 
        self.__modules[module_id] = module
        
    def add_connection(self, from_module, to_module):
        if self.__module_order(from_module) > self.__module_order(to_module):
            raise ValueError("""Modules can be only connected in the order of their definition: 
                Tried to connect %s to %s""", from_module, to_module)
        if to_module in self.__connections:
            self.__connections[to_module] = self.__connections[to_module] + (from_module, )
        else:
            self.__connections[to_module] = (from_module, )
            
    def get_inputs(self, module):
        if not module.get_id() in self.__connections:
            return tuple()
        
        return [self.get_module(m_id) for m_id in self.__connections[module.get_id()]]
        
    def get_module(self, module_id):
        return self.__modules[module_id]
    
    def get_modules(self):
        return self.__modules.values()
    
    def __module_order(self, module_id):
        return self.__modules.keys().index(module_id)
    
class Network(Module):
    def __init__(self, graph):
        self.__graph = graph
    
    def process(self, inputs):
        result = [self.__process_single(inp) for inp in inputs]

        while result[-1] and len(result) < len(inputs) * 16:
            result.append(self.__process_single(""))
                          
        return " ".join(result).strip()
    
    def __process_single(self, input_value):
        modules = self.__graph.get_modules()
        outputs = self.__calculate_outputs(modules, input_value)
        output_module = modules[-1].get_id()
        
        return outputs[output_module]
        
    def __calculate_outputs(self, modules, input_value):
        input_module = modules[0]
        values = {input_module.get_id(): input_module.process((input_value, ))}
        for module in modules[1:]:
            inputs = self.__graph.get_inputs(module)
            input_values = [values[i.get_id()] for i in inputs]
            values[module.get_id()] = module.process(input_values)
            
        return values
        
if __name__ == "__main__":
    inputs = ("Hello", "World")
    net = NetworkGraph()
    net.add_module(Reverse("A"))
    net.add_module(Delay("B"))
    net.add_connection("A", "B")
    
    print(Network(net).process(inputs))
