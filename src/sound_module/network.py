from sound_module.modules import Module
from collections import OrderedDict
import logging

_log = logging.getLogger(__name__)

class NetworkGraph():
    """Specifies an ordered list of named Modules and directed connections between them.
    
    The NetworkGraph can be built by adding new modules with a unique name and
    specifing connections between already added modules by specifing their names.
    
    The order of the modules in the NetworkGraph is the order in which they
    where added. Connections can only be created from Module A to B if A < B,
    that is, if A was added before B. In particular circles are not permited.
    
    """
    def __init__(self, module = None, connections = None):
        self.__modules = module if module else OrderedDict()
        self.__connections = connections if connections else {}
        
    def add_module(self, module_id, module):
        """Adds the given module with the given id to the NetworkGraph.
        
        If the NetworkGraph already contains a module with the given name, a
        ValueError is raised.
        """
        if module_id in self.__modules:
            raise ValueError("Module with name \"{0}\" is already defined".format(module.get_id())) 
        
        self.__modules[module_id] = module
        
        _log.info("Added module %s", module_id)
        
    def add_connection(self, from_module, to_module):
        """Adds a connection from from_module to to_module to the NetworkGraph.
        
        If the NetworkGraph either of them was not yet added to the NetworkGraph
        or if the from_module was added after to_module to the NetworkGraph, a
        ValueError is raised.
        """
        if not from_module in self.__modules or not to_module in self.__modules:
            raise ValueError("""Modules must be added to before they can be connected: Tried to connect {0} to {1}. Available: {2}""".format(from_module, to_module, self.get_modules().keys()))
            
        if self.__module_order(from_module) > self.__module_order(to_module):
            raise ValueError("""Modules can be only connected in the order of their definition: Tried to connect {0} to {1}. Available: {2}""".format(from_module, to_module, self.get_modules().keys()))
        
        if to_module in self.__connections:
            self.__connections[to_module] = self.__connections[to_module] + (from_module, )
        else:
            self.__connections[to_module] = (from_module, )
        
        _log.info("Added connection from %s to %s", from_module, to_module)
            
    def get_input_modules(self, module_id):
        """Returns the names of the modules that act as input to the module with the given module_id"""
        if not module_id in self.__connections:
            return ()
        
        return self.__connections[module_id]
        
    def get_module(self, module_id):
        """Returns the module that was added with the given module_id"""
        return self.__modules[module_id]
    
    def get_modules(self):
        """Returns a copy of the ordered dictionary containing the modules by their names."""
        return self.__modules.copy()
    
    def copy(self):
        return NetworkGraph(self.__modules.copy(), self.__connections.copy())
    
    def __module_order(self, module_id):
        return self.__modules.keys().index(module_id)
    
class Network(Module):
    """Network is a composite module for string processing.
    
    The structure of a Network module is defined by a NetworkGraph, which
    specifies and ordered list of modules and input-output connections between
    them.
    
    The input strings to the Network are feed to the first module in the
    NetworkGraph one by one. A single input string is process by the modules in
    their given order. Thus connections that lead backward in the module order,
    and in particular circles, are not allowed in the NetworkGraph.
    
    The output of the Network for a single input string is the value of the
    last module in the NetworkGraph after processing. For multiple inputs the
    outputs are concatenated with a single separating whitespace character in
    between them. The number of words in the output string is limited to
    Network.OUTPUT_LENGHT times the number of strings in the input. If the
    Network contains no module, the output is the empty string. 
    
    """

    OUTPUT_LENGHT = 16

    def __init__(self, graph, value = None):
        """Creates a new Network instance based on the specified NetworkGraph and value."""
        super(Network, self).__init__(value)
        self.__graph = graph.copy()
    
    def process(self, inputs):
        """Returns a new Network instance holding the processed input value."""
        return Network(self.__graph, self.__calculate_new_value(inputs))
    
    def __calculate_new_value(self, inputs):
        modules = self.__graph.get_modules()
        if not modules:
            return ""
        
        result = self.__process_inputs(modules, inputs)

        return " ".join(result).strip()
    
    def __process_inputs(self, modules, inputs):
        result = []
        for input_value in inputs :
            modules = self.__process_single(modules, input_value)
            last_module = modules.values()[-1]
            result.append(last_module.get_value())
        
        while result[-1] and len(result) < len(inputs) * Network.OUTPUT_LENGHT:
            modules = self.__process_single(modules, "")
            last_module = modules.values()[-1]
            result.append(last_module.get_value())
                          
        return result
    
    def __process_single(self, modules, input_value):
        first_module = modules.keys()[0]
        modules[first_module] = modules[first_module].process((input_value, ))
        for module in modules.keys()[1:]:
            input_modules = self.__graph.get_input_modules(module)
            input_values = [modules[input_id].get_value() for input_id in input_modules]
            modules[module] = modules[module].process(input_values)
        
        return modules