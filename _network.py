from collections import OrderedDict
from functools import partial
from modular.channels._channels import memoryless_channel

def network_channel(modules, connections):
    if not modules:
        empty = (None for _ in range(2))
        empty.next()
        
        return empty

    started_modules = [module._start() for module in modules]
    process = partial(_process_modules, modules=started_modules, connections=connections)
    
    return memoryless_channel(process)
    
def _process_modules(input_, modules, connections):
    #Modules are outputs in the order of their definition. This is
    #guaranteed to work by the conditions in the NetworkDefinition. 
    #The algorithm could be improved by depth-first search like processing. 
    outputs = OrderedDict()
    
    first_module_id, first_channel = modules[0].get_state()
    outputs[first_module_id] = first_channel.send(input_)
    
    for module in modules[1:]:
        outputs = _process_module(module, outputs, connections)
    
    return outputs.values()[-1]
    
def _process_module(module, outputs, connections):
    module_id, channel = module.get_state()

    input_modules = connections[module_id] if module_id in connections else () 
    input_values = (outputs[input_id] for input_id in input_modules)
    
    outputs[module_id] = channel.send(input_values)
    
    return outputs