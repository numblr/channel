from sound_module.modules import Module
from collections import OrderedDict
import logging

_log = logging.getLogger(__name__)

class NetworkGraph():
    def __init__(self):
        self.__modules = OrderedDict()
        self.__connections = {}
        
    def add_module(self, module):
        module_id = module.get_id()
        if module_id in self.__modules:
            raise ValueError("Module with name %s is already defined", module.get_id()) 
        
        self.__modules[module_id] = module
        
        _log.info("Added module %s", module_id)
        
    def add_connection(self, from_module, to_module):
        if self.__module_order(from_module) > self.__module_order(to_module):
            raise ValueError("""Modules can be only connected in the order of their definition: 
                Tried to connect %s to %s""", from_module, to_module)
        
        if to_module in self.__connections:
            self.__connections[to_module] = self.__connections[to_module] + (from_module, )
        else:
            self.__connections[to_module] = (from_module, )
        
        _log.info("Added connection from %s to %s", from_module, to_module)
            
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
    def __init__(self, graph, value = None, module_id = None):
        super(Network, self).__init__(value, module_id)
        self.__graph = graph
    
    def process(self, inputs):
        modules = self.__graph.get_modules()
        if not modules:
            return ""
        
        result = self.__process_inputs(modules, inputs)

        return " ".join(result).strip()
    
    def __process_inputs(self, modules, inputs):
        result = []
        for input_value in inputs :
            modules = self.__process_single(modules, input_value)
            result.append(modules[-1].get_value())
        
        while result[-1] and len(result) < len(inputs) * 16:
            modules = self.__process_single(modules, "")
            result.append(modules[-1].get_value())
                          
        return result
    
    def __process_single(self, modules, input_value):
        input_module = modules[0]
        processed = OrderedDict()
        processed[input_module.get_id()] = input_module.process((input_value, ))
        for module in modules[1:]:
            inputs = self.__graph.get_inputs(module)
            input_values = [processed[i.get_id()].get_value() for i in inputs]
            processed[module.get_id()] = module.process(input_values)
        
        return processed.values()
    
    
    
    
    