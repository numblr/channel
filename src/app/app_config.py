from app.interpreter import EXIT
from sound_module.network import NetworkFactory
from itertools import islice
from sound_module.modules import process_sequence

_OUTPUT_LENGTH = 16

class NetworkState():
    def __init__(self):
        self.network_factory = NetworkFactory()
    
    def __str__(self):
        return "Defined modules: " + str(self.network_factory.available_modules_ids()) + "\n" \
            + "Available operations: " + str(self.network_factory.available_module_types())

def _module(state, *args):
    if len(args) != 2:
        raise ArgumentError("{0} arguments expected, {1} where given, ".format(2, len(args)))
    
    state.network_factory.add_module(*args)

def _connect(state, *args):
    if len(args) != 2:
        raise ArgumentError("{0} arguments expected, {1} where given, ".format(2, len(args)))
    
    state.network_factory.add_connection(*args)

def _process(state, *args):
    network = state.network_factory.create()
    outputs = process_sequence(network, args)

    result = islice(outputs, len(args) * _OUTPUT_LENGTH)

    return " ".join(result).strip()
    
def _define(state, *args):
    if len(args) != 1:
        raise ArgumentError("{0} arguments expected, {1} where given, ".format(1, len(args)))
    
    state.network_factory.define_as_module()

def _help(state, *args):
    return _USAGE

def _who(state, *args):
    return str(state)

COMMANDS = {"module": _module,
             "connect": _connect,
             "process": _process,
             "define": _define,
             "help": _help,
             "who": _who,
             "exit": EXIT
            }

class ArgumentError(Exception):
    def __init__(self, value):
        self.__value = value
        
    def __str__(self):
        return self.__value

_USAGE = """
Modular string processing utility.

#################################################

Build a network of modules and process strings.
Use the following commands:

-------------------------------------------------

Create a new module:

module <name> <operation>

Default operations are:
noop, echo, delay, reverse.

-------------------------------------------------

Create a new connection between modules:

connection <name_1> <name_2>

Connects the output of the module with name_1 to
the input of the module with name_2.

-------------------------------------------------

Process input

process <string>...

Processes the given strings with the network as
it is currently defined.

-------------------------------------------------

Define new operations:

define <name>

Defines a new operation with the given name from
the network as it is currently defined and clears
the network.

-------------------------------------------------

Get help:

help

-------------------------------------------------

Quit:

exit

"""