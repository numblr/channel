"""Input processing by a network of named modules.

Each module has a channel that executes a simple task on its input. The inputs
of a module can be connected to outputs of other modules.

The channel in a module is a generator function that creates an initalized
generator. Processing of input is done by sending the input to the generator
using its send method:

>>> initialized_channel = channel()
>>> output = initialized_channel.send(input)

The generator is imediatelly initialized, that is, the first call to the
generator should already contain the first input value, not None.

A network is a channel itself and can be created from a NetworkFactory.
The building blocks of the network are channels available to the NetworkFactory
instance. New channels types can be created in the NetworkFactory instance
based on a NetworkDefinition. 

Classes:

NetworkDefinition -- Definition of the structure of the network based on identifiers
NetworkFactory -- Creation of network channels and new module type definition from a network definition

"""
from functools import partial
from modular.channels._network import network_channel
from modular.channels._module import Module

class NetworkDefinition():
    """Specifies an ordered list of named modules and directed connections between them.
    
    The NetworkDefinition can be edited by adding new modules with a unique id
    and specifing connections between already added modules by via their ids.
    
    The order of the modules in the definition is the order in which they where
    added. Connections can only be created from Module A to B if A < B, that is,
    if A was added before B. In particular circular connections between the
    modules are not permited.
    
    """
    def __init__(self, module_types):
        """Initializes a new instance from an iterable of allowed module types."""
        self.__modules = ()
        self.__connections = {}
        self.__module_types = tuple(module_types)

    def available_module_ids(self):
        """Returns a list with the ids of the modules defined in the current instance."""
        return [module.id for module in self.__modules]

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
        
        self.__modules = self.__modules + (Module(module_id, module_type), )
        
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
    """Creates network channels from a NetworkDefinition.
    
    New compound module types can be defined from a NetworkDefinition.
        
    """
    def __init__(self, channels):
        """Initializes a new instance with the given channels.
        
        channels must privide a mapping from a module type to a factories
        function for the corresponding Module instances.
        
        """
        self.__channels = channels.copy()
        
    def available_module_types(self):
        """Returns a list of the available module type identifiers."""
        return self.__channels.keys()
        
    #this creates a an generator function
    def create(self, network_definition):
        """Returns a new Network instance based on the given NetworkDefinition.
        
        If the specified network_definition contains module types that are not
        accepted by the current instance, a KeyError is raised.
        
        """
        modules, connections = network_definition._get_state()

        return self.__create(modules, connections, self.__channels)
    
    def __create(self, modules, connections, channels):
        channels = self.__channels
        modules_instances = [Module(module.id, channels[module.channel]) for module in modules]
        
        return partial(network_channel, modules_instances, connections)

    def define_module_type(self, module_type, network_definition):
        """Adds support for Network modules based on the given definition to the current instance.
        
        After defining a module type, the create method on the current instance
        accepts network_channel definitions containing the specified module_type
        identifier. For these entries a Network module based on
        network_definition will be created in the resulting Network.
        
        If there is already a module type with the given identifier, a
        NameConflictError is raised. If the specified network_definition
        contains module types that are not accepted by the current instance,
        a KeyError is raised.

        """
        if module_type in self.__channels:
            raise NameConflictError("\"{0}\" is already defined".format(module_type))
            
        self.__channels[module_type] = self.__create_network_channel(network_definition)
        
    #this creates a an generator function
    def __create_network_channel(self, network_definition):
        modules, connections = network_definition._get_state()
        if not all(module.channel in self.__channels.keys() for module in modules):
            raise KeyError("Definition contains unsupported module types")
        
        return self.__create(modules, connections, self.__channels)

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