from collections import OrderedDict
from modular.modules.base import Module, sum_input

class Network(Module):
    """Network is a composite module based on a NetworkDefinition.
    
    The structure of a Network module is defined by a NetworkDefinition, which
    specifies and ordered list of modules and input-output connections between
    them.
    
    The order of processing of the modules in the Network is according to the
    topologial ordering implied by the input-output connections between them.  
    
    """
    def __init__(self, modules, connections, output = None):
        """Network instances should be created from a NetworkFactory."""
        super(Network, self).__init__(output)
        self.__modules = modules
        self.__connections = connections
    
    def process(self, input_):
        """Returns a new Network instance holding the processed summed input value.

        The input to is feed to the first module in the Network.
        
        The output held by the returned Network instance is the output value of
        the last module in the Network after processing the input by all
        modules in the Network, even if it is not connected from the input
        module. Modules are processed in their topolocial order according to the
        specified connections. If the Network contains no module, the output is
        None. 
        
        """
        if not self.__modules:
            return _EMPTY
        
        processed_modules = self.__process_modules(sum_input(input_))
        _, last_module = processed_modules[-1]
        
        return Network(processed_modules, self.__connections, last_module.get_output())
    
    def __process_modules(self, input_):
        #Modules are processed in the order of their definition. This is
        #guaranteed to work by the conditions in the NetworkDefinition. 
        #The algorithm could be improved by depth-first search like processing. 
        modules = self.__modules
        processed = OrderedDict()
        
        first_module_id, first_module = modules[0]
        processed[first_module_id] = first_module.process(input_)
        
        for module_id, module in modules[1:]:
            processed = self.__process_module(module_id, module, processed)
        
        return processed.items()
        
    def __process_module(self, module_id, module, outputs):
        connections = self.__connections
        input_modules = connections[module_id] if module_id in connections else () 
        input_values = (outputs[input_id].get_output() for input_id in input_modules)
        
        outputs[module_id] = module.process(input_values)
        
        return outputs

_EMPTY = Network(None, None, None)