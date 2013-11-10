EXIT = ()
        
class Interpreter(object):
    def __init__(self, state, commands):
        self.__state = state
        self.__commands = commands
        
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
    
class CommandError(Exception):
    def __init__(self, output):
        self.__output = output
        
    def __str__(self):
        return self.__output