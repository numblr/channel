from sound_module.modules import Sum, Delay, Echo, Reverse
from sound_module.network import NetworkGraph, Network
        
EXIT = ()

def _module(state, *args):
    if len(args) != 2:
        raise ValueError("Module definition requires a name and a module type, was {0}.\nChoose from: {1}".format(args, state.get_factories().keys()))
    
    state.add_module(*args)
    
    return 0

def _connect(state, *args):
    if len(args) != 2:
        raise ValueError("Connection definition requires two module names, was {0}.\nDefined modules: ".format(args, state.get_network().get_modules().keys()))
    
    state.add_connection(*args)

    return 0

def _process(state, *args):
    print(Network(state.get_network()).process(args).get_value())

    return 0
    
def _define(state, *args):
    if len(args) != 1:
        raise ValueError("Module type definition \"{0}\"requires a valid type name.\nChoose from: {1}".format(args, state.get_factories().keys()))
    
    state.add_factory(args[0], _create_network_factory(state.get_network()))
    state.reset()

    return 0

def _exit(state, *args):
    return EXIT

def _create_network_factory(graph):
    def factory():
        return Network(graph)
        
    return factory
    
        
class Interpreter(object):
    __COMMANDS = {"module": _module,
                 "connect": _connect,
                 "process": _process,
                 "define": _define,
                 "exit": _exit
                }
    
    def __init__(self, state = None):
        self.__state = state if state else InterpreterState()
        
    def parse(self, line):
        input_strings = line.split()
        
        command =  input_strings[0]
        if not command in Interpreter.__COMMANDS:
            raise ValueError("There is no command with name: \"{0}\".\nChoose from: {1}".format(command, Interpreter.__COMMANDS.keys()))
        
        
        return Interpreter.__COMMANDS[command](self.__state, *input_strings[1:])
        
class InterpreterState():
    __BASE_FACTORIES = {"delay": Delay.create,
                      "echo": Echo.create,
                      "noop": Sum.create,
                      "reverse": Reverse.create
                      }
    
    def __init__(self, factories = None):
        self._factories = factories if factories else InterpreterState.__BASE_FACTORIES.copy()
        self._network = NetworkGraph()
        
    def reset(self):
        self._network = NetworkGraph()
        
    def add_module(self, module_id, module_type):
        module = self._factories[module_type]()
        self._network.add_module(module_id, module)
        
    def add_connection(self, from_module, to_module):
        self._network.add_connection(from_module, to_module)
        
    def add_factory(self, module_type, factory):
        self._factories[module_type] = factory
        
    def get_network(self):
        return self._network
        
    def get_factories(self):
        return self._factories