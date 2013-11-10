from sound_module.network import NetworkFactory
from itertools import chain
from sound_module.modules import process

EXIT = ()
        
_OUTPUT_LENGTH = 16

class Interpreter(object):
    def __init__(self, state = None, commands = None):
        self.__state = state if state is not None else _InterpreterState()
        self.__commands = commands if commands is not None else _COMMANDS
        
    def parse(self, line):
        if not line or line.isspace():
            return
        
        input_strings = line.split()
        
        command_token =  input_strings[0]
        if not command_token in self.__commands:
            raise CommandError("\"{0}\" is not defined".format(command_token))

        command = self.__commands[command_token]
        arguments = input_strings[1:]

        return command(self.__state, *arguments) if command is not EXIT else EXIT
    
    def print_state(self):
        print(self.__state)
        
    def print_commands(self):
        print(self.__commands.keys())
        
class _InterpreterState():
    def __init__(self):
        self.network_factory = NetworkFactory()
    
    def __str__(self):
        print("Defined modules: ", self.network_factory.available_modules_ids())
        print("Available operations: ", self.network_factory.available_module_types())

def _module(state, *args):
    if len(args) != 2:
        raise ArgumentError("{0} arguments expected, {1} where given, ".format(2, len(args)))
    
    state.network_factory.add_module(*args)

def _connect(state, *args):
    if len(args) != 2:
        raise ArgumentError("{0} arguments expected, {1} where given, ".format(2, len(args)))
    
    state.network_factory.add_connection(*args)

def _process(state, *args):
    inputs = chain(args, iter(str, "infinite generator of empty strings"))
    network = state.network_factory.create()

    result = []
    while len(result) < len(args) * _OUTPUT_LENGTH:
        input_value = next(inputs)
        network, new_value = process(network, input_value)
        result.append(new_value)
    
    print(" ".join(result).strip())
    
def _define(state, *args):
    if len(args) != 1:
        raise ArgumentError("{0} arguments expected, {1} where given, ".format(1, len(args)))
    
    state.network_factory.define_as_module()

def _help(state, *args):
    print(_USAGE)

def _who(state, *args):
    print(state)

_COMMANDS = {"module": _module,
             "connect": _connect,
             "process": _process,
             "define": _define,
             "help": _help,
             "who": _who,
             "exit": EXIT
            }

class CommandError(Exception):
    def __init__(self, value):
        self.__value = value
        
    def __str__(self):
        return self.__value

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