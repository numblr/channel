from collections import OrderedDict
from modular.modules.base import Module, sum_input

class NetworkDefinition():
    """Specifies an ordered list of named Modules and directed connections between them.
    
    The NetworkDefinition can be built by adding new modules with a unique id and
    specifing connections between already added modules by specifing their ids.
    
    The order of the modules in the definition is the order in which they where
    added. Connections can only be created from Module A to B if A < B, that is,
    if A was added before B. In particular circular connections between the
    modules are not permited.
    
    """
    def __init__(self, module_types):
        """Initializes a new instance with an iterable of allowed module types."""
        self.__modules = ()
        self.__connections = {}
        self.__module_types = tuple(module_types)

    def available_module_ids(self):
        """Returns the ids of the modules defined in the current instance."""
        return [id_ for id_, _ in self.__modules]
        
    def add_module(self, module_id, module_type):
        """Adds the given module_type with the given module_id to the definition.
        
        If the current instance already contains a module with the given
        module_id, a NameConflictError is raised. If the current instance does
        not accept the specified module_type, an UndefinedNameError is raised.
        
        """
        if module_type not in self.__module_types:
            raise UndefinedNameError("\"{0}\" is not defined".format(module_type))

        if module_id in self.available_module_ids():
            raise NameConflictError("\"{0}\" is already defined".format(module_id))
        
        self.__modules = self.__modules + ((module_id, module_type), )
        
    def add_connection(self, from_module, to_module):
        """Adds a connection from from_module to to_module to the current instance.
        
        If one of the given id's was not yet defined in the current instance,
        a UndefinedNameError is raised. If the from_module was added after
        to_module to the current instance, an IllegalOrderError is raised. If
        the connection is already present, a NameConflictError is raised.
        
        """
        available_modules_ids = self.available_module_ids()
        if from_module not in available_modules_ids or to_module not in available_modules_ids:
            raise UndefinedNameError("\"{0}\" or \"{1}\" is not defined".format(from_module, to_module))
            
        if self.__module_order(from_module) > self.__module_order(to_module):
            raise IllegalOrderError("\"{0}\" must have been defined before \"{1}\"".format(from_module, to_module))
        
        if to_module in self.__connections and from_module in self.__connections[to_module]:
            raise NameConflictError("\"{0}\" is already connected to \"{1}\"".format(from_module, to_module)) 
        
        if to_module not in self.__connections:
            self.__connections[to_module] = ()
            
        self.__connections[to_module] += (from_module, )
            
    def __module_order(self, module_id):
        return self.available_module_ids().index(module_id)
        
    def _get_state(self):
        return self.__modules, self.__connections.copy()
    
class NetworkFactory():
    """Creates Network instances from a NetworkDefinition.
    
    New compound module types can be defined from a NetworkDefinition.
        
    """
    def __init__(self, factories):
        """Initializes a new instance with the given factories.
        
        factories must privide a mapping from a module type to a factory
        function for the corresponding Module instances.
        
        """
        self.__factories = factories.copy()
        
    def available_module_types(self):
        """Returns a list of the available module type identifiers."""
        return self.__factories.keys()
        
    def create(self, network_definition):
        """Returns a new Network instance based on the given NetworkDefinition.
        
        If the specified network_definition contains module types that are not
        accepted by the current instance, a KeyError is raised.
        
        """
        modules, connections = network_definition._get_state()

        return self.__create(modules, connections, self.__factories)
    
    def __create(self, modules, connections, factories):
        modules_instances = [(id_, self.__factories[type_]()) for id_, type_ in modules]
        
        return Network(modules_instances, connections)

    def define_module_type(self, module_type, network_definition):
        """Adds support for Network modules based on the given definition to the current instance.
        
        After defining a module type, the create method on the current instance
        accepts network definitions containing the specified module_type
        identifier. For these entries a Network module based on
        network_definition will be created in the resulting Network.
        
        If there is already a module type with the given identifier, a
        NameConflictError is raised. If the specified network_definition
        contains module types that are not accepted by the current instance,
        a KeyError is raised.

        """
        if module_type in self.__factories:
            raise NameConflictError("\"{0}\" is already defined".format(module_type))
            
        self.__factories[module_type] = self.__create_network_factory(network_definition)
        
    def __create_network_factory(self, network_definition):
        modules, connections = network_definition._get_state()
        if not all(type_ in self.__factories.keys() for _, type_ in modules):
            raise KeyError("Definition contains unsuppoted module types")
        
        def factory():
            return self.__create(modules, connections, self.__factories)
        
        return factory
    
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
        modules in the Network, according to the specified connections. If the
        Network contains no module, the output is the empty string. 
        
        """
        if not self.__modules:
            return _EMPTY
        
        processed_modules = self.__process_modules(sum_input(input_))
        _, last_module = processed_modules[-1]
        
        return Network(processed_modules, self.__connections, last_module.get_output())
    
    def __process_modules(self, input_):
        modules = self.__modules
        processed = OrderedDict()
        
        first_module_id, first_module = modules[0]
        processed[first_module_id] = first_module.process(input_)
        
        for module_id, module in modules[1:]:
            processed = self.__process_module(module_id, module, processed)
        
        return processed.items()
        
    def __process_module(self, module_id, module, processed):
        connections = self.__connections
        input_modules = connections[module_id] if module_id in connections else () 
        input_values = (processed[input_id].get_output() for input_id in input_modules)
        
        processed[module_id] = module.process(input_values)
        
        return processed

_EMPTY = Network(None, None, "")
    
class NameConflictError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
class UndefinedNameError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
    
class IllegalOrderError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)