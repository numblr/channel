from app.interpreter import Interpreter, EXIT, CommandError, ArgumentError
import logging
from sound_module.network import UndefinedValueError, IllegalOrderError,\
    NameConflictError

_log = logging.getLogger(__name__)

def main():
    print("Type help to get usage information")
    interpreter = Interpreter()
    result = 0
    while not result is EXIT:
        try:
            result = interpreter.parse(raw_input(">>> "))
        except (CommandError, ArgumentError) as error:
            print(error)
            interpreter.print_commands()
            print("Type help to get usage information")
        except (UndefinedValueError, IllegalOrderError) as error:
            print(error)
            interpreter.print_state()
        except (NameConflictError) as error:
            print(error)
        
    return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()