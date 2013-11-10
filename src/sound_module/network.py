from sound_module.modules import Module, Delay, Echo, Sum, Reverse
from collections import OrderedDict
import logging

_log = logging.getLogger(__name__)



class NetworkFactory():
    """Specifies an ordered list of named Modules and directed connections between them.
    
    The NetworkFactory can be built by adding new modules with a unique name and
    specifing connections between already added modules by specifing their names.
    
    The order of the modules in the NetworkFactory is the order in which they
    where added. Connections can only be created from Module A to B if A < B,
    that is, if A was added before B. In particular circles are not permited.
    
    """
    __BASE_FACTORIES = {"delay": Delay.create,
                        "echo": Echo.create,
                        "noop": Sum.create,
                        "reverse": Reverse.create
                        }
    
    def __init__(self, modules = None, connections = None, factories = None):
        self.__modules = modules if modules else ()
        self.__connections = connections if connections else {}
        self.__factories = factories if factories else NetworkFactory.__BASE_FACTORIES.copy()
        
    def add_module(self, module_id, module_type):
        """Adds the given module_type with the given id to the NetworkFactory.
        
        If the NetworkFactory already contains a module_type with the given name, a
        ValueError is raised.
        """
        if module_type not in self.__factories:
            raise UndefinedValueError("{0} is not defined".format(module_type))
#            raise ValueError("There is no module type with name \"{0}\". Choose from: {1} ".format(module_type, self.__factories.keys())) 

        if module_id in self.__modules:
            raise NameConflictError("\"{0}\" is already defined".format(module_id))
#            raise ValueError("Module with name \"{0}\" is already defined".format(module_type.get_id())) 
        
        self.__modules = self.__modules + ((module_id, module_type), )
        
        _log.info("Added module with name %s", module_id)
        
    def add_connection(self, from_module, to_module):
        """Adds a connection from from_module to to_module to the NetworkFactory.
        
        If the NetworkFactory either of them was not yet added to the NetworkFactory
        or if the from_module was added after to_module to the NetworkFactory, a
        ValueError is raised.
        """
        available_modules_ids = self.available_modules_ids()
        if from_module not in available_modules_ids or to_module not in available_modules_ids:
            raise UndefinedValueError("{0} or {1} is not defined".format(from_module, to_module))
#            raise ValueError("""Modules must be added to before they can be connected: Tried to connect {0} to {1}. Available: {2}""".format(from_module, to_module, self._available_modules_ids()))
            
        if self.__module_order(from_module) > self.__module_order(to_module):
            raise IllegalOrderError("{0} was defined after {1}".format(from_module, to_module))
#            raise ValueError("""Modules can be only connected in the order of their definition: Tried to connect {0} to {1}. Available: {2}""".format(from_module, to_module, self.available_modules_ids()))
        
        if to_module in self.__connections:
            self.__connections[to_module] += (from_module, )
        else:
            self.__connections[to_module] = (from_module, )
        
        _log.info("Added connection from %s to %s", from_module, to_module)
            
    def __module_order(self, module_id):
        return self.available_modules_ids().index(module_id)
        
    def create(self):
        return self.__create(self.__modules, self.__connections, self.__factories)
    
    def __create(self, modules, connections, factories):
        modules_by_id = [(id_, self.__module_from_type(type_)) for id_, type_ in modules]
        
        return Network(modules_by_id, connections.copy())

    def __module_from_type(self, module_type):
        module_factory = self.__factories[module_type]
        
        return module_factory()
        
    def available_module_types(self):
        return self.__factories.viewkeys()
    
    def available_modules_ids(self):
        return [id_ for id_, type_ in self.__modules]
    
    def define_as_module(self, module_type):
        if module_type in self.__factories:
            raise NameConflictError("\"{0}\" is already defined".format(module_type))
#            raise ValueError("Module type with name \"{0}\" is already defined".format(module_type.get_id())) 
            
        factory = self.__create_network_factory(self.__modules, self.__connections, self.__factories)
        self.__factories[module_type] = factory
        self.__reset()
        
        _log.info("Created module type %s", module_type)
        
    def __create_network_factory(self, modules, connections):
        factories = {type_: factory for type_, factory in self.__factories if type_ in modules.values()}
        def factory():
            return self.__create(modules, connections, factories)
        
        return factory
    
    def __reset(self):
        self.__modules = OrderedDict()
        self.__connections = {}
    
class Network(Module):
    """Network is a composite module for string processing.
    
    The structure of a Network module is defined by a NetworkFactory, which
    specifies and ordered list of modules and input-output connections between
    them.
    
    The input strings to the Network are feed to the first module in the
    NetworkFactory one by one. A single input string is process by the modules in
    their given order. Thus connections that lead backward in the module order,
    and in particular circles, are not allowed in the NetworkFactory.
    
    The output of the Network for a single input string is the value of the
    last module in the NetworkFactory after processing. For multiple inputs the
    outputs are concatenated with a single separating whitespace character in
    between them. The number of words in the output string is limited to
    Network.OUTPUT_LENGHT times the number of strings in the input. If the
    Network contains no module, the output is the empty string. 
    
    """
    
    __SUM = Sum()
    
    def __init__(self, modules, connections, value = None):
        """Network instances should be created with a NetworkFactory."""
        super(Network, self).__init__(value)
        self.__modules = modules if modules else ()
        self.__connections = connections if connections else {}
    
    def process(self, input_):
        """Returns a new Network instance holding the processed summed input value."""
        if not self.__modules:
            return _EMPTY
        
        summed_input = self.__SUM.process(input_).get_value()
        processed_modules = self.__process_modules(summed_input)
        id_, last_module = processed_modules[-1]  # @UnusedVariable
        
        return Network(processed_modules, self.__connections, last_module.get_value())
    
    def __process_modules(self, input_):
        modules = self.__modules
        processed = OrderedDict()
        
        first_module_id, first_module = modules[0]
        processed[first_module_id] = first_module.process(input_)
        
        for module_id, module in modules[1:]:
            processed = self.__process_module(module_id, module, processed)
        
        return processed.items()
        
    def __process_module(self, module_id, module, processed):
        input_modules = self.__connections[module_id]
        input_values = (processed[input_id].get_value() for input_id in input_modules)
        
        processed[module_id] = module.process(input_values)
        
        return processed
    
class NameConflictError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    
class UndefinedValueError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    
class IllegalOrderError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

_EMPTY = Network(None, None, "")

