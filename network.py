"""Input processing by a network of named modules.

Allows definition and creation of networks of processing units (modules). Each
module has a channel that executes a simple task on its input. The outputs of a
module can be connected to inputs of other modules.

The structure of the network is created via a NetworkDefinition by adding
modules and connections between them.

A network is a channel itself and can be created from a NetworkFactory.
The building blocks of the network are the channels available to the
NetworkFactory instance. New channels types can be created in the
NetworkFactory instance based on a NetworkDefinition. 

Classes:

NetworkDefinition -- Definition of the structure of the network based on identifiers
NetworkFactory -- Creation of network channels based on standard and custom defined channels from a network definition

See also modular.channels.channels

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
    def __init__(self, channel_types):
        """Initializes a new instance from an iterable of allowed module types."""
        self.__modules = ()
        self.__connections = {}
        self.__channel_types = tuple(channel_types)

    def available_module_ids(self):
        """Returns a list with the ids of the modules defined in the current instance."""
        return [module.id for module in self.__modules]

    def add_module(self, module_id, channel_type):
        """Adds the given channel_type with the given module_id to the definition.
        
        If the current instance already contains a module with the given
        module_id, a NameConflictError is raised. If the current instance does
        not accept the specified channel_type, an UndefinedNameError is raised.
        
        """
        if channel_type not in self.__channel_types:
            raise UndefinedNameError("\"{0}\" is not defined".format(channel_type))

        if module_id in self.available_module_ids():
            raise NameConflictError("\"{0}\" is already defined".format(module_id))
        
        self.__modules = self.__modules + (Module(module_id, channel_type), )
        
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
    
    Supports the channel types provided at construction and allows the
    definition of new channel types from a NetworkDefinition.
    
    The created network channels have the following behviour:
    
    The input to is feed to the first module in the network.
    
    Modules are processed in their topolocial order according to the specified
    connections. If the network contains no module, the output is None. The
    inputs of the individual modules are processed in the order in which they
    are specified in the network definition.  
    
    The output is the output of the last module in the network, even if there
    is no connected from the input module.
    
    """
    def __init__(self, channels):
        """Initializes a new instance with the given channels.
        
        channels must privide a mapping from a channels type to a channels
        function for the corresponding Module instances.
        
        """
        self.__channels = channels.copy()
        
    def available_channel_types(self):
        """Returns a list of the available module type identifiers."""
        return self.__channels.keys()
        
    def create(self, network_definition):
        """Returns a network channel based on the given NetworkDefinition.
        
        The returned network channel is a generator function that returns an
        initialized generator that processes input via its send method (See
        also modular.channels.channels).
        
        If the specified network_definition contains module types that are not
        accepted by the current instance, a KeyError is raised.
        
        """
        modules, connections = network_definition._get_state()

        return self.__create(modules, connections, self.__channels)
    
    def __create(self, modules, connections, channels):
        channels = self.__channels
        modules_instances = [Module(module.id, channels[module.channel]) for module in modules]
        
        return partial(network_channel, modules_instances, connections)

    def define_channel_type(self, channel_type, network_definition):
        """Adds support for a new channel type based on the given definition to the current instance.
        
        After defining a channel type, the create method on the current instance
        accepts network definitions containing the specified channel type
        identifier.
        
        If there exitst already a channel type with the given identifier, a
        NameConflictError is raised. If the specified network_definition
        contains module types that are not accepted by the current instance,
        a KeyError is raised.

        """
        if channel_type in self.__channels:
            raise NameConflictError("\"{0}\" is already defined".format(channel_type))
            
        self.__channels[channel_type] = self.__create_network_channel(network_definition)
        
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