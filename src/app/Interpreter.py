from sound_module.modules import Adder, Delay, Echo, Reverse
from sound_module.network import NetworkGraph, Network
        
class ModuleFactory(object):
    def __init__(self, factory):
        self.__factory = factory
        
    def create(self, module_id):
        return self.__factory(module_id)
    
class NetworkFactory(ModuleFactory):
    @classmethod
    def from_graph(cls, graph):
        def factory(module_id):
            return Network(graph, module_id)
        
        return cls(factory)
        
    def __init__(self, factory):
        super(NetworkFactory, self).__init__(factory)
        
class Operator(object):
    def apply(self, *args):
        raise NotImplementedError

class ModuleOp(Operator):
    def apply(self, interpreter, *args):
        if len(args) != 2:
            raise ValueError("Module definition requires a name and a module type: %s", args)
        
        module_name, module_id = args
        module = interpreter._factories[module_name].create(module_id)
        interpreter._network.add_module(module)

class ConnectOp(Operator):
    def apply(self, interpreter, *args):
        if len(args) != 2:
            raise ValueError("Connection definition requires two module names: %s", args)
        
        from_module, to_module = args
        interpreter._network.add_connection(from_module, to_module)

class ProcessOp(Operator):
    def apply(self, interpreter, *args):
        print(Network(interpreter._network).process(args))
        
class DefineOp(Operator):
    def apply(self, interpreter, *args):
        if len(args) != 1:
            raise ValueError("Module type definition requires a type name: %s", args)
        
        interpreter._factories[args[0]] = NetworkFactory.from_graph(interpreter._network)
        interpreter._network = NetworkGraph()
    
class Interpreter(object):
    KEY_WORDS = {"module": ModuleOp(),
                 "connect": ConnectOp(),
                 "process": ProcessOp(),
                 "define": DefineOp()
                }
    
    BASE_FACTORIES = {"delay": ModuleFactory(Delay.from_id),
                      "echo": ModuleFactory(Echo.from_id),
                      "noop": ModuleFactory(Adder.from_id),
                      "reverse": ModuleFactory(Reverse.from_id)
                      }
    
    def __init__(self, factories = None):
        self._factories = factories if factories else Interpreter.BASE_FACTORIES.copy()
        self._network = NetworkGraph()
        
    def parse(self, line):
        words = line.split()
        operator = Interpreter.KEY_WORDS[words[0]]
        operator.apply(self, *words[1:])
