from app.app_config import NetworkState, COMMANDS, ArgumentError
from app.interpreter import Interpreter, EXIT, CommandError
from sound_module.network import UndefinedValueError, IllegalOrderError, \
    NameConflictError
import logging

def main():
    print("Type help to get usage information")
    network_state = NetworkState()
    interpreter = Interpreter(network_state, COMMANDS)
    result = ""
    while result is not EXIT:
        try:
            result = interpreter.parse(raw_input(">>> "))
            print(result)
        except (CommandError, ArgumentError) as error:
            print(error)
            print("Available commands: ", COMMANDS.keys())
            print("Type help to get usage information")
        except (UndefinedValueError, IllegalOrderError) as error:
            print(error)
            print(network_state)
        except (NameConflictError) as error:
            print(error)
        
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    main()