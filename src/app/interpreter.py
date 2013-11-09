from sound_module.network import NetworkFactory
from itertools import chain
from sound_module.modules import process

EXIT = ()
        
_OUTPUT_LENGTH = 16

class Interpreter(object):
    def __init__(self, state = None, commands = None):
        self.__state = state if state else _InterpreterState()
        self.__commands = commands if commands else _COMMANDS
        
    def parse(self, line):
        input_strings = line.split()
        
        command =  input_strings[0]
        if not command in self.__commands:
            raise ValueError("There is no command with name: \"{0}\".\nChoose from: {1}".format(command, _COMMANDS.keys()))
        
        arguments = input_strings[1:]
        
        return self.__commands[command](self.__state, *arguments)
        
class _InterpreterState():
    def __init__(self):
        self.network_factory = NetworkFactory()
        

def _module(state, *args):
    if len(args) != 2:
        raise ValueError("Module definition requires a name and a module type, was {0}.\nChoose from: {1}".format(args, state.network_factory.available_module_types()))
    
    state.network_factory.add_module(*args)
    
    return 0

def _connect(state, *args):
    if len(args) != 2:
        raise ValueError("Connection definition requires two module names, was {0}.\nDefined modules: ".format(args, state.network_factory.available_modules_ids()))
    
    state.network_factory.add_connection(*args)

    return 0

def _process(state, *args):
    inputs = chain(args, iter(str, "infinite generator of empty strings"))
    network = state.network_factory.create()

    result = []
    while len(result) < len(args) * _OUTPUT_LENGTH:
        input_value = next(inputs)
        network, new_value = process(network, input_value)
        result.append(new_value)
    
    print(" ".join(result).strip())

    return 0
    
def _define(state, *args):
    if len(args) != 1:
        raise ValueError("Module type definition \"{0}\"requires a valid type name.\nChoose from: {1}".format(args, state.get_factories().keys()))
    
    state.network_factory.define_as_module()

    return 0

def _help(state, *args):
    print(_USAGE)

def _exit(state, *args):
    return EXIT

_COMMANDS = {"module": _module,
             "connect": _connect,
             "process": _process,
             "define": _define,
             "help": _help,
             "exit": _exit
            }

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