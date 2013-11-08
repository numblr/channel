from sound_module.modules import Sum, Delay, Echo, Reverse
from sound_module.network import NetworkGraph, Network
        
EXIT = ()
        
class ModuleFactory(object):
    def __init__(self, factory):
        self.__factory = factory
        
    def create(self):
        return self.__factory()
    
class NetworkFactory(ModuleFactory):
    @classmethod
    def from_graph(cls, graph):
        def factory():
            return Network(graph)
        
        return cls(factory)
        
    def __init__(self, factory):
        super(NetworkFactory, self).__init__(factory)
        
class ModuleOp():
    def apply(self, interpreter, *args):
        if len(args) != 2:
            raise ValueError("Module definition requires a name and a module type, was {0}.\nChoose from: {1}".format(args, interpreter._factories.keys()))
        
        module_id, module_type = args
        module = interpreter._factories[module_type].create()
        interpreter._network.add_module(module_id, module)
        
        return 0

class ConnectOp():
    def apply(self, interpreter, *args):
        if len(args) != 2:
            raise ValueError("Connection definition requires two module names, was {0}.\nDefined modules: ".format(args, interpreter._network.get_modules().keys()))
        
        from_module, to_module = args
        interpreter._network.add_connection(from_module, to_module)

        return 0

class ProcessOp():
    def apply(self, interpreter, *args):
        print(Network(interpreter._network).process(args).get_value())

        return 0
        
class DefineOp():
    def apply(self, interpreter, *args):
        if len(args) != 1:
            raise ValueError("Module type definition \"{0}\"requires a valid type name.\nChoose from: {1}".format(args, interpreter._factories.keys()))
        
        interpreter._factories[args[0]] = NetworkFactory.from_graph(interpreter._network)
        interpreter._network = NetworkGraph()

        return 0
    
class ExitOp():
    def apply(self, interpreter, *args):
        return EXIT
    
class Interpreter(object):
    __COMMANDS = {"module": ModuleOp(),
                 "connect": ConnectOp(),
                 "process": ProcessOp(),
                 "define": DefineOp(),
                 "exit": ExitOp()
                }
    
    __BASE_FACTORIES = {"delay": ModuleFactory(Delay.create),
                      "echo": ModuleFactory(Echo.create),
                      "noop": ModuleFactory(Sum.create),
                      "reverse": ModuleFactory(Reverse.create)
                      }
    
    def __init__(self, factories = None):
        self._factories = factories if factories else Interpreter.__BASE_FACTORIES.copy()
        self._network = NetworkGraph()
        
    def parse(self, line):
        input_strings = line.split()
        
        key_word =  input_strings[0]
        if not key_word in Interpreter.__COMMANDS:
            raise ValueError("There is no command with name: \"{0}\".\nChoose from: {1}".format(key_word, Interpreter.__COMMANDS.keys()))
        
        command = Interpreter.__COMMANDS[key_word]
        
        return command.apply(self, *input_strings[1:])