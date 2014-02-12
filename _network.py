"""Composite network channel from modules and connections."""
from functools import partial
from .channels import memoryless_channel

def network_channel(modules, connections):
    if not modules:
        return _empty_channel()

    started_modules = [module._start() for module in modules]
    process = partial(_process_modules, modules=started_modules, connections=connections)
    
    #The state of the network is confined in the started modules
    return memoryless_channel(process)
    
def _process_modules(input_, modules, connections):
    #Modules are procesed in the order of their definition. This is
    #guaranteed to work by the preconditions in the NetworkDefinition. 
    outputs = {}
    
    first_module_id, first_channel = modules[0].get_state()
    last_value = first_channel.send(input_)
    outputs[first_module_id] = last_value
    
    for module in modules[1:]:
        last_value = _process_module(module, outputs, connections)
        outputs[module.id] = last_value
    
    return last_value
    
def _process_module(module, outputs, connections):
    module_id, channel = module.get_state()

    input_modules = connections[module_id] if module_id in connections else () 
    input_values = (outputs[input_id] for input_id in input_modules)
    
    return channel.send(input_values)

def _empty_channel():
    empty = (None for _ in range(2))
    empty.next()

    #Returns None on the first call to send and terminates.
    return empty
